"""Counterfactual intervention engine for DUAT Smallville v0.2."""

from __future__ import annotations

import copy
from collections import Counter
from typing import Any

from .contracts import DUAT_SMALLVILLE_INTERVENTION_SCHEMA, DUAT_SMALLVILLE_LEDGER_SCHEMA
from .signal_source_pack import DEFAULT_SEED, build_signal_source_pack, clamp01
from .smallville_lab import DEFAULT_AGENT_COUNT, build_smallville_scenario, stable_hash
from .synthetic_environment_channels import agent_environment_state, build_channel_observations, fuse_environment_channels


INTERVENTION_NAMES = ("weather_shock", "social_rumor", "infrastructure_degradation", "geophysical_alert")


def apply_intervention(pack: dict[str, Any], intervention: str = "weather_shock") -> dict[str, Any]:
    if intervention not in INTERVENTION_NAMES:
        raise ValueError(f"unknown intervention: {intervention}")
    mutated = copy.deepcopy(pack)
    ticks = int(mutated["time_model"]["ticks"])
    start = max(1, ticks // 3)
    end = min(ticks, start + min(120, max(2, ticks // 6)))
    for tick in range(start, end):
        if intervention == "weather_shock":
            weather = mutated["channels"]["weather"]["series"][tick]
            infra = mutated["channels"]["infrastructure"]["series"][tick]
            geo = mutated["channels"]["geophysics"]["series"][tick]
            weather["rain_intensity"] = clamp01(weather["rain_intensity"] + 0.62)
            weather["visibility"] = clamp01(weather["visibility"] - 0.42)
            weather["heat_stress_index"] = clamp01(weather["heat_stress_index"] + 0.08)
            infra["road_access"] = clamp01(infra["road_access"] - 0.38)
            infra["comms_latency"] = clamp01(infra["comms_latency"] + 0.24)
            geo["soil_saturation"] = clamp01(geo["soil_saturation"] + 0.46)
            geo["flood_risk"] = clamp01(geo["flood_risk"] + 0.38)
        elif intervention == "social_rumor":
            social = mutated["channels"]["social_pressure"]["series"][tick]
            social["rumor_pressure"] = clamp01(social["rumor_pressure"] + 0.58)
            social["trust_gradient"] = clamp01(social["trust_gradient"] - 0.38)
            social["conflict_potential"] = clamp01(social["conflict_potential"] + 0.34)
            social["invitation_spread_rate"] = clamp01(social["invitation_spread_rate"] + 0.25)
        elif intervention == "infrastructure_degradation":
            infra = mutated["channels"]["infrastructure"]["series"][tick]
            resources = mutated["channels"]["resource_availability"]["series"][tick]
            infra["comms_latency"] = clamp01(infra["comms_latency"] + 0.48)
            infra["power_stability"] = clamp01(infra["power_stability"] - 0.42)
            infra["road_access"] = clamp01(infra["road_access"] - 0.28)
            for key in ("food_access", "shelter_access", "tool_access", "medical_access"):
                resources[key] = clamp01(resources[key] - 0.22)
        elif intervention == "geophysical_alert":
            geo = mutated["channels"]["geophysics"]["series"][tick]
            geo["soil_saturation"] = clamp01(geo["soil_saturation"] + 0.48)
            geo["flood_risk"] = clamp01(geo["flood_risk"] + 0.42)
            geo["terrain_stability"] = clamp01(geo["terrain_stability"] - 0.36)
            geo["microtremor_index"] = clamp01(geo["microtremor_index"] + 0.18)
    mutated["intervention"] = {
        "name": intervention,
        "start_tick": start,
        "end_tick": end,
        "synthetic": True,
        "uses_real_data": False,
    }
    mutated["fingerprint"] = stable_hash(mutated)
    return mutated


def _plan_from_gate(gate: str, agent_role: str) -> str:
    if gate == "BLOCK":
        return "halt_expansion_and_request_review"
    if gate == "REVIEW":
        return "bounded_review_of_environment_signals"
    if agent_role in {"engineer", "observer"}:
        return "inspect_calibrated_signal"
    return "continue_synthetic_daily_plan"


def run_smallville_v0_2(
    *,
    seed: int = DEFAULT_SEED,
    ticks: int = 1440,
    pack: dict[str, Any] | None = None,
    intervention_name: str | None = None,
) -> dict[str, Any]:
    source_pack = pack if pack is not None else build_signal_source_pack(seed=seed, ticks=ticks)
    scenario = build_smallville_scenario(seed=f"duat-smallville-v0-2-{seed}", days=1, ticks_per_day=1, agent_count=DEFAULT_AGENT_COUNT)
    agents = scenario["agents"]
    previous_hash = "GENESIS"
    events: list[dict[str, Any]] = []
    total_ticks = int(source_pack["time_model"]["ticks"])
    for tick in range(total_ticks):
        observations = build_channel_observations(source_pack, tick)
        fusion = fuse_environment_channels(observations)
        agent_states = []
        for agent in agents:
            env_state = agent_environment_state(pack=source_pack, tick=tick, agent=agent)
            gate = env_state["gate"]
            plan = _plan_from_gate(gate, agent["role"])
            agent_states.append(
                {
                    "agent_id": agent["agent_id"],
                    "location_id": agent["home_zone"],
                    "memory_state": {
                        "last_signal_tick": tick,
                        "evidence_mode": "append_only_synthetic",
                    },
                    "plan_state": {
                        "plan": plan,
                        "changed_by_intervention": bool(intervention_name and gate != "APPROVE"),
                    },
                    "environment_exposure": env_state["environment_exposure"],
                    "r_state": env_state["r_state"],
                    "phi_eff": env_state["phi_eff"],
                    "gate": gate,
                    "next_action": env_state["next_action"],
                }
            )
        gate_counts = dict(Counter(state["gate"] for state in agent_states))
        event_body = {
            "tick": tick,
            "previous_hash": previous_hash,
            "channel_summary": {
                name: {
                    "r_total": observations[name]["r_total"],
                    "phi_eff_i": observations[name]["phi_eff_i"],
                    "contradiction": observations[name]["contradiction"],
                }
                for name in observations
            },
            "fusion": fusion,
            "agent_states": agent_states,
            "summary": {
                "gate_counts": {gate: gate_counts.get(gate, 0) for gate in ("APPROVE", "REVIEW", "BLOCK")},
                "fusion_R_mean": round(sum(state["r_state"]["fusion_R"] for state in agent_states) / len(agent_states), 6),
                "phi_eff_mean": round(sum(state["phi_eff"] for state in agent_states) / len(agent_states), 6),
            },
        }
        event_hash = stable_hash(event_body)
        event = dict(event_body)
        event["event_hash"] = event_hash
        events.append(event)
        previous_hash = event_hash
    ledger_body = {
        "schema": DUAT_SMALLVILLE_LEDGER_SCHEMA,
        "schema_version": "v0_2",
        "run_id": "DUAT_SMALLVILLE_CITY_SIM_LAB_v0_2",
        "seed": seed,
        "agents": DEFAULT_AGENT_COUNT,
        "ticks": total_ticks,
        "intervention": intervention_name,
        "signal_source_pack_hash": source_pack["fingerprint"],
        "events": events,
        "boundary": {
            "uses_real_data": False,
            "uses_network": False,
            "uses_credentials": False,
            "publication_gate": "BLOCK",
        },
        "claims": {
            "prediction": "SYNTHETIC_SIMULATION_ONLY",
            "bias": "AUDITABLE_NOT_ABSENT",
            "science": "FALSIFIABLE_LOCAL_LAB_NOT_REAL_WORLD_CLAIM",
        },
    }
    ledger = dict(ledger_body)
    ledger["fingerprints"] = {"ledger_sha256": stable_hash(ledger_body), "last_event_hash": previous_hash}
    return ledger


def compare_intervention(
    baseline: dict[str, Any],
    intervention: dict[str, Any],
    *,
    intervention_name: str = "weather_shock",
) -> dict[str, Any]:
    base_events = baseline["events"]
    int_events = intervention["events"]
    changed_agents = set()
    changed_plans = 0
    delta_r_values = []
    delta_phi_values = []
    for base_event, int_event in zip(base_events, int_events):
        for base_state, int_state in zip(base_event["agent_states"], int_event["agent_states"]):
            delta_r = int_state["r_state"]["fusion_R"] - base_state["r_state"]["fusion_R"]
            delta_phi = int_state["phi_eff"] - base_state["phi_eff"]
            delta_r_values.append(delta_r)
            delta_phi_values.append(delta_phi)
            if abs(delta_r) > 0.0001 or abs(delta_phi) > 0.0001:
                changed_agents.add(int_state["agent_id"])
            if base_state["plan_state"]["plan"] != int_state["plan_state"]["plan"]:
                changed_plans += 1
    delta = {
        "schema": DUAT_SMALLVILLE_INTERVENTION_SCHEMA,
        "run_id": "DUAT_SMALLVILLE_INTERVENTION_DELTA_v0_2",
        "intervention": intervention_name,
        "baseline_hash": baseline["fingerprints"]["ledger_sha256"],
        "intervention_hash": intervention["fingerprints"]["ledger_sha256"],
        "hash_linked": True,
        "intervention_delta": {
            "delta_R_mean": round(sum(delta_r_values) / max(1, len(delta_r_values)), 6),
            "delta_Phi_eff_mean": round(sum(delta_phi_values) / max(1, len(delta_phi_values)), 6),
            "changed_agent_count": len(changed_agents),
            "changed_plan_count": changed_plans,
        },
        "boundary": {
            "uses_real_data": False,
            "uses_network": False,
            "uses_credentials": False,
            "publication_gate": "BLOCK",
        },
    }
    delta["fingerprint"] = stable_hash(delta)
    return delta


def build_baseline_intervention_pair(
    *,
    seed: int = DEFAULT_SEED,
    ticks: int = 1440,
    intervention_name: str = "weather_shock",
) -> dict[str, Any]:
    pack = build_signal_source_pack(seed=seed, ticks=ticks)
    intervention_pack = apply_intervention(pack, intervention_name)
    baseline = run_smallville_v0_2(seed=seed, ticks=ticks, pack=pack)
    intervention = run_smallville_v0_2(seed=seed, ticks=ticks, pack=intervention_pack, intervention_name=intervention_name)
    delta = compare_intervention(baseline, intervention, intervention_name=intervention_name)
    return {"pack": pack, "intervention_pack": intervention_pack, "baseline": baseline, "intervention": intervention, "delta": delta}


__all__ = [
    "INTERVENTION_NAMES",
    "apply_intervention",
    "build_baseline_intervention_pair",
    "compare_intervention",
    "run_smallville_v0_2",
]
