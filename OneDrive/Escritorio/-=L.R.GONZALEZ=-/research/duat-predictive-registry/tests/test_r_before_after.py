from __future__ import annotations

from duat_predictive_registry.benchmarking import _benchmark_forecast_gate
from duat_predictive_registry.evaluation import r_from_error


def test_r_before_after_can_show_improvement():
    before = r_from_error(
        normalized_error_value=0.45,
        coverage_value=0.80,
        source_quality=0.50,
        calibration_score_value=0.55,
        temporal_penalty=0.20,
    )
    after = r_from_error(
        normalized_error_value=0.20,
        coverage_value=0.95,
        source_quality=0.80,
        calibration_score_value=0.80,
        temporal_penalty=0.05,
    )
    assert after < before


def test_r_before_after_can_show_worse_result_without_hiding_it():
    before = r_from_error(
        normalized_error_value=0.10,
        coverage_value=0.95,
        source_quality=0.70,
        calibration_score_value=0.90,
        temporal_penalty=0.05,
    )
    after = r_from_error(
        normalized_error_value=0.70,
        coverage_value=0.95,
        source_quality=0.70,
        calibration_score_value=0.30,
        temporal_penalty=0.05,
    )
    gate = _benchmark_forecast_gate(
        r_after=after,
        r_delta=after - before,
        enhanced_mae=7.0,
        baseline_mae=1.0,
        minimum_evidence_passed=True,
        leakage_check="PASS",
        license_terms_scan="PASS",
    )
    assert after > before
    assert gate["forecast_gate"] == "REVIEW"
    assert gate["reason"] == "enhanced_worse_than_selected_baseline"
