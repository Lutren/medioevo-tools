"""Forecast evaluation helpers for DUAT one-step benchmarks."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

from .r_vector import clamp01


def mae(actual: Sequence[float], predicted: Sequence[float]) -> float:
    _check_same_length(actual, predicted)
    return sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual)


def rmse(actual: Sequence[float], predicted: Sequence[float]) -> float:
    _check_same_length(actual, predicted)
    return math.sqrt(sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual))


def mape_if_safe(actual: Sequence[float], predicted: Sequence[float]) -> dict[str, Any]:
    _check_same_length(actual, predicted)
    if any(abs(a) < 1e-9 for a in actual):
        return {"value": None, "reason": "actual_contains_zero"}
    if any(a < 0 for a in actual):
        return {"value": None, "reason": "actual_contains_negative_values"}
    return {
        "value": sum(abs((a - p) / a) for a, p in zip(actual, predicted)) / len(actual),
        "reason": "PASS",
    }


def normalized_error(error: float, values: Sequence[float]) -> float:
    if not values:
        return 1.0
    value_range = max(values) - min(values)
    scale = max(1.0, value_range)
    return clamp01(error / scale)


def r_from_error(
    normalized_error_value: float,
    coverage_value: float,
    source_quality: float,
    calibration_score_value: float,
    temporal_penalty: float,
) -> float:
    """Fallback R_pred used by the benchmark report."""

    return clamp01(
        0.30 * clamp01(normalized_error_value)
        + 0.20 * (1.0 - clamp01(coverage_value))
        + 0.20 * (1.0 - clamp01(source_quality))
        + 0.15 * (1.0 - clamp01(calibration_score_value))
        + 0.15 * clamp01(temporal_penalty)
    )


def metric_bundle(actual: Sequence[float], predicted: Sequence[float]) -> dict[str, Any]:
    return {
        "MAE": mae(actual, predicted),
        "RMSE": rmse(actual, predicted),
        "MAPE_if_safe": mape_if_safe(actual, predicted),
    }


def _check_same_length(actual: Sequence[float], predicted: Sequence[float]) -> None:
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have equal length")
    if not actual:
        raise ValueError("actual and predicted must not be empty")
