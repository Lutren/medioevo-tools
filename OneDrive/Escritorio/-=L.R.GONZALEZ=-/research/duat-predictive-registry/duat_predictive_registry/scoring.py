"""Predictive scoring formulas for DUAT registry."""

from __future__ import annotations

import math
from collections.abc import Sequence

from .r_vector import clamp01


def freshness(age_days: float, lambda_age: float = 0.03) -> float:
    return clamp01(math.exp(-lambda_age * max(0.0, age_days)))


def coverage(valid_points: int, expected_points: int) -> float:
    if expected_points <= 0:
        return 0.0
    return clamp01(valid_points / expected_points)


def calibration_score(normalized_historical_error: float) -> float:
    return clamp01(1.0 - normalized_historical_error)


def r_pred(
    R_source: float,
    R_missing: float,
    R_temporal: float,
    R_contra: float,
    R_model: float,
) -> float:
    return clamp01(
        0.25 * R_source
        + 0.20 * R_missing
        + 0.20 * R_temporal
        + 0.20 * R_contra
        + 0.15 * R_model
    )


def h_eff_pred(
    H_raw: float,
    SourceQuality: float,
    Freshness: float,
    Coverage: float,
    Phi_eff: float,
    CalibrationScore: float,
    FilterFit: float = 1.0,
) -> float:
    return clamp01(
        H_raw
        * SourceQuality
        * Freshness
        * Coverage
        * Phi_eff
        * CalibrationScore
        * FilterFit
    )


def ensemble_weight(
    historical_error: float,
    R_pred: float,
    age_days: float,
    SourceQuality: float,
    lambda_error: float = 2.0,
    lambda_noise: float = 2.0,
    lambda_age: float = 0.03,
) -> float:
    return math.exp(
        -lambda_error * clamp01(historical_error)
        -lambda_noise * clamp01(R_pred)
        -lambda_age * max(0.0, age_days)
    ) * clamp01(SourceQuality)


def weighted_ensemble(predictions: Sequence[float], weights: Sequence[float]) -> float:
    if len(predictions) != len(weights):
        raise ValueError("predictions and weights must have equal length")
    total_weight = sum(weights)
    if total_weight <= 0:
        raise ValueError("weights must sum to a positive value")
    return sum(pred * weight for pred, weight in zip(predictions, weights)) / total_weight


def bayesian_update(prior: float, likelihood: float, evidence: float) -> float:
    if evidence <= 0:
        raise ValueError("evidence must be positive")
    return clamp01(prior * likelihood / evidence)


def scalar_kalman_gain(P: float, H: float, R: float) -> float:
    denominator = H * P * H + R
    if denominator <= 0:
        raise ValueError("kalman denominator must be positive")
    return P * H / denominator
