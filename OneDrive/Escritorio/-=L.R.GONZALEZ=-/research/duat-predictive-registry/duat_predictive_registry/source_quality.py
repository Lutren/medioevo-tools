"""SourceQuality scoring for DUAT predictive registry."""

from __future__ import annotations

from dataclasses import dataclass

from .r_vector import clamp01


@dataclass(frozen=True)
class SourceQualityInputs:
    provenance_score: float
    license_score: float
    api_stability_score: float
    granularity_score: float
    coverage_score: float
    traceability_score: float
    reproducibility_score: float


DEFAULT_SOURCE_QUALITY_WEIGHTS: dict[str, float] = {
    "provenance_score": 0.18,
    "license_score": 0.16,
    "api_stability_score": 0.14,
    "granularity_score": 0.12,
    "coverage_score": 0.14,
    "traceability_score": 0.14,
    "reproducibility_score": 0.12,
}


def weighted_mean(values: dict[str, float], weights: dict[str, float]) -> float:
    numerator = 0.0
    denominator = 0.0
    for key, weight in weights.items():
        numerator += clamp01(values.get(key, 0.0)) * weight
        denominator += weight
    if denominator == 0:
        return 0.0
    return clamp01(numerator / denominator)


def compute_source_quality(
    scores: SourceQualityInputs | dict[str, float],
    weights: dict[str, float] | None = None,
) -> float:
    if isinstance(scores, SourceQualityInputs):
        values = scores.__dict__
    else:
        values = dict(scores)
    return weighted_mean(values, weights or DEFAULT_SOURCE_QUALITY_WEIGHTS)


def compute_r_source(source_quality: float) -> float:
    return clamp01(1.0 - source_quality)
