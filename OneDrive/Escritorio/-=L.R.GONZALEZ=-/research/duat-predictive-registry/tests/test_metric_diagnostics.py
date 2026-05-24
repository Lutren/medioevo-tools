from __future__ import annotations

from duat_predictive_registry.metric_diagnostics import compare_metric_deltas


def test_metric_diagnostics_improved_when_mae_rmse_improve_and_mape_skipped():
    diagnostics = compare_metric_deltas(
        {"MAE": 2.0, "RMSE": 3.0, "MAPE_if_safe": {"value": None, "reason": "actual_contains_negative_values"}},
        {"MAE": 1.0, "RMSE": 2.0, "MAPE_if_safe": {"value": None, "reason": "actual_contains_negative_values"}},
    )
    assert diagnostics["metrics_improved"] is True
    assert diagnostics["metrics_mixed"] is False
    assert diagnostics["metrics_worse"] is False


def test_metric_diagnostics_worse_when_mae_rmse_worse():
    diagnostics = compare_metric_deltas(
        {"MAE": 1.0, "RMSE": 2.0, "MAPE_if_safe": {"value": 0.10, "reason": "PASS"}},
        {"MAE": 1.2, "RMSE": 2.4, "MAPE_if_safe": {"value": 0.11, "reason": "PASS"}},
    )
    assert diagnostics["metrics_improved"] is False
    assert diagnostics["metrics_worse"] is True
    assert diagnostics["metric_deltas"]["MAE"] > 0
    assert diagnostics["metric_deltas"]["RMSE"] > 0


def test_metric_diagnostics_mixed_when_preferred_metrics_disagree():
    diagnostics = compare_metric_deltas(
        {"MAE": 1.0, "RMSE": 2.0, "MAPE_if_safe": {"value": None, "reason": "actual_contains_zero"}},
        {"MAE": 0.9, "RMSE": 2.2, "MAPE_if_safe": {"value": None, "reason": "actual_contains_zero"}},
    )
    assert diagnostics["metrics_improved"] is False
    assert diagnostics["metrics_mixed"] is True
    assert diagnostics["metrics_worse"] is False
