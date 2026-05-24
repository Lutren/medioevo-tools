from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "src"))

from shared_contracts import (  # noqa: E402
    CONTRACT_SCHEMAS,
    ValidationError,
    canonical_json,
    load_fixture,
    load_schema,
    replay_hash,
    validate_contract,
    validate_no_dangerous_fields,
)


FIXTURE_BY_CONTRACT = {
    "TaskSpec": "task_spec_minimal.json",
    "Workpack": "workpack_minimal.json",
    "WorldState": "world_state_minimal.json",
    "AgentState": "agent_state_001.json",
    "ObservationEnvelope": "observation_envelope_minimal.json",
    "SharedReality": "shared_reality_minimal.json",
    "BiasProfile": "bias_profile_minimal.json",
    "TheatreLineage": "theatre_lineage_minimal.json",
    "ScenarioSpec": "scenario_spec_minimal.json",
    "EventInjection": "event_injection_minimal.json",
    "DirectorCommand": "director_command_minimal.json",
    "RenderFrameRequest": "render_frame_request_minimal.json",
    "RendererCapabilityProfile": "renderer_capability_profile_minimal.json",
    "AssetManifest": "asset_manifest_minimal.json",
    "ReplayFrame": "replay_frame_minimal.json",
    "ReplayHash": "replay_hash_minimal.json",
    "ActionGateDecision": "action_gate_decision_approve.json",
    "WitnessEvent": "witness_event_minimal.json",
    "HandoffPacket": "handoff_packet_minimal.json",
    "ForgeProjectSpec": "forge_project_spec_minimal.json",
    "HypothesisPacket": "hypothesis_packet_minimal.json",
}


class SharedContractsP0Tests(unittest.TestCase):
    def test_all_schemas_parse(self) -> None:
        self.assertEqual(len(CONTRACT_SCHEMAS), 21)
        for contract_name in CONTRACT_SCHEMAS:
            schema = load_schema(contract_name)
            self.assertEqual(schema["type"], "object")
            self.assertIn("required", schema)
            self.assertIn("properties", schema)

    def test_fixtures_validate_against_contracts(self) -> None:
        for contract_name, fixture_name in FIXTURE_BY_CONTRACT.items():
            with self.subTest(contract_name=contract_name):
                validate_contract(contract_name, load_fixture(fixture_name))

    def test_three_agent_fixtures_validate_with_bias_and_lineage(self) -> None:
        for fixture_name in ["agent_state_001.json", "agent_state_002.json", "agent_state_003.json"]:
            agent = load_fixture(fixture_name)
            validate_contract("AgentState", agent)
            self.assertIn("bias_profile", agent)
            self.assertIn("lineage", agent)

    def test_replay_hash_determinism(self) -> None:
        payload = load_fixture("replay_frame_minimal.json")["state_delta"]
        left = replay_hash(seed="duat-seed-001", payload=payload, prev_hash="GENESIS")
        right = replay_hash(seed="duat-seed-001", payload={"events_added": ["event-light-source-001"]}, prev_hash="GENESIS")
        changed = replay_hash(seed="duat-seed-002", payload=payload, prev_hash="GENESIS")
        self.assertEqual(left, right)
        self.assertNotEqual(left, changed)
        self.assertEqual(len(left), 64)

    def test_canonical_json_is_key_order_stable(self) -> None:
        self.assertEqual(canonical_json({"b": 2, "a": 1}), canonical_json({"a": 1, "b": 2}))

    def test_public_safe_portal_boundary_passes_and_blocks_private(self) -> None:
        handoff = load_fixture("handoff_packet_minimal.json")
        validate_contract("HandoffPacket", handoff)
        unsafe = copy.deepcopy(handoff)
        unsafe["public_safe"] = False
        with self.assertRaisesRegex(ValidationError, "portal_requires_public_safe_true"):
            validate_contract("HandoffPacket", unsafe)

    def test_forge_cannot_mutate_duat_directly(self) -> None:
        spec = load_fixture("forge_project_spec_minimal.json")
        validate_contract("ForgeProjectSpec", spec)
        unsafe = copy.deepcopy(spec)
        unsafe["integration_mode"] = "direct_mutation"
        unsafe["mutates_systems"] = ["DUAT_SIMULATOR_WORLD"]
        with self.assertRaisesRegex(ValidationError, "forge_must_not_mutate_duat_directly"):
            validate_contract("ForgeProjectSpec", unsafe)

    def test_wabi_apply_requires_approve_gate(self) -> None:
        workpack = load_fixture("workpack_minimal.json")
        unsafe = copy.deepcopy(workpack)
        unsafe["operation"]["kind"] = "apply"
        unsafe["action_gate"]["decision"] = "REVIEW"
        with self.assertRaisesRegex(ValidationError, "wabi_apply_requires_approve_gate"):
            validate_contract("Workpack", unsafe)

    def test_dangerous_fields_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValidationError, "dangerous_field"):
            validate_no_dangerous_fields({"nested": {"api_key": "redacted"}})

    def test_witness_event_json_parses(self) -> None:
        path = PACKAGE_ROOT / "fixtures" / "witness_event_minimal.json"
        parsed = json.loads(path.read_text(encoding="utf-8"))
        validate_contract("WitnessEvent", parsed)
        self.assertEqual(parsed["schema_version"], "medioevo.witness_event.v0.1")

    def test_hypothesis_packet_requires_falsifiers(self) -> None:
        packet = load_fixture("hypothesis_packet_minimal.json")
        validate_contract("HypothesisPacket", packet)
        unsafe = copy.deepcopy(packet)
        unsafe["falsifiers"] = []
        with self.assertRaisesRegex(ValidationError, "min_items"):
            validate_contract("HypothesisPacket", unsafe)


if __name__ == "__main__":
    unittest.main()
