#!/usr/bin/env python3
"""Build a dry programmer workpack from an L1 ObservationEnvelope packet.

The workpack is a planning artifact for a programmer agent. It never applies
patches, never runs external commands and never converts L1 `actuar` into write
permission.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from l1_to_envelope import canonical_json, compile_l1_to_observation_packet, fingerprint


WORKPACK_SCHEMA = "observacionismo.l1_programmer_workpack.v0_1"
COMMS_MESSAGE_SCHEMA = "observacionismo.l1_programmer_workpack.comms_message.v0_1"
DEFAULT_COMMS_SENDER = "observacionismo-lab"
DEFAULT_COMMS_RECIPIENT = "claudio-local-agent"
DEFAULT_COMMS_MESSAGE_TYPE = "L1_PROGRAMMER_WORKPACK_READY"

FORBIDDEN_OPERATIONS = [
    "apply_patch",
    "delete",
    "download",
    "external_network",
    "git_push",
    "login",
    "move_files",
    "publish",
    "run_shell",
    "store_credentials",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _action_value(packet: dict[str, Any]) -> str:
    return str(packet.get("contract", {}).get("action") or packet.get("metadata", {}).get("action") or "")


def extract_action_targets(action: str) -> list[str]:
    """Extract local path-like targets from compact action metadata.

    Supported examples:
    - edit_file:docs/example.md
    - patch:research/example.py

    External URLs are intentionally ignored; they are represented as risk flags,
    not target paths.
    """

    targets: list[str] = []
    for marker in ("edit_file:", "patch:", "write:", "edit:"):
        if marker in action:
            value = action.split(marker, 1)[1].split()[0].strip().strip(",;")
            if value and "://" not in value:
                targets.append(value.replace("\\", "/"))
    for match in re.findall(r"`([^`]+)`", action):
        if "://" not in match and any(char in match for char in ("/", "\\", ".")):
            targets.append(match.replace("\\", "/"))
    seen: set[str] = set()
    unique: list[str] = []
    for target in targets:
        if target not in seen:
            seen.add(target)
            unique.append(target)
    return unique


def classify_workpack(packet: dict[str, Any]) -> str:
    gate = packet.get("action_gate", {})
    decision = str(gate.get("decision") or packet.get("observation_envelope", {}).get("action_gate") or "REVIEW").upper()
    risks = set(str(item) for item in packet.get("observation_envelope", {}).get("risk_flags", []))
    if decision == "BLOCK" or "blocked_external_action" in risks:
        return "BLOCKED_BY_ACTION_GATE"
    if "missing_evidence" in risks:
        return "REVIEW_MISSING_EVIDENCE"
    if "write_requires_action_gate" in risks:
        return "REVIEW_PATCH_PLAN_ONLY"
    if "handoff_requires_review" in risks or packet.get("contract", {}).get("handoff", {}).get("required"):
        return "HANDOFF_REVIEW"
    if decision == "APPROVE":
        return "READY_READ_ONLY"
    return "REVIEW_REQUIRED"


def build_programmer_workpack(packet: dict[str, Any]) -> dict[str, Any]:
    status = classify_workpack(packet)
    action = _action_value(packet)
    target_paths = extract_action_targets(action)
    may_prepare_patch = status == "REVIEW_PATCH_PLAN_ONLY" and bool(target_paths)
    action_gate_decision = packet.get("action_gate", {}).get("decision", "REVIEW")
    workpack = {
        "schema": WORKPACK_SCHEMA,
        "source_packet_fingerprint": packet.get("fingerprint", ""),
        "programmer_agent": {
            "recommended_agent": "claudio-local-agent",
            "mode": "dry_workpack_only",
            "may_execute": False,
        },
        "status": status,
        "intent": packet.get("contract", {}).get("claim", ""),
        "observation_envelope": packet.get("observation_envelope", {}),
        "action_gate": packet.get("action_gate", {}),
        "proposed_scope": {
            "action": action,
            "target_paths": target_paths,
            "private_boundary_touched": False,
            "external_boundary_touched": "blocked_external_action" in packet.get("observation_envelope", {}).get("risk_flags", []),
        },
        "patch_policy": {
            "may_prepare_patch_plan": may_prepare_patch,
            "may_apply_patch": False,
            "requires_action_gate": action_gate_decision != "APPROVE" or may_prepare_patch,
            "rollback_required_before_apply": True,
            "no_auto_write": True,
        },
        "evidence_refs": packet.get("contract", {}).get("evidence", []),
        "risk_flags": packet.get("observation_envelope", {}).get("risk_flags", []),
        "validation_required": [
            "read ObservationEnvelope fingerprint",
            "read ActionGate decision",
            "prepare diff only if status is REVIEW_PATCH_PLAN_ONLY",
            "do not apply patch without separate ActionGate APPROVE",
            "run module-specific tests after any future approved write",
        ],
        "forbidden_operations": FORBIDDEN_OPERATIONS,
        "handoff": packet.get("contract", {}).get("handoff", {}),
        "falsifiers": [
            "workpack sets may_apply_patch=true",
            "workpack omits ActionGate",
            "external action is not BLOCKED_BY_ACTION_GATE",
            "missing evidence is not REVIEW_MISSING_EVIDENCE",
            "patch target is applied instead of planned",
        ],
    }
    workpack["workpack_id"] = fingerprint(workpack, prefix="OBS_L1_PROGRAMMER_WORKPACK_V01_2026-05-06")
    return workpack


def validate_programmer_workpack(workpack: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if workpack.get("schema") != WORKPACK_SCHEMA:
        errors.append("schema mismatch")
    patch_policy = workpack.get("patch_policy", {})
    if patch_policy.get("may_apply_patch") is not False:
        errors.append("may_apply_patch must be false")
    if patch_policy.get("no_auto_write") is not True:
        errors.append("no_auto_write must be true")
    if workpack.get("programmer_agent", {}).get("may_execute") is not False:
        errors.append("programmer_agent.may_execute must be false")
    forbidden = set(workpack.get("forbidden_operations", []))
    for operation in FORBIDDEN_OPERATIONS:
        if operation not in forbidden:
            errors.append(f"missing forbidden operation: {operation}")
    risks = set(workpack.get("risk_flags", []))
    if "blocked_external_action" in risks and workpack.get("status") != "BLOCKED_BY_ACTION_GATE":
        errors.append("external action risk must produce BLOCKED_BY_ACTION_GATE")
    if "missing_evidence" in risks and workpack.get("status") not in {"REVIEW_MISSING_EVIDENCE", "BLOCKED_BY_ACTION_GATE"}:
        errors.append("missing evidence must produce REVIEW_MISSING_EVIDENCE")
    if workpack.get("status") == "REVIEW_PATCH_PLAN_ONLY" and not workpack.get("proposed_scope", {}).get("target_paths"):
        errors.append("patch plan status requires target_paths")
    return {
        "schema": "observacionismo.l1_programmer_workpack.validation.v0_1",
        "ok": not errors,
        "errors": errors,
        "status": workpack.get("status", "UNKNOWN"),
        "workpack_id": workpack.get("workpack_id", ""),
    }


def _message_status(workpack: dict[str, Any]) -> str:
    status = str(workpack.get("status") or "REVIEW_REQUIRED")
    if status == "BLOCKED_BY_ACTION_GATE":
        return "BLOCK"
    if status == "READY_READ_ONLY":
        return "READY"
    return "REVIEW"


def build_comms_message(
    workpack: dict[str, Any],
    *,
    sender: str = DEFAULT_COMMS_SENDER,
    recipient: str = DEFAULT_COMMS_RECIPIENT,
    message_type: str = DEFAULT_COMMS_MESSAGE_TYPE,
) -> dict[str, Any]:
    """Build a COMMS-compatible message that embeds the dry workpack."""

    message = {
        "schema": COMMS_MESSAGE_SCHEMA,
        "message_id": f"l1-workpack-{workpack.get('workpack_id', '')}",
        "timestamp_utc": utc_now(),
        "sender": sender,
        "recipient": recipient,
        "message_type": message_type,
        "status": _message_status(workpack),
        "action_gate": workpack.get("action_gate", {}).get("decision", "REVIEW"),
        "observation_envelope": workpack.get("observation_envelope", {}),
        "workpack": {
            "schema": workpack.get("schema"),
            "workpack_id": workpack.get("workpack_id"),
            "status": workpack.get("status"),
            "source_packet_fingerprint": workpack.get("source_packet_fingerprint"),
            "programmer_agent": workpack.get("programmer_agent"),
            "proposed_scope": workpack.get("proposed_scope"),
            "patch_policy": workpack.get("patch_policy"),
            "validation": workpack.get("validation"),
            "forbidden_operations": workpack.get("forbidden_operations"),
        },
        "routing": {
            "target_stream": f"COMMS/inbox/{recipient}.jsonl",
            "does_not_execute": True,
            "append_only": True,
            "consumer_must_review_action_gate": True,
        },
    }
    message["message_hash"] = fingerprint(message, prefix="OBS_L1_WORKPACK_COMMS_V01_2026-05-06")
    return message


def validate_comms_message(message: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    required = {
        "message_id",
        "timestamp_utc",
        "sender",
        "recipient",
        "message_type",
        "status",
        "observation_envelope",
        "workpack",
        "routing",
        "message_hash",
    }
    missing = sorted(required - set(message))
    if missing:
        errors.append(f"missing keys: {', '.join(missing)}")
    envelope = message.get("observation_envelope", {})
    if not isinstance(envelope, dict):
        errors.append("observation_envelope must be object")
    elif envelope.get("envelope_version") != "seto-observation-v1":
        errors.append("bad observation envelope version")
    workpack = message.get("workpack", {})
    if workpack.get("patch_policy", {}).get("may_apply_patch") is not False:
        errors.append("embedded workpack may_apply_patch must be false")
    if message.get("routing", {}).get("does_not_execute") is not True:
        errors.append("routing.does_not_execute must be true")
    if message.get("routing", {}).get("append_only") is not True:
        errors.append("routing.append_only must be true")
    return {
        "schema": "observacionismo.l1_programmer_workpack.comms_validation.v0_1",
        "ok": not errors,
        "errors": errors,
        "message_id": message.get("message_id", ""),
        "action_gate": message.get("action_gate", "REVIEW"),
    }


def append_comms_message(inbox_path: str | Path, message: dict[str, Any]) -> dict[str, Any]:
    validation = validate_comms_message(message)
    if not validation["ok"]:
        raise ValueError("; ".join(validation["errors"]))
    target = Path(inbox_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(message, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n")
    return {
        "schema": "observacionismo.l1_programmer_workpack.comms_append.v0_1",
        "ok": True,
        "path": str(target),
        "message_id": message.get("message_id"),
        "action_gate": message.get("action_gate"),
    }


def build_workpack_from_l1(script: str, *, inputs: Sequence[int] = (), source_path: str = "<inline_l1>") -> dict[str, Any]:
    packet = compile_l1_to_observation_packet(script, inputs=inputs, source_path=source_path)
    workpack = build_programmer_workpack(packet)
    workpack["validation"] = validate_programmer_workpack(workpack)
    return workpack


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a dry programmer workpack from L1")
    parser.add_argument("script", type=Path)
    parser.add_argument("--inputs", default="", help="Comma-separated bit inputs")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--comms-inbox", type=Path, help="Append COMMS inbox message. No COMMS write occurs unless supplied.")
    parser.add_argument("--comms-sender", default=DEFAULT_COMMS_SENDER)
    parser.add_argument("--comms-recipient", default=DEFAULT_COMMS_RECIPIENT)
    parser.add_argument("--comms-message-type", default=DEFAULT_COMMS_MESSAGE_TYPE)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)
    inputs = [int(item.strip()) for item in args.inputs.split(",") if item.strip()]
    workpack = build_workpack_from_l1(
        args.script.read_text(encoding="utf-8"),
        inputs=inputs,
        source_path=str(args.script),
    )
    if args.comms_inbox:
        message = build_comms_message(
            workpack,
            sender=args.comms_sender,
            recipient=args.comms_recipient,
            message_type=args.comms_message_type,
        )
        workpack["comms_message"] = message
        workpack["comms_append"] = append_comms_message(args.comms_inbox, message)
    text = json.dumps(workpack, ensure_ascii=True, indent=2 if args.pretty else None, sort_keys=bool(args.pretty))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if workpack["validation"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
