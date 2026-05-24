"""Dynamic R/Phi helpers for clean-room runtime experiments."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List

from .core import clamp


class TemperatureProfile(str, Enum):
    EXPLORATION = "EXPLORATION"
    BALANCED = "BALANCED"
    FOCUSED = "FOCUSED"
    CONSTRAINED = "CONSTRAINED"


@dataclass(frozen=True)
class TemperatureConfig:
    temperature: float
    profile: TemperatureProfile
    top_p: float
    reasoning: str

    def to_dict(self) -> dict:
        return {
            "temperature": self.temperature,
            "profile": self.profile.value,
            "top_p": self.top_p,
            "reasoning": self.reasoning,
        }


def compute_temperature(*, r: float, phi_eff: float, task_type: str = "general") -> TemperatureConfig:
    base = 0.95 * ((1.0 - clamp(r, 0.0, 1.0)) ** 1.2)
    modifiers = {
        "creative": 0.10,
        "general": 0.00,
        "plan": -0.12,
        "code": -0.18,
        "factual": -0.25,
    }
    modifier = modifiers.get(task_type.lower(), 0.0)
    temperature = clamp(base + modifier * clamp(phi_eff, 0.0, 1.0), 0.05, 0.95)
    if temperature >= 0.75:
        profile = TemperatureProfile.EXPLORATION
    elif temperature >= 0.50:
        profile = TemperatureProfile.BALANCED
    elif temperature >= 0.25:
        profile = TemperatureProfile.FOCUSED
    else:
        profile = TemperatureProfile.CONSTRAINED
    return TemperatureConfig(
        temperature=round(temperature, 3),
        profile=profile,
        top_p=round(clamp(0.85 + temperature * 0.10, 0.80, 0.95), 3),
        reasoning=f"task={task_type}; temperature decreases as R rises and is capped by task risk",
    )


def compute_r_velocity(r_history: Iterable[float], *, window: int = 3) -> float:
    values: List[float] = [clamp(float(value), 0.0, 1.0) for value in r_history]
    if len(values) < 2:
        return 0.0
    slice_values = values[-max(2, window):]
    return round((slice_values[-1] - slice_values[0]) / (len(slice_values) - 1), 4)


def classify_r_trend(r_history: Iterable[float], *, epsilon: float = 0.01) -> str:
    velocity = compute_r_velocity(r_history)
    if velocity > epsilon:
        return "RISING"
    if velocity < -epsilon:
        return "FALLING"
    return "STABLE"

