"""Deterministic DUAT/Smallville-style synthetic simulation lab.

This module is intentionally CPU-only and synthetic. It creates a local,
auditable agent sandbox without claiming public prediction, ranking, causality
or validated social science.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from typing import Any

from .contracts import (
    DUAT_SMALLVILLE_FALSIFIER_SCHEMA,
    DUAT_SMALLVILLE_LEDGER_SCHEMA,
    DUAT_SMALLVILLE_SCENARIO_SCHEMA,
)


DEFAULT_AGENT_COUNT = 25
DEFAULT_DAYS = 2
DEFAULT_TICKS_PER_DAY = 6

ZONE_IDS = (
    "plaza",
    "clinic",
    "school",
    "market",
    "observatory",
    "waterworks",
    "hillside",
)

ROLE_IDS = (
    "organizer",
    "teacher",
    "medic",
    "artisan",
    "observer",
    "farmer",
    "engineer",
    "courier",
)


@dataclass(frozen=True)
class SmallvilleConfig:
    seed: str = "duat-smallville-v0-1"
    days: int = DEFAULT_DAYS
    ticks_per_day: int = DEFAULT_TICKS_PER_DAY
    agent_count: int = DEFAULT_AGENT_COUNT


def stable_hash(payload: Any) -> str:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _unit(seed: str, *parts: object) -> float:
    digest = stable_hash({"seed": seed, "parts": parts})
    return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)


def _bounded(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return round(max(low, min(high, value)), 6)


def _agent(seed: str, index: int) -> dict[str, Any]:
    role = ROLE_IDS[index % len(ROLE_IDS)]
    return {
        "agent_id": f"agent_{index:02d}",
        "synthetic_identity": f"synthetic_{role}_{index:02d}",
        "role": role,
        "home_zone": ZONE_IDS[index % len(ZONE_IDS)],
        "traits": {
            "curiosity": _bounded(0.25 + _unit(seed, index, "curiosity") * 0.65),
            "caution": _bounded(0.2 + _unit(seed, index, "caution") * 0.7),
            "cooperation": _bounded(0.3 + _unit(seed, index, "cooperation") * 0.6),
            "routine_need": _bounded(0.2 + _unit(seed, index, "routine_need") * 0.65),
            "stress_resilience": _bounded(0.25 + _unit(seed, index, "stress_resilience") * 0.65),
        },
    }


def build_smallville_scenario(
    *,
    seed: str = "duat-smallville-v0-1",
    days: int = DEFAULT_DAYS,
    ticks_per_day: int = DEFAULT_TICKS_PER_DAY,
    agent_count: int = DEFAULT_AGENT_COUNT,
) -> dict[str, Any]:
    if agent_count != DEFAULT_AGENT_COUNT:
        raise ValueError("v0.1 requires exactly 25 synthetic agents")
    if days < 1:
        raise ValueError("days must be >= 1")
    if ticks_per_day < 1:
        raise ValueError("ticks_per_day must be >= 1")

    agents = [_agent(seed, index) for index in range(agent_count)]
    zones = [
        {"zone_id": zone_id, "function": function, "capacity_pressure": _bounded(0.2 + i * 0.08)}
        for i, (zone_id, function) in enumerate(
            zip(
                ZONE_IDS,
                (
                    "coordination",
                    "care",
                    "learning",
                    "exchange",
                    "observation",
                    "infrastructure",
                    "geology",
                ),
            )
        )
    ]
    scenario = {
        "schema": DUAT_SMALLVILLE_SCENARIO_SCHEMA,
        "scenario_id": "duat_smallville_city_v0_1",
        "seed": seed,
        "synthetic": True,
        "agent_count": agent_count,
        "clock": {
            "start_date": "2026-05-17",
            "days": days,
            "ticks_per_day": ticks_per_day,
            "total_ticks": days * ticks_per_day,
            "rotation_minutes": 1440,
            "translation_model": "deterministic_day_of_year_phase_only",
        },
        "zones": zones,
        "agents": agents,
        "parameter_domains": [
            "climate",
            "social",
            "geological",
            "atmospheric_pressure",
            "rotation",
            "translation",
            "media_events",
        ],
        "source_policy": {
            "fixtures": "SYNTHETIC_ONLY",
            "real_sources": "REVIEW_SOURCE_CARD_REQUIRED",
            "publication_gate": "BLOCK",
        },
    }
    return scenario


def _environment(seed: str, tick: int, total_ticks: int, ticks_per_day: int) -> dict[str, Any]:
    day_fraction = (tick % ticks_per_day) / max(1, ticks_per_day)
    seasonal_phase = 137.0 / 365.2422
    daylight = max(0.0, math.sin(day_fraction * math.tau))
    translation_wave = math.sin(seasonal_phase * math.tau)
    weather_noise = (_unit(seed, tick, "weather") - 0.5) * 2.0
    social_noise = (_unit(seed, tick, "social") - 0.5) * 2.0
    geological_noise = _unit(seed, tick, "geology")
    media_event_pressure = _bounded(0.22 + 0.25 * max(0.0, social_noise) + 0.08 * tick / max(1, total_ticks))
    return {
        "tick": tick,
        "climate": {
            "temperature_c": round(21.0 + 5.5 * translation_wave + 3.5 * daylight + weather_noise, 3),
            "humidity_pct": round(52.0 + 18.0 * math.cos((day_fraction + 0.2) * math.tau) + weather_noise * 2.0, 3),
            "precipitation_mm": round(max(0.0, weather_noise - 0.1) * 4.0, 3),
            "wind_speed_mps": round(2.2 + abs(weather_noise) * 2.5, 3),
        },
        "atmospheric_pressure": {
            "pressure_hpa": round(1012.0 + math.cos((day_fraction + seasonal_phase) * math.tau) * 7.0, 3)
        },
        "geological": {
            "seismic_background": _bounded(0.03 + geological_noise * 0.09),
            "soil_saturation": _bounded(0.2 + max(0.0, weather_noise) * 0.35),
        },
        "orbital": {
            "rotation_phase": round(day_fraction, 6),
            "translation_phase": round(seasonal_phase, 6),
            "daylight_factor": round(daylight, 6),
        },
        "social": {
            "media_event_pressure": media_event_pressure,
            "mobility_pressure": _bounded(0.35 + daylight * 0.4 + social_noise * 0.12),
            "resource_stress": _bounded(0.25 + media_event_pressure * 0.25 + max(0.0, weather_noise) * 0.18),
        },
    }


def _pressure_vector(environment: dict[str, Any]) -> dict[str, float]:
    climate = environment["climate"]
    pressure = environment["atmospheric_pressure"]["pressure_hpa"]
    geological = environment["geological"]
    social = environment["social"]
    climate_pressure = (
        abs(climate["temperature_c"] - 22.0) / 32.0
        + abs(pressure - 1013.0) / 90.0
        + climate["precipitation_mm"] / 18.0
        + climate["wind_speed_mps"] / 35.0
    )
    return {
        "climate": _bounded(climate_pressure),
        "social": _bounded(social["media_event_pressure"] * 0.55 + social["resource_stress"] * 0.45),
        "geological": _bounded(geological["seismic_background"] * 0.7 + geological["soil_saturation"] * 0.3),
        "mobility": _bounded(social["mobility_pressure"]),
    }


def _choose_plan(role: str, pressure: dict[str, float], residue: float) -> str:
    dominant = max(pressure, key=lambda key: pressure[key])
    if residue >= 0.68:
        return "request_human_review"
    if dominant == "climate":
        return "stabilize_weather_routine" if role not in ("engineer", "observer") else "inspect_climate_signal"
    if dominant == "geological":
        return "inspect_infrastructure" if role in ("engineer", "courier") else "move_to_safe_zone"
    if dominant == "social":
        return "coordinate_public_message" if role in ("organizer", "teacher") else "reduce_information_noise"
    return "continue_local_task"


def _reflection(agent: dict[str, Any], plan: str, residue: float, trust: float) -> str:
    if plan == "request_human_review":
        return f"{agent['agent_id']} holds action; residue is high and needs review."
    if trust < 0.42:
        return f"{agent['agent_id']} narrows scope and asks for corroborating evidence."
    return f"{agent['agent_id']} keeps plan bounded to synthetic evidence."


def _step_agent(
    *,
    seed: str,
    tick: int,
    agent: dict[str, Any],
    previous: dict[str, float],
    pressure: dict[str, float],
) -> dict[str, Any]:
    traits = agent["traits"]
    role_bias = 0.08 if agent["role"] in ("observer", "engineer", "medic") else 0.03
    sensitivity = 0.35 + traits["curiosity"] * 0.22 + traits["caution"] * 0.18
    resilience = traits["stress_resilience"]
    weighted_pressure = (
        pressure["climate"] * 0.25
        + pressure["social"] * 0.34
        + pressure["geological"] * 0.19
        + pressure["mobility"] * 0.12
        + role_bias
    )
    noise = (_unit(seed, tick, agent["agent_id"], "update") - 0.5) * 0.025
    residue = _bounded(previous["residue"] * 0.66 + weighted_pressure * sensitivity * 0.34 + noise)
    trust = _bounded(previous["trust"] * 0.82 + traits["cooperation"] * 0.13 + (1.0 - pressure["social"]) * 0.08 - residue * 0.08)
    phi_eff = _bounded(1.0 - residue * (0.75 + (1.0 - resilience) * 0.2))
    plan = _choose_plan(agent["role"], pressure, residue)
    return {
        "agent_id": agent["agent_id"],
        "zone": agent["home_zone"],
        "residue": residue,
        "trust": trust,
        "phi_eff": phi_eff,
        "plan": plan,
        "reflection": _reflection(agent, plan, residue, trust),
    }


def verify_hash_chain(ledger: dict[str, Any]) -> bool:
    previous_hash = "GENESIS"
    for event in ledger.get("events", []):
        observed_hash = event.get("event_hash")
        body = {key: value for key, value in event.items() if key != "event_hash"}
        if body.get("previous_hash") != previous_hash:
            return False
        if stable_hash(body) != observed_hash:
            return False
        previous_hash = observed_hash
    return previous_hash == ledger.get("fingerprints", {}).get("last_event_hash")


def run_smallville_duat_lab(
    *,
    seed: str = "duat-smallville-v0-1",
    days: int = DEFAULT_DAYS,
    ticks_per_day: int = DEFAULT_TICKS_PER_DAY,
    agent_count: int = DEFAULT_AGENT_COUNT,
) -> dict[str, Any]:
    scenario = build_smallville_scenario(
        seed=seed,
        days=days,
        ticks_per_day=ticks_per_day,
        agent_count=agent_count,
    )
    config = SmallvilleConfig(seed=seed, days=days, ticks_per_day=ticks_per_day, agent_count=agent_count)
    previous_states = {
        agent["agent_id"]: {
            "residue": _bounded(0.18 + _unit(seed, agent["agent_id"], "residue") * 0.14),
            "trust": _bounded(0.58 + _unit(seed, agent["agent_id"], "trust") * 0.16),
        }
        for agent in scenario["agents"]
    }
    events: list[dict[str, Any]] = []
    previous_hash = "GENESIS"
    total_ticks = days * ticks_per_day
    for tick in range(total_ticks):
        environment = _environment(seed, tick, total_ticks, ticks_per_day)
        pressure = _pressure_vector(environment)
        agent_states = [
            _step_agent(
                seed=seed,
                tick=tick,
                agent=agent,
                previous=previous_states[agent["agent_id"]],
                pressure=pressure,
            )
            for agent in scenario["agents"]
        ]
        for state in agent_states:
            previous_states[state["agent_id"]] = {"residue": state["residue"], "trust": state["trust"]}

        plan_counts = dict(sorted(Counter(state["plan"] for state in agent_states).items()))
        avg_residue = round(sum(state["residue"] for state in agent_states) / agent_count, 6)
        avg_trust = round(sum(state["trust"] for state in agent_states) / agent_count, 6)
        avg_phi_eff = round(sum(state["phi_eff"] for state in agent_states) / agent_count, 6)
        dominant_pressure = max(pressure, key=lambda key: pressure[key])
        event_body = {
            "tick": tick,
            "previous_hash": previous_hash,
            "environment": environment,
            "pressure_vector": pressure,
            "summary": {
                "avg_residue": avg_residue,
                "avg_trust": avg_trust,
                "avg_phi_eff": avg_phi_eff,
                "dominant_pressure": dominant_pressure,
                "plans": plan_counts,
            },
            "agent_states": agent_states,
        }
        event_hash = stable_hash(event_body)
        event = dict(event_body)
        event["event_hash"] = event_hash
        events.append(event)
        previous_hash = event_hash

    final_states = events[-1]["agent_states"] if events else []
    ledger_body = {
        "schema": DUAT_SMALLVILLE_LEDGER_SCHEMA,
        "run_id": "DUAT_SMALLVILLE_CITY_SIM_LAB_v0_1",
        "config": config.__dict__,
        "scenario": scenario,
        "events": events,
        "final_state": {
            "agent_count": agent_count,
            "avg_residue": round(sum(state["residue"] for state in final_states) / agent_count, 6),
            "avg_trust": round(sum(state["trust"] for state in final_states) / agent_count, 6),
            "avg_phi_eff": round(sum(state["phi_eff"] for state in final_states) / agent_count, 6),
        },
        "gates": {
            "ActionGate": "APPROVE_LOCAL_ONLY",
            "ForecastGate": "REVIEW_INTERNAL_ONLY",
            "RemoteComputeGate": "REVIEW_FOR_EXTERNAL_RUNTIME",
            "publication_gate": "BLOCK",
        },
        "claims": {
            "data": "SYNTHETIC_ONLY",
            "public_prediction": "NOT_ALLOWED",
            "ranking": "NOT_ALLOWED",
            "causality": "NOT_CLAIMED",
            "bias": "AUDITABLE_NOT_ABSENT",
            "private_engineering": "EXCLUDED",
        },
        "external_publication": False,
    }
    ledger_fingerprint = stable_hash(ledger_body)
    ledger = dict(ledger_body)
    ledger["fingerprints"] = {
        "ledger_sha256": ledger_fingerprint,
        "scenario_sha256": stable_hash(scenario),
        "last_event_hash": previous_hash,
    }
    return ledger


def falsify_smallville_run(ledger: dict[str, Any]) -> dict[str, Any]:
    config = ledger.get("config", {})
    recomputed = run_smallville_duat_lab(
        seed=config.get("seed", "duat-smallville-v0-1"),
        days=int(config.get("days", DEFAULT_DAYS)),
        ticks_per_day=int(config.get("ticks_per_day", DEFAULT_TICKS_PER_DAY)),
        agent_count=int(config.get("agent_count", DEFAULT_AGENT_COUNT)),
    )
    serialized = json.dumps(ledger, ensure_ascii=False).lower()
    private_markers = ("metaevo", "tcg", "game_bridge", ".env", "api_key", "secret", "token")
    values = [
        state
        for event in ledger.get("events", [])
        for state in event.get("agent_states", [])
    ]
    bounded = all(
        0.0 <= float(state.get("residue", -1.0)) <= 1.0
        and 0.0 <= float(state.get("trust", -1.0)) <= 1.0
        and 0.0 <= float(state.get("phi_eff", -1.0)) <= 1.0
        for state in values
    )
    checks = [
        {
            "name": "deterministic_replay",
            "passed": ledger.get("fingerprints", {}).get("ledger_sha256") == recomputed.get("fingerprints", {}).get("ledger_sha256"),
            "decision_if_failed": "BLOCK",
        },
        {
            "name": "hash_chain",
            "passed": verify_hash_chain(ledger),
            "decision_if_failed": "BLOCK",
        },
        {
            "name": "smallville_agent_count",
            "passed": ledger.get("scenario", {}).get("agent_count") == DEFAULT_AGENT_COUNT,
            "decision_if_failed": "REVIEW",
        },
        {
            "name": "bounded_state",
            "passed": bounded,
            "decision_if_failed": "BLOCK",
        },
        {
            "name": "private_boundary",
            "passed": not any(marker in serialized for marker in private_markers),
            "decision_if_failed": "BLOCK",
        },
        {
            "name": "publication_gate",
            "passed": ledger.get("gates", {}).get("publication_gate") == "BLOCK" and ledger.get("external_publication") is False,
            "decision_if_failed": "BLOCK",
        },
        {
            "name": "bias_claim_boundary",
            "passed": ledger.get("claims", {}).get("bias") == "AUDITABLE_NOT_ABSENT",
            "decision_if_failed": "BLOCK",
        },
    ]
    return {
        "schema": DUAT_SMALLVILLE_FALSIFIER_SCHEMA,
        "run_id": ledger.get("run_id"),
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
        "publication_gate": "BLOCK",
    }


__all__ = [
    "DEFAULT_AGENT_COUNT",
    "build_smallville_scenario",
    "falsify_smallville_run",
    "run_smallville_duat_lab",
    "stable_hash",
    "verify_hash_chain",
]
