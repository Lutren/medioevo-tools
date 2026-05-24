"""Calibrated synthetic environment channels and MTS fusion for v0.2."""

from __future__ import annotations

import math
from typing import Any

from .signal_source_pack import CHANNEL_NAMES, clamp01, stable_unit


def channel_snapshot(pack: dict[str, Any], tick: int) -> dict[str, dict[str, Any]]:
    ticks = int(pack["time_model"]["ticks"])
    idx = tick % ticks
    return {name: pack["channels"][name]["series"][idx] for name in CHANNEL_NAMES}


def _risk_from_channel(name: str, values: dict[str, Any]) -> float:
    if name == "weather":
        return clamp01(
            values["heat_stress_index"] * 0.32
            + values["rain_intensity"] * 0.3
            + (1.0 - values["visibility"]) * 0.24
            + values["wind"] * 0.14
        )
    if name == "geophysics":
        return clamp01(
            (1.0 - values["terrain_stability"]) * 0.34
            + values["flood_risk"] * 0.28
            + values["slope_risk"] * 0.22
            + values["microtremor_index"] * 0.16
        )
    if name == "social_pressure":
        return clamp01(
            values["rumor_pressure"] * 0.28
            + (1.0 - values["trust_gradient"]) * 0.28
            + values["conflict_potential"] * 0.28
            + values["crowd_density"] * 0.16
        )
    if name == "infrastructure":
        return clamp01(
            (1.0 - values["power_stability"]) * 0.26
            + (1.0 - values["water_access"]) * 0.24
            + (1.0 - values["road_access"]) * 0.26
            + values["comms_latency"] * 0.24
        )
    if name == "resource_availability":
        return clamp01(
            (1.0 - values["food_access"]) * 0.24
            + (1.0 - values["shelter_access"]) * 0.24
            + (1.0 - values["tool_access"]) * 0.22
            + (1.0 - values["medical_access"]) * 0.3
        )
    raise KeyError(name)


def build_channel_observations(pack: dict[str, Any], tick: int) -> dict[str, dict[str, Any]]:
    snapshot = channel_snapshot(pack, tick)
    observations: dict[str, dict[str, Any]] = {}
    social_risk = _risk_from_channel("social_pressure", snapshot["social_pressure"])
    infra_risk = _risk_from_channel("infrastructure", snapshot["infrastructure"])
    for name in CHANNEL_NAMES:
        contract = dict(pack["channels"][name]["contract"])
        raw_risk = _risk_from_channel(name, snapshot[name])
        contradiction = float(contract.get("contradiction", 0.0))
        if name == "social_pressure" and infra_risk > 0.58 and social_risk < 0.28:
            contradiction = max(contradiction, 0.52)
        if name == "infrastructure" and social_risk > 0.58 and infra_risk < 0.28:
            contradiction = max(contradiction, 0.52)
        r_total = clamp01(raw_risk + float(contract["noise"]) + float(contract["missingness"]) + contradiction * 0.2)
        phi_eff_i = clamp01(float(contract["calibration"]) * math.exp(-1.1 * r_total))
        observations[name] = {
            "values": snapshot[name],
            "latency": contract["latency"],
            "bandwidth": contract["bandwidth"],
            "calibration": contract["calibration"],
            "noise": contract["noise"],
            "missingness": contract["missingness"],
            "contradiction": contradiction,
            "r_total": r_total,
            "phi_eff_i": phi_eff_i,
        }
    return observations


def fuse_environment_channels(observations: dict[str, dict[str, Any]]) -> dict[str, Any]:
    weights: dict[str, float] = {}
    weighted_phi = 0.0
    total_weight = 0.0
    missing_penalty = 0.0
    contradiction_penalty = 0.0
    for name, channel in observations.items():
        weight = clamp01(
            float(channel["phi_eff_i"])
            * float(channel["bandwidth"])
            * float(channel["calibration"])
            * (1.0 - float(channel["r_total"]))
        )
        weights[name] = weight
        weighted_phi += float(channel["phi_eff_i"]) * weight
        total_weight += weight
        missing_penalty += float(channel["missingness"])
        contradiction_penalty = max(contradiction_penalty, float(channel["contradiction"]))
    confidence = clamp01(weighted_phi / total_weight) if total_weight else 0.0
    missing_penalty = clamp01(missing_penalty / max(1, len(observations)))
    fusion_R = clamp01(1.0 - confidence + contradiction_penalty + missing_penalty)
    fusion_phi = clamp01(confidence * math.exp(-1.25 * fusion_R))
    if fusion_R >= 0.85:
        gate = "BLOCK"
        regime = "JAMMING"
    elif contradiction_penalty >= 0.5:
        gate = "REVIEW"
        regime = "PRE_JAMMING" if fusion_R >= 0.45 else "FUNCTIONAL_REVIEW"
    elif fusion_R >= 0.45:
        gate = "REVIEW"
        regime = "PRE_JAMMING"
    else:
        gate = "APPROVE"
        regime = "FUNCTIONAL"
    return {
        "channel_weight_i": weights,
        "confidence": confidence,
        "fusion_R": fusion_R,
        "fusion_Phi_eff": fusion_phi,
        "R_contradiction": clamp01(contradiction_penalty),
        "missing_penalty": missing_penalty,
        "J_c_proximity": clamp01(fusion_R / 0.45),
        "gate": gate,
        "regime": regime,
    }


def agent_environment_state(
    *,
    pack: dict[str, Any],
    tick: int,
    agent: dict[str, Any],
) -> dict[str, Any]:
    observations = build_channel_observations(pack, tick)
    fusion = fuse_environment_channels(observations)
    agent_bias = stable_unit(pack["seed"], tick, agent["agent_id"], "env_bias") * 0.08
    exposure = {
        "weather": clamp01(observations["weather"]["r_total"] + agent_bias),
        "geophysics": clamp01(observations["geophysics"]["r_total"] + agent_bias * 0.5),
        "social_pressure": clamp01(observations["social_pressure"]["r_total"] + agent_bias * 0.8),
        "infrastructure": clamp01(observations["infrastructure"]["r_total"] + agent_bias * 0.6),
        "resources": clamp01(observations["resource_availability"]["r_total"] + agent_bias * 0.4),
    }
    r_env = clamp01((exposure["weather"] + exposure["geophysics"] + exposure["infrastructure"] + exposure["resources"]) / 4)
    r_social = exposure["social_pressure"]
    fusion_R = clamp01(fusion["fusion_R"] * 0.72 + r_env * 0.18 + r_social * 0.1)
    if fusion["R_contradiction"] >= 0.5:
        gate = "REVIEW"
    elif fusion_R >= 0.85:
        gate = "BLOCK"
    elif fusion_R >= 0.45:
        gate = "REVIEW"
    else:
        gate = "APPROVE"
    phi_eff = clamp01(fusion["fusion_Phi_eff"] * math.exp(-0.42 * fusion_R))
    if gate == "BLOCK":
        next_action = "halt_and_request_review"
    elif gate == "REVIEW":
        next_action = "reduce_scope_and_collect_evidence"
    else:
        next_action = "continue_bounded_plan"
    return {
        "environment_exposure": exposure,
        "r_state": {
            "R_env": r_env,
            "R_social": r_social,
            "R_geologic": exposure["geophysics"],
            "R_weather": exposure["weather"],
            "R_contradiction": fusion["R_contradiction"],
            "fusion_R": fusion_R,
        },
        "phi_eff": phi_eff,
        "gate": gate,
        "next_action": next_action,
        "fusion": fusion,
    }


__all__ = [
    "agent_environment_state",
    "build_channel_observations",
    "channel_snapshot",
    "fuse_environment_channels",
]
