#!/usr/bin/env python3
"""Adapter from minimal L1 IR to ObservationEnvelope and ActionGate.

This module keeps L1 as a small control/evidence language. It does not execute
external actions, write patches, publish, fetch network resources or replace
Python/TypeScript/Godot/NASM.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

from obs_l1_ir import parse_l1, run_l1


ADAPTER_SCHEMA = "observacionismo.l1_observation_packet.v0_1"
OBSERVATION_ENVELOPE_VERSION = "seto-observation-v1"
ACTION_GATE_SCHEMA = "medioevo.seto.action_gate.from_l1.v0_1"
ZERO_HASH = "0" * 64

EXTERNAL_ACTION_MARKERS = {
    "browser",
    "delete",
    "deploy",
    "download",
    "external",
    "fetch",
    "gumroad",
    "login",
    "network",
    "publish",
    "push",
    "send",
    "social",
    "upload",
}

WRITE_ACTION_MARKERS = {
    "edit",
    "edit_file",
    "patch",
    "write",
    "move",
    "rename",
}

NON_BLOCKING_RISK_FLAGS = {"low", "low_local", "document_only"}


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":"), default=str)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def fingerprint(payload: Any, prefix: str = "OBS_LANGUAGE_L1_ENVELOPE_V01_2026-05-06") -> str:
    return f"{prefix}_{sha256_text(canonical_json(payload))[:12]}"


def _append_metadata(metadata: dict[str, Any], key: str, value: str) -> None:
    list_keys = {"evidence", "falsifier", "risk"}
    if key in list_keys:
        metadata.setdefault(key, []).append(value)
    else:
        metadata[key] = value


def parse_metadata(script: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "claim": "",
        "evidence": [],
        "falsifier": [],
        "risk": [],
        "residue": "",
        "action": "",
        "gate": "INHERIT",
        "handoff": "",
    }
    aliases = {
        "claim": "claim",
        "evidence": "evidence",
        "evidencia": "evidence",
        "falsifier": "falsifier",
        "falsador": "falsifier",
        "risk": "risk",
        "riesgo": "risk",
        "residue": "residue",
        "residuo": "residue",
        "action": "action",
        "accion": "action",
        "gate": "gate",
        "handoff": "handoff",
    }
    for raw in script.splitlines():
        line = raw.strip()
        if not line.startswith("#") or ":" not in line:
            continue
        key, value = line[1:].split(":", 1)
        normalized = aliases.get(key.strip().lower())
        if normalized:
            _append_metadata(metadata, normalized, value.strip())
    metadata["gate"] = str(metadata.get("gate") or "INHERIT").upper()
    return metadata


def _action_tokens(action: str) -> set[str]:
    text = action.lower().replace(":", " ").replace("/", " ").replace("\\", " ")
    return {part for part in text.replace("-", "_").split() if part}


def normalize_optional(value: Any) -> str:
    text = str(value or "").strip()
    if text.lower() in {"", "none", "ninguno", "no", "false", "null"}:
        return ""
    return text


def classify_action(action: str) -> dict[str, Any]:
    tokens = _action_tokens(action)
    external = bool(tokens & EXTERNAL_ACTION_MARKERS) or "http" in action.lower()
    write = bool(tokens & WRITE_ACTION_MARKERS)
    handoff = "handoff" in tokens or "entregar" in tokens
    return {
        "action": action,
        "external": external,
        "write": write,
        "handoff": handoff,
        "tokens": sorted(tokens),
    }


def _gate_from_metadata(metadata_gate: str, risk_flags: list[str], ok: bool, action_class: dict[str, Any]) -> str:
    gate = str(metadata_gate or "INHERIT").upper()
    if gate == "BLOCK" or action_class["external"]:
        return "BLOCK"
    if "missing_evidence" in risk_flags or action_class["write"] or action_class["handoff"] or not ok:
        return "REVIEW"
    if gate in {"APPROVE", "REVIEW"}:
        return gate
    return "APPROVE"


def _psi_state(action_gate: str, ok: bool, risk_flags: list[str]) -> str:
    if action_gate == "BLOCK":
        return "BLOQUEADO"
    blocking_risk_flags = [flag for flag in risk_flags if flag not in NON_BLOCKING_RISK_FLAGS]
    if ok and not blocking_risk_flags:
        return "CERTEZA"
    return "INFERENCIA"


def compile_l1_to_observation_packet(
    script: str,
    *,
    inputs: Sequence[int] = (),
    source_path: str = "<inline_l1>",
) -> dict[str, Any]:
    metadata = parse_metadata(script)
    result = run_l1(script, inputs=inputs)
    program = parse_l1(script)
    action_class = classify_action(str(metadata.get("action") or ""))
    handoff_target = normalize_optional(metadata.get("handoff"))
    claim_evidence = [str(item) for item in metadata.get("evidence", []) if str(item).strip()]
    risk_flags = [str(item) for item in metadata.get("risk", []) if str(item).strip()]
    if not claim_evidence:
        risk_flags.append("missing_evidence")
    if action_class["external"]:
        risk_flags.append("blocked_external_action")
    if action_class["write"]:
        risk_flags.append("write_requires_action_gate")
    if action_class["handoff"]:
        risk_flags.append("handoff_requires_review")
    if not result["ok"]:
        risk_flags.append("verification_failed")
    risk_flags = sorted(set(risk_flags))
    action_gate = _gate_from_metadata(str(metadata.get("gate") or "INHERIT"), risk_flags, bool(result["ok"]), action_class)
    claim = str(metadata.get("claim") or "L1 program compiled to ObservationEnvelope")
    falsifiers = [str(item) for item in metadata.get("falsifier", []) if str(item).strip()]
    falsifiers.extend(
        [
            "L1 parser rejects the program",
            "ObsBitMachine output does not satisfy VERIFICAR checks",
            "ActionGate allows external or write action without explicit approval",
        ]
    )
    script_sha = sha256_text(script)
    envelope = {
        "envelope_version": OBSERVATION_ENVELOPE_VERSION,
        "source_path": source_path,
        "source_kind": "generated_artifact",
        "sha256": script_sha,
        "size_bytes": len(script.encode("utf-8")),
        "evidence": claim_evidence or ["compiler evidence only: missing claim evidence"],
        "psi_state": _psi_state(action_gate, bool(result["ok"]), risk_flags),
        "claim_level": "blocked_claim" if action_gate == "BLOCK" else "operational",
        "falsifiers": falsifiers,
        "risk_flags": risk_flags,
        "action_gate": action_gate,
        "decision": "BLOCK_L1_ACTION" if action_gate == "BLOCK" else ("REVIEW_L1_PROGRAM" if action_gate == "REVIEW" else "KEEP_L1_ENVELOPE_LOCAL"),
        "fingerprint": ZERO_HASH,
    }
    contract = {
        "type": "ObservationEnvelope",
        "claim": claim,
        "evidence": envelope["evidence"],
        "risk": ",".join(risk_flags) if risk_flags else "none",
        "residue": metadata.get("residue") or str(result["residue"]),
        "action": metadata.get("action") or "none",
        "gate_required": action_gate in {"REVIEW", "BLOCK"} or action_class["write"] or action_class["external"],
        "handoff": {
            "target": handoff_target,
            "required": bool(handoff_target or action_class["handoff"]),
        },
    }
    packet = {
        "schema": ADAPTER_SCHEMA,
        "source_path": source_path,
        "metadata": metadata,
        "l1": {
            "verbs": [step.verb.lower() for step in program.steps],
            "bytecode": result["bytecode"],
            "assembly": result["assembly"],
            "checks": result["checks"],
            "ok": result["ok"],
            "residue": result["residue"],
            "phi_eff": result["phi_eff"],
        },
        "contract": contract,
        "observation_envelope": envelope,
    }
    envelope["fingerprint"] = fingerprint(packet)
    packet["fingerprint"] = envelope["fingerprint"]
    packet["action_gate"] = observation_envelope_to_action_gate(envelope, contract=contract)
    return packet


def observation_envelope_to_action_gate(envelope: dict[str, Any], *, contract: dict[str, Any] | None = None) -> dict[str, Any]:
    risk_flags = [str(item) for item in envelope.get("risk_flags", [])]
    decision = str(envelope.get("action_gate") or "REVIEW").upper()
    if "blocked_external_action" in risk_flags:
        decision = "BLOCK"
    elif decision == "APPROVE" and ("missing_evidence" in risk_flags or "write_requires_action_gate" in risk_flags):
        decision = "REVIEW"
    required_evidence = []
    if "missing_evidence" in risk_flags:
        required_evidence.append("claim evidence artifact")
    if "verification_failed" in risk_flags:
        required_evidence.append("passing VERIFICAR checks")
    if "write_requires_action_gate" in risk_flags:
        required_evidence.append("explicit write target approval")
    if "blocked_external_action" in risk_flags:
        required_evidence.append("target-specific external ActionGate")
    return {
        "schema": ACTION_GATE_SCHEMA,
        "decision": decision,
        "risk_flags": risk_flags,
        "required_evidence": required_evidence,
        "no_delete": True,
        "no_move": True,
        "no_external_action": True,
        "no_write_to_concurrent_lane": decision != "APPROVE",
        "requires_hash_refresh_before_future_action": True,
        "requires_canonical_replacement_or_keep_decision": False,
        "post_validation": [
            "run research observacionismo-lab tests",
            "verify ObservationEnvelope fingerprint",
            "review ActionGate before any write or external action",
        ],
        "source_fingerprint": envelope.get("fingerprint", ""),
        "contract": contract or {},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile L1 script to ObservationEnvelope packet")
    parser.add_argument("script", type=Path)
    parser.add_argument("--inputs", default="", help="Comma-separated bit inputs, for example 1,0")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)
    inputs = [int(item.strip()) for item in args.inputs.split(",") if item.strip()]
    packet = compile_l1_to_observation_packet(
        args.script.read_text(encoding="utf-8"),
        inputs=inputs,
        source_path=str(args.script),
    )
    print(json.dumps(packet, ensure_ascii=True, indent=2 if args.pretty else None, sort_keys=bool(args.pretty)))
    return 0 if packet["action_gate"]["decision"] != "BLOCK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
