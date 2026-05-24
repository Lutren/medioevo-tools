"""Synthetic local SignalSourcePack for DUAT Smallville v0.2."""

from __future__ import annotations

import math
import re
from typing import Any

from .contracts import DUAT_SIGNAL_SOURCE_PACK_SCHEMA
from .smallville_lab import stable_hash


DEFAULT_SEED = 20260517
DEFAULT_TICK_SECONDS = 10
DEFAULT_TICKS = 1440
CHANNEL_NAMES = (
    "weather",
    "geophysics",
    "social_pressure",
    "infrastructure",
    "resource_availability",
)


def clamp01(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 6)


def stable_unit(seed: int | str, *parts: object) -> float:
    digest = stable_hash({"seed": str(seed), "parts": parts})
    return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)


def _wave(tick: int, period: int, phase: float = 0.0) -> float:
    return (math.sin(((tick / max(1, period)) + phase) * math.tau) + 1.0) / 2.0


def _channel_contract(latency: int, bandwidth: float, calibration: float, noise: float) -> dict[str, float]:
    return {
        "latency": latency,
        "bandwidth": round(bandwidth, 6),
        "calibration": round(calibration, 6),
        "noise": round(noise, 6),
        "missingness": 0.0,
        "contradiction": 0.0,
    }


def _weather(seed: int, tick: int) -> dict[str, float]:
    day = _wave(tick, 144, 0.0)
    wet = _wave(tick, 360, 0.15)
    noise = stable_unit(seed, tick, "weather") - 0.5
    temperature = 18.0 + 13.0 * day + noise * 2.0
    humidity = clamp01(0.42 + wet * 0.42 + noise * 0.05)
    rain = clamp01(max(0.0, wet - 0.58) * 1.8 + max(0.0, noise) * 0.08)
    wind = clamp01(0.18 + _wave(tick, 96, 0.31) * 0.34 + abs(noise) * 0.12)
    visibility = clamp01(1.0 - rain * 0.52 - humidity * 0.12)
    heat = clamp01((temperature - 24.0) / 15.0 + humidity * 0.18)
    return {
        "temperature": round(temperature, 3),
        "humidity": humidity,
        "wind": wind,
        "rain_intensity": rain,
        "visibility": visibility,
        "heat_stress_index": heat,
    }


def _geophysics(seed: int, tick: int, weather: dict[str, float]) -> dict[str, float]:
    micro = clamp01(0.05 + stable_unit(seed, tick, "microtremor") * 0.12)
    saturation = clamp01(0.18 + weather["rain_intensity"] * 0.58 + _wave(tick, 480, 0.2) * 0.09)
    flood = clamp01(weather["rain_intensity"] * 0.72 + saturation * 0.24)
    slope = clamp01(saturation * 0.42 + micro * 0.24)
    stability = clamp01(1.0 - (micro * 0.35 + saturation * 0.22 + slope * 0.3))
    return {
        "terrain_stability": stability,
        "microtremor_index": micro,
        "flood_risk": flood,
        "slope_risk": slope,
        "soil_saturation": saturation,
    }


def _social_pressure(seed: int, tick: int) -> dict[str, float]:
    pulse = _wave(tick, 240, 0.42)
    noise = stable_unit(seed, tick, "social") - 0.5
    crowd = clamp01(0.22 + pulse * 0.42 + max(0.0, noise) * 0.12)
    rumor = clamp01(0.14 + _wave(tick, 300, 0.61) * 0.34 + max(0.0, noise) * 0.2)
    trust = clamp01(0.72 - rumor * 0.28 + (stable_unit(seed, tick, "trust") - 0.5) * 0.06)
    conflict = clamp01(rumor * 0.42 + crowd * 0.22 + (1.0 - trust) * 0.26)
    spread = clamp01(rumor * 0.5 + crowd * 0.24)
    return {
        "crowd_density": crowd,
        "rumor_pressure": rumor,
        "trust_gradient": trust,
        "conflict_potential": conflict,
        "invitation_spread_rate": spread,
    }


def _infrastructure(seed: int, tick: int, weather: dict[str, float]) -> dict[str, float]:
    base_noise = stable_unit(seed, tick, "infra") - 0.5
    power = clamp01(0.88 - weather["wind"] * 0.11 - weather["rain_intensity"] * 0.13 + base_noise * 0.04)
    water = clamp01(0.84 - weather["rain_intensity"] * 0.05 + _wave(tick, 720, 0.12) * 0.04)
    road = clamp01(0.9 - weather["rain_intensity"] * 0.34 - (1.0 - weather["visibility"]) * 0.12)
    comms = clamp01(0.12 + (1.0 - power) * 0.46 + weather["wind"] * 0.18)
    return {
        "power_stability": power,
        "water_access": water,
        "road_access": road,
        "comms_latency": comms,
    }


def _resources(seed: int, tick: int, infrastructure: dict[str, float]) -> dict[str, float]:
    drift = (stable_unit(seed, tick, "resources") - 0.5) * 0.04
    transport = infrastructure["road_access"]
    water = infrastructure["water_access"]
    power = infrastructure["power_stability"]
    return {
        "food_access": clamp01(0.82 * transport + 0.1 + drift),
        "shelter_access": clamp01(0.86 * power + 0.08),
        "tool_access": clamp01(0.72 * transport + 0.18 * power + drift),
        "medical_access": clamp01(0.58 * transport + 0.24 * power + 0.12 * water),
    }


def build_signal_source_pack(
    *,
    seed: int = DEFAULT_SEED,
    ticks: int = DEFAULT_TICKS,
    tick_seconds: int = DEFAULT_TICK_SECONDS,
) -> dict[str, Any]:
    if ticks < 1:
        raise ValueError("ticks must be >= 1")
    series = {name: [] for name in CHANNEL_NAMES}
    for tick in range(ticks):
        weather = _weather(seed, tick)
        geophysics = _geophysics(seed, tick, weather)
        social = _social_pressure(seed, tick)
        infrastructure = _infrastructure(seed, tick, weather)
        resources = _resources(seed, tick, infrastructure)
        series["weather"].append({"tick": tick, **weather})
        series["geophysics"].append({"tick": tick, **geophysics})
        series["social_pressure"].append({"tick": tick, **social})
        series["infrastructure"].append({"tick": tick, **infrastructure})
        series["resource_availability"].append({"tick": tick, **resources})

    channels = {
        "weather": {"contract": _channel_contract(2, 0.86, 0.91, 0.08), "series": series["weather"]},
        "geophysics": {"contract": _channel_contract(5, 0.74, 0.88, 0.07), "series": series["geophysics"]},
        "social_pressure": {"contract": _channel_contract(1, 0.68, 0.82, 0.12), "series": series["social_pressure"]},
        "infrastructure": {"contract": _channel_contract(3, 0.78, 0.9, 0.06), "series": series["infrastructure"]},
        "resource_availability": {"contract": _channel_contract(4, 0.72, 0.86, 0.08), "series": series["resource_availability"]},
    }
    pack = {
        "schema": DUAT_SIGNAL_SOURCE_PACK_SCHEMA,
        "pack_id": "duat_signal_source_pack_v0_2",
        "seed": seed,
        "time_model": {"tick_seconds": tick_seconds, "ticks": ticks},
        "channels": channels,
        "boundary": {
            "uses_real_data": False,
            "uses_credentials": False,
            "uses_network": False,
            "publication_gate": "BLOCK",
            "data_claim": "SYNTHETIC_ONLY",
        },
    }
    pack["fingerprint"] = stable_hash(pack)
    return pack


def assert_no_real_data_or_credentials(pack: dict[str, Any]) -> dict[str, Any]:
    serialized = repr(pack).lower()
    forbidden_patterns = {
        "url": re.compile(r"https?://|www\."),
        "key_value": re.compile(r"(api[_-]?key|token|password|secret)\s*[:=]\s*[a-z0-9_./+=-]{8,}", re.I),
        "private_path": re.compile(r"[a-z]:\\users\\|/users/|/home/"),
        "coordinates": re.compile(r"\b(lat|latitude|lon|longitude)\b\s*[:=]"),
        "absolute_bias_claim": re.compile(r"\b(bias-free|unbiased|sin sesgos absolutos|sin sesgos)\b", re.I),
    }
    findings = [name for name, pattern in forbidden_patterns.items() if pattern.search(serialized)]
    boundary = pack.get("boundary", {})
    if boundary.get("uses_real_data") is not False:
        findings.append("uses_real_data_not_false")
    if boundary.get("uses_credentials") is not False:
        findings.append("uses_credentials_not_false")
    if boundary.get("uses_network") is not False:
        findings.append("uses_network_not_false")
    return {"passed": not findings, "findings": findings, "values_printed": False}


__all__ = [
    "CHANNEL_NAMES",
    "DEFAULT_SEED",
    "DEFAULT_TICKS",
    "assert_no_real_data_or_credentials",
    "build_signal_source_pack",
    "clamp01",
    "stable_unit",
]
