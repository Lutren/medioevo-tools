"""Multidimensional R vector utilities."""

from __future__ import annotations

from collections.abc import Mapping

R_DIMENSIONS: tuple[str, ...] = (
    "R_cognitive",
    "R_entertainment",
    "R_social_manipulative",
    "R_temporal",
    "R_source",
    "R_contra",
    "R_sensitive",
    "R_model",
    "R_user_style",
    "R_agent_operational",
)

_DEFAULT_WEIGHTS: dict[str, float] = {
    "R_cognitive": 0.10,
    "R_entertainment": 0.06,
    "R_social_manipulative": 0.12,
    "R_temporal": 0.10,
    "R_source": 0.13,
    "R_contra": 0.12,
    "R_sensitive": 0.20,
    "R_model": 0.10,
    "R_user_style": 0.03,
    "R_agent_operational": 0.04,
}

_TECHNICAL_WEIGHTS: dict[str, float] = {
    **_DEFAULT_WEIGHTS,
    "R_sensitive": 0.24,
    "R_source": 0.15,
    "R_model": 0.13,
    "R_user_style": 0.01,
}

_CREATIVE_WEIGHTS: dict[str, float] = {
    **_DEFAULT_WEIGHTS,
    "R_cognitive": 0.14,
    "R_user_style": 0.10,
    "R_entertainment": 0.08,
    "R_model": 0.05,
    "R_source": 0.09,
}


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def task_weights(task_type: str = "technical") -> dict[str, float]:
    label = task_type.lower().strip()
    if label in {"creative", "explanatory", "narrative", "design"}:
        weights = dict(_CREATIVE_WEIGHTS)
    elif label in {"technical", "critical", "code", "data", "legal", "security", "prediction"}:
        weights = dict(_TECHNICAL_WEIGHTS)
    else:
        weights = dict(_DEFAULT_WEIGHTS)
    total = sum(weights.values())
    return {key: value / total for key, value in weights.items()}


def compute_r_total(
    r_vector: Mapping[str, float],
    task_type: str = "technical",
    override_weights: Mapping[str, float] | None = None,
) -> float:
    """Compute weighted R across known dimensions.

    Unknown dimensions are ignored. Missing dimensions are treated as zero.
    R_sensitive acts as a partial dominance term: if it is high, the final R
    cannot drop below it.
    """

    weights = dict(override_weights or task_weights(task_type))
    weighted = 0.0
    for key in R_DIMENSIONS:
        weighted += clamp01(r_vector.get(key, 0.0)) * weights.get(key, 0.0)
    sensitive = clamp01(r_vector.get("R_sensitive", 0.0))
    return clamp01(max(weighted, sensitive * 0.85))


def empty_r_vector() -> dict[str, float]:
    return {key: 0.0 for key in R_DIMENSIONS}
