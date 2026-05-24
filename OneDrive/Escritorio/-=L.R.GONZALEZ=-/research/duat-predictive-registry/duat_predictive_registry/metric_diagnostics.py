"""Metric comparison helpers for DUAT domain calibration."""

from __future__ import annotations

from typing import Any


EPSILON = 1e-9


def metric_value(metrics: dict[str, Any], metric_name: str) -> float | None:
    """Extract a metric value, including nested MAPE_if_safe values."""

    value = metrics.get(metric_name)
    if isinstance(value, dict):
        nested = value.get("value")
        return float(nested) if isinstance(nested, (int, float)) else None
    return float(value) if isinstance(value, (int, float)) else None


def metric_status(delta: float | None, epsilon: float = EPSILON) -> str:
    """Return IMPROVED, SAME, WORSE or SKIPPED for an error metric delta."""

    if delta is None:
        return "SKIPPED"
    if delta < -epsilon:
        return "IMPROVED"
    if delta > epsilon:
        return "WORSE"
    return "SAME"


def compare_metric_deltas(
    baseline_metrics: dict[str, Any],
    enhanced_metrics: dict[str, Any],
    epsilon: float = EPSILON,
) -> dict[str, Any]:
    """Compare enhanced error metrics against the selected baseline."""

    deltas: dict[str, Any] = {}
    statuses: dict[str, str] = {}
    for metric in ("MAE", "RMSE", "MAPE_if_safe"):
        baseline = metric_value(baseline_metrics, metric)
        enhanced = metric_value(enhanced_metrics, metric)
        delta = None if baseline is None or enhanced is None else enhanced - baseline
        deltas[metric] = delta
        statuses[metric] = metric_status(delta, epsilon)

    mae_status = statuses["MAE"]
    rmse_status = statuses["RMSE"]
    mape_status = statuses["MAPE_if_safe"]
    preferred = [mae_status, rmse_status]
    preferred_improved = all(status == "IMPROVED" for status in preferred)
    preferred_worse = all(status == "WORSE" for status in preferred)
    preferred_disagree = len(set(preferred)) > 1

    metrics_improved = preferred_improved and mape_status in {"IMPROVED", "SKIPPED", "SAME"}
    metrics_worse = preferred_worse
    metrics_mixed = not metrics_improved and not metrics_worse
    if preferred_disagree:
        metrics_mixed = True
    if "SAME" in preferred:
        metrics_mixed = True

    return {
        "metric_deltas": deltas,
        "metric_status": statuses,
        "metrics_improved": metrics_improved,
        "metrics_mixed": metrics_mixed,
        "metrics_worse": metrics_worse,
        "mape_status": mape_status,
        "epsilon": epsilon,
    }


def explain_metric_diagnostics(diagnostics: dict[str, Any]) -> str:
    """Create a short deterministic explanation for report output."""

    statuses = diagnostics.get("metric_status", {})
    return (
        f"MAE={statuses.get('MAE')}, RMSE={statuses.get('RMSE')}, "
        f"MAPE_if_safe={statuses.get('MAPE_if_safe')}"
    )
