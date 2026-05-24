from __future__ import annotations

from duat_predictive_registry.out_of_sample_gate import out_of_sample_gate


def _gate(metric_delta, r_delta=-0.01, **overrides):
    payload = {
        "data_mode": "real_fixture",
        "leakage_check": "PASS",
        "comparability_status": "PASS",
        "license_terms_scan": "PASS",
        "n_outer_folds": 2,
        "metric_delta_outer": metric_delta,
        "r_aligned_delta_outer": r_delta,
    }
    payload.update(overrides)
    return out_of_sample_gate(**payload)


def test_out_of_sample_gate_classifies_metrics_improved():
    result = _gate({"MAE": -0.1, "RMSE": -0.2})
    assert result["oos_classification"] == "OOS_METRICS_IMPROVED"
    assert result["out_of_sample_gate"] == "APPROVE_LOCAL"
    assert result["publication_gate"] == "BLOCK"


def test_out_of_sample_gate_classifies_metrics_worse():
    result = _gate({"MAE": 0.1, "RMSE": 0.2}, r_delta=0.01)
    assert result["oos_classification"] == "OOS_METRICS_WORSE"
    assert result["out_of_sample_gate"] == "REVIEW"


def test_out_of_sample_gate_classifies_r_only_improved():
    result = _gate({"MAE": 0.1, "RMSE": 0.2}, r_delta=-0.01)
    assert result["oos_classification"] == "OOS_R_ONLY_IMPROVED"
    assert result["out_of_sample_gate"] == "REVIEW"


def test_out_of_sample_gate_keeps_publication_block_on_license_review():
    result = _gate({"MAE": -0.1, "RMSE": -0.2}, license_terms_scan="REVIEW")
    assert result["out_of_sample_gate"] == "REVIEW"
    assert result["publication_gate"] == "BLOCK"


def test_out_of_sample_gate_blocks_leakage():
    result = _gate({"MAE": -0.1, "RMSE": -0.2}, leakage_check="BLOCK")
    assert result["oos_classification"] == "OOS_BLOCKED_LEAKAGE"
    assert result["out_of_sample_gate"] == "BLOCK"
