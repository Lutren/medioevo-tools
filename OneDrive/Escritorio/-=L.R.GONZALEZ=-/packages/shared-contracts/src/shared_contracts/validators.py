from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = PACKAGE_ROOT / "schemas"
FIXTURE_DIR = PACKAGE_ROOT / "fixtures"

CONTRACT_SCHEMAS = {
    "TaskSpec": "task_spec.schema.json",
    "Workpack": "workpack.schema.json",
    "WorldState": "world_state.schema.json",
    "AgentState": "agent_state.schema.json",
    "ObservationEnvelope": "observation_envelope.schema.json",
    "SharedReality": "shared_reality.schema.json",
    "BiasProfile": "bias_profile.schema.json",
    "TheatreLineage": "theatre_lineage.schema.json",
    "ScenarioSpec": "scenario_spec.schema.json",
    "EventInjection": "event_injection.schema.json",
    "DirectorCommand": "director_command.schema.json",
    "RenderFrameRequest": "render_frame_request.schema.json",
    "RendererCapabilityProfile": "renderer_capability_profile.schema.json",
    "AssetManifest": "asset_manifest.schema.json",
    "ReplayFrame": "replay_frame.schema.json",
    "ReplayHash": "replay_hash.schema.json",
    "ActionGateDecision": "action_gate_decision.schema.json",
    "WitnessEvent": "witness_event.schema.json",
    "HandoffPacket": "handoff_packet.schema.json",
    "ForgeProjectSpec": "forge_project_spec.schema.json",
    "HypothesisPacket": "hypothesis_packet.schema.json",
}

SYSTEMS = {
    "WABI_SABI_CONTROL_PLANE",
    "DUAT_SIMULATOR_WORLD",
    "MEDIOEVO_FORGE_APP_GAME_CREATOR",
    "MEDIOEVO_SPACE_PUBLIC_PORTAL",
    "SHARED_CONTRACTS",
}

FORBIDDEN_KEYS = {
    ".env",
    "api_key",
    "apikey",
    "bearer",
    "credential",
    "credentials",
    "env",
    "password",
    "private_canon",
    "private_key",
    "raw_dataset",
    "raw_media",
    "raw_prompt",
    "rpg_private",
    "secret",
    "secrets",
    "tcg_private",
    "token",
    "tokens",
}

FORBIDDEN_VALUE_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bghp_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
]


class ValidationError(ValueError):
    pass


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schema(contract_name: str) -> dict[str, Any]:
    try:
        filename = CONTRACT_SCHEMAS[contract_name]
    except KeyError as exc:
        raise ValidationError(f"unknown_contract:{contract_name}") from exc
    data = load_json(SCHEMA_DIR / filename)
    if not isinstance(data, dict):
        raise ValidationError(f"schema_not_object:{filename}")
    return data


def load_fixture(filename: str) -> Any:
    return load_json(FIXTURE_DIR / filename)


def validate_schema_shape(contract_name: str, payload: Any) -> None:
    schema = load_schema(contract_name)
    _validate_value(payload, schema, f"${contract_name}")


def validate_no_dangerous_fields(payload: Any, path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            lowered = str(key).strip().casefold()
            if lowered in FORBIDDEN_KEYS:
                raise ValidationError(f"dangerous_field:{path}.{key}")
            validate_no_dangerous_fields(value, f"{path}.{key}")
        return
    if isinstance(payload, list):
        for index, item in enumerate(payload):
            validate_no_dangerous_fields(item, f"{path}[{index}]")
        return
    if isinstance(payload, str):
        for pattern in FORBIDDEN_VALUE_PATTERNS:
            if pattern.search(payload):
                raise ValidationError(f"dangerous_value:{path}")


def validate_boundary(contract_name: str, payload: dict[str, Any]) -> None:
    boundary = payload.get("boundary")
    if isinstance(boundary, dict):
        if boundary.get("contains_private_data") is True:
            raise ValidationError(f"private_data_blocked:{contract_name}")
        if boundary.get("publication_gate") != "BLOCK":
            raise ValidationError(f"publication_gate_must_block:{contract_name}")

    destination = payload.get("destination_system") or payload.get("target_system")
    if destination == "MEDIOEVO_SPACE_PUBLIC_PORTAL":
        if payload.get("public_safe") is not True:
            raise ValidationError("portal_requires_public_safe_true")
        if isinstance(boundary, dict) and boundary.get("contains_private_data") is not False:
            raise ValidationError("portal_requires_no_private_data")

    if contract_name == "ForgeProjectSpec":
        mode = payload.get("integration_mode")
        mutates = set(payload.get("mutates_systems", []))
        if mode == "direct_mutation" or "DUAT_SIMULATOR_WORLD" in mutates:
            raise ValidationError("forge_must_not_mutate_duat_directly")

    source = payload.get("source_system")
    if source == "WABI_SABI_CONTROL_PLANE":
        gate = payload.get("action_gate")
        if not isinstance(gate, dict):
            raise ValidationError("wabi_requires_action_gate")
        operation = payload.get("operation", {})
        kind = operation.get("kind") if isinstance(operation, dict) else None
        if kind == "apply" and gate.get("decision") != "APPROVE":
            raise ValidationError("wabi_apply_requires_approve_gate")


def validate_contract(contract_name: str, payload: Any) -> None:
    validate_schema_shape(contract_name, payload)
    validate_no_dangerous_fields(payload)
    if isinstance(payload, dict):
        validate_boundary(contract_name, payload)


def _validate_value(value: Any, schema: dict[str, Any], path: str) -> None:
    expected = schema.get("type")
    if expected is not None and not _matches_type(value, expected):
        raise ValidationError(f"type_mismatch:{path}:expected={expected}")

    if "const" in schema and value != schema["const"]:
        raise ValidationError(f"const_mismatch:{path}")

    if "enum" in schema and value not in schema["enum"]:
        raise ValidationError(f"enum_mismatch:{path}:{value}")

    if "pattern" in schema and isinstance(value, str):
        if re.fullmatch(schema["pattern"], value) is None:
            raise ValidationError(f"pattern_mismatch:{path}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                raise ValidationError(f"missing_required:{path}.{key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    raise ValidationError(f"additional_property:{path}.{key}")
        for key, child_schema in properties.items():
            if key in value:
                _validate_value(value[key], child_schema, f"{path}.{key}")

    if isinstance(value, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < int(min_items):
            raise ValidationError(f"min_items:{path}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate_value(item, item_schema, f"{path}[{index}]")


def _matches_type(value: Any, expected: str | list[str]) -> bool:
    if isinstance(expected, list):
        return any(_matches_type(value, item) for item in expected)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True
