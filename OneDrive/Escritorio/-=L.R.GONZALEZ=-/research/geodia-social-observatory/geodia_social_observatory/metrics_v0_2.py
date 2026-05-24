"""Metrics and falsifiers for DUAT Smallville v0.2."""

from __future__ import annotations

from collections import Counter
from typing import Any

from .contracts import DUAT_SMALLVILLE_FALSIFIER_V0_2_SCHEMA, DUAT_SMALLVILLE_METRICS_SCHEMA
from .replay_verifier import verify_replay, verify_v0_2_hash_chain
from .signal_source_pack import assert_no_real_data_or_credentials
from .smallville_lab import stable_hash
from .synthetic_environment_channels import fuse_environment_channels


def _states(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    return [state for event in ledger.get("events", []) for state in event.get("agent_states", [])]


def _mean(values: list[float]) -> float:
    return round(sum(values) / max(1, len(values)), 6)


def summarize_ledger_metrics(ledger: dict[str, Any]) -> dict[str, Any]:
    states = _states(ledger)
    gates = Counter(state["gate"] for state in states)
    return {
        "R_env_mean": _mean([state["r_state"]["R_env"] for state in states]),
        "R_social_mean": _mean([state["r_state"]["R_social"] for state in states]),
        "R_geologic_mean": _mean([state["r_state"]["R_geologic"] for state in states]),
        "R_weather_mean": _mean([state["r_state"]["R_weather"] for state in states]),
        "R_contradiction_max": round(max((state["r_state"]["R_contradiction"] for state in states), default=0.0), 6),
        "fusion_R_mean": _mean([state["r_state"]["fusion_R"] for state in states]),
        "J_c_proximity_max": round(max((state["r_state"]["fusion_R"] / 0.45 for state in states), default=0.0), 6),
        "phi_eff_mean": _mean([state["phi_eff"] for state in states]),
        "phi_eff_min": round(min((state["phi_eff"] for state in states), default=0.0), 6),
        "phi_eff_max": round(max((state["phi_eff"] for state in states), default=0.0), 6),
        "gates": {gate: gates.get(gate, 0) for gate in ("APPROVE", "REVIEW", "BLOCK")},
    }


def _contradiction_preservation_check() -> bool:
    observations = {
        "weather": {"phi_eff_i": 0.9, "bandwidth": 0.9, "calibration": 0.9, "r_total": 0.1, "missingness": 0.0, "contradiction": 0.0},
        "geophysics": {"phi_eff_i": 0.9, "bandwidth": 0.9, "calibration": 0.9, "r_total": 0.1, "missingness": 0.0, "contradiction": 0.0},
        "social_pressure": {"phi_eff_i": 0.9, "bandwidth": 0.9, "calibration": 0.9, "r_total": 0.1, "missingness": 0.0, "contradiction": 0.62},
        "infrastructure": {"phi_eff_i": 0.9, "bandwidth": 0.9, "calibration": 0.9, "r_total": 0.1, "missingness": 0.0, "contradiction": 0.0},
        "resource_availability": {"phi_eff_i": 0.9, "bandwidth": 0.9, "calibration": 0.9, "r_total": 0.1, "missingness": 0.0, "contradiction": 0.0},
    }
    return fuse_environment_channels(observations)["gate"] == "REVIEW"


def _jamming_gate_check() -> bool:
    observations = {
        name: {"phi_eff_i": 0.35, "bandwidth": 0.7, "calibration": 0.75, "r_total": 0.62, "missingness": 0.1, "contradiction": 0.0}
        for name in ("weather", "geophysics", "social_pressure", "infrastructure", "resource_availability")
    }
    result = fuse_environment_channels(observations)
    return result["fusion_R"] >= 0.45 and result["gate"] in {"REVIEW", "BLOCK"} and result["regime"] in {"PRE_JAMMING", "JAMMING"}


def falsify_v0_2(pack: dict[str, Any], baseline: dict[str, Any], intervention: dict[str, Any], delta: dict[str, Any]) -> dict[str, Any]:
    replay = verify_replay(baseline, pack)
    no_real_data = assert_no_real_data_or_credentials(pack)
    intervention_delta = delta["intervention_delta"]
    text = repr({"pack": pack, "baseline": baseline, "intervention": intervention, "delta": delta}).lower()
    checks = [
        {"name": "replay_determinism", "passed": replay["replay_verified"], "decision_if_failed": "BLOCK"},
        {"name": "hash_chain", "passed": verify_v0_2_hash_chain(baseline) and verify_v0_2_hash_chain(intervention), "decision_if_failed": "BLOCK"},
        {"name": "contradiction_preservation", "passed": _contradiction_preservation_check(), "decision_if_failed": "BLOCK"},
        {
            "name": "intervention_sensitivity",
            "passed": abs(intervention_delta["delta_R_mean"]) > 0.0001
            and abs(intervention_delta["delta_Phi_eff_mean"]) > 0.0001
            and intervention_delta["changed_agent_count"] > 0,
            "decision_if_failed": "BLOCK",
        },
        {"name": "no_real_data", "passed": no_real_data["passed"], "decision_if_failed": "BLOCK", "findings": no_real_data["findings"]},
        {"name": "jamming_gate", "passed": _jamming_gate_check(), "decision_if_failed": "BLOCK"},
        {
            "name": "auditable_bias_boundary",
            "passed": "auditable_not_absent" in text and all(term not in text for term in ("bias-free", "unbiased", "sin sesgos")),
            "decision_if_failed": "BLOCK",
        },
    ]
    return {
        "schema": DUAT_SMALLVILLE_FALSIFIER_V0_2_SCHEMA,
        "run_id": "DUAT_SMALLVILLE_FALSIFIER_v0_2",
        "passed": all(check["passed"] for check in checks),
        "failed": [check["name"] for check in checks if not check["passed"]],
        "checks": checks,
        "replay": replay,
        "boundary": {
            "uses_real_data": False,
            "uses_network": False,
            "uses_credentials": False,
            "publication_gate": "BLOCK",
        },
    }


def build_metrics_v0_2(
    *,
    seed: int,
    pack: dict[str, Any],
    baseline: dict[str, Any],
    intervention: dict[str, Any],
    delta: dict[str, Any],
    replay: dict[str, Any],
    falsifier: dict[str, Any],
) -> dict[str, Any]:
    summary = summarize_ledger_metrics(intervention)
    metrics = {
        "schema": DUAT_SMALLVILLE_METRICS_SCHEMA,
        "run_id": "DUAT_SMALLVILLE_METRICS_v0_2",
        "seed": seed,
        "agents": intervention["agents"],
        "ticks": intervention["ticks"],
        "events": len(intervention["events"]),
        "hash_chain_valid": verify_v0_2_hash_chain(intervention),
        "replay_verified": replay["replay_verified"],
        "baseline_hash": baseline["fingerprints"]["ledger_sha256"],
        "intervention_hash": intervention["fingerprints"]["ledger_sha256"],
        "R": {
            "R_env_mean": summary["R_env_mean"],
            "R_social_mean": summary["R_social_mean"],
            "R_geologic_mean": summary["R_geologic_mean"],
            "R_weather_mean": summary["R_weather_mean"],
            "R_contradiction_max": summary["R_contradiction_max"],
            "fusion_R_mean": summary["fusion_R_mean"],
            "J_c_proximity_max": summary["J_c_proximity_max"],
        },
        "Phi_eff": {
            "mean": summary["phi_eff_mean"],
            "min": summary["phi_eff_min"],
            "max": summary["phi_eff_max"],
        },
        "gates": summary["gates"],
        "intervention_delta": delta["intervention_delta"],
        "falsifiers": {
            "passed": falsifier["passed"],
            "failed": falsifier["failed"],
            "pass_rate": round((len(falsifier["checks"]) - len(falsifier["failed"])) / max(1, len(falsifier["checks"])), 6),
        },
        "boundary": {
            "uses_real_data": False,
            "uses_network": False,
            "uses_credentials": False,
            "publication_gate": "BLOCK",
        },
    }
    metrics["fingerprint"] = stable_hash(metrics)
    return metrics


__all__ = ["build_metrics_v0_2", "falsify_v0_2", "summarize_ledger_metrics"]
