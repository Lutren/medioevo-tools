from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from duat_predictive_registry.benchmark_matrix import RUN_ID_V0_4, run_benchmark_matrix
from duat_predictive_registry.domain_calibration import calibrate_matrix
from duat_predictive_registry.metric_aligned_r import (
    RUN_ID,
    build_metric_aligned_report,
    compute_metric_aligned_r,
    validate_metric_aligned_report,
    write_metric_aligned_markdown,
)
from duat_predictive_registry.objectives import find_workspace_root


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = find_workspace_root(ROOT)
ECONOMY = ROOT / "fixtures" / "duat_first_predictive_objective_v0_1.json"
LABOR = ROOT / "fixtures" / "duat_labor_market_unemployment_objective_v0_1.json"
THIRD = ROOT / "fixtures" / "duat_non_economic_third_indicator_objective_v0_1.json"


def test_metric_aligned_r_preserves_operational_r():
    result = compute_metric_aligned_r(
        r_before=0.30,
        r_after=0.20,
        baseline_metrics={"MAE": 2.0, "RMSE": 3.0, "MAPE_if_safe": {"value": None}},
        enhanced_metrics={"MAE": 1.8, "RMSE": 3.3, "MAPE_if_safe": {"value": None}},
        domain="economy",
        comparability_status="REVIEW",
        license_terms_scan="REVIEW",
        leakage_check="PASS",
    )
    assert result["r_operational_before"] == 0.30
    assert result["r_operational_after"] == 0.20
    assert result["r_operational_delta"] == -0.09999999999999998
    assert result["publication_gate"] == "BLOCK"


def test_metric_aligned_r_applies_floor_when_mae_and_rmse_worsen():
    result = compute_metric_aligned_r(
        r_before=0.30,
        r_after=0.20,
        baseline_metrics={"MAE": 2.0, "RMSE": 3.0, "MAPE_if_safe": 0.20},
        enhanced_metrics={"MAE": 2.2, "RMSE": 3.4, "MAPE_if_safe": 0.25},
        domain="labor_market",
        comparability_status="PASS",
        license_terms_scan="PASS",
        leakage_check="PASS",
    )
    assert result["metric_status"] == "WORSE"
    assert result["alignment_floor_applied"] is True
    assert result["r_after_aligned"] >= result["r_operational_before"]
    assert result["r_delta_aligned"] >= 0
    assert result["predictive_claim_gate"] == "REVIEW"


def test_metric_aligned_r_reviews_mixed_metrics():
    result = compute_metric_aligned_r(
        r_before=0.30,
        r_after=0.20,
        baseline_metrics={"MAE": 2.0, "RMSE": 3.0, "MAPE_if_safe": {"value": None}},
        enhanced_metrics={"MAE": 1.5, "RMSE": 3.3, "MAPE_if_safe": {"value": None}},
        domain="economy",
        comparability_status="PASS",
        license_terms_scan="PASS",
        leakage_check="PASS",
    )
    assert result["metric_status"] == "MIXED"
    assert result["predictive_claim_gate"] == "REVIEW"


def test_metric_aligned_r_approves_local_only_when_metrics_improve_and_gates_pass():
    result = compute_metric_aligned_r(
        r_before=0.30,
        r_after=0.20,
        baseline_metrics={"MAE": 2.0, "RMSE": 3.0, "MAPE_if_safe": {"value": None}},
        enhanced_metrics={"MAE": 1.5, "RMSE": 2.3, "MAPE_if_safe": {"value": None}},
        domain="economy",
        comparability_status="PASS",
        license_terms_scan="PASS",
        leakage_check="PASS",
    )
    assert result["metric_status"] == "IMPROVED"
    assert result["predictive_claim_gate"] == "APPROVE_LOCAL"
    assert result["publication_gate"] == "BLOCK"


def test_metric_aligned_report_validates_three_objectives_and_markdown_boundary(tmp_path):
    matrix = run_benchmark_matrix([ECONOMY, LABOR, THIRD], WORKSPACE_ROOT, run_id=RUN_ID_V0_4, schema="duat.benchmark_matrix.v0_4")
    calibration = calibrate_matrix(matrix, WORKSPACE_ROOT)
    report = build_metric_aligned_report(calibration, matrix)
    assert report["run_id"] == RUN_ID
    assert validate_metric_aligned_report(report) == []
    assert report["publication_gate"] == "BLOCK"
    assert report["summary"]["alignment_floor_applied_count"] == 2
    labor = next(item for item in report["objectives"] if item["indicator"] == "labor_market.unemployment_rate.total")
    assert labor["alignment_classification"] == "METRIC_DEGRADED_NO_PREDICTIVE_CLAIM"
    md_path = tmp_path / "metric-aligned.md"
    write_metric_aligned_markdown(report, md_path)
    assert "R reduction does not equal predictive validation" in md_path.read_text(encoding="utf-8")


def test_metric_aligned_schema_shape():
    schema = json.loads((ROOT / "schemas" / "duat_metric_aligned_r_v0_5.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["publication_gate"]["const"] == "BLOCK"
    assert schema["properties"]["objectives"]["items"]["properties"]["predictive_claim_gate"]["enum"] == [
        "APPROVE_LOCAL",
        "REVIEW",
        "BLOCK",
    ]


def test_cli_metric_align_r_generates_json(tmp_path):
    matrix = run_benchmark_matrix([ECONOMY, LABOR, THIRD], WORKSPACE_ROOT, run_id=RUN_ID_V0_4, schema="duat.benchmark_matrix.v0_4")
    calibration = calibrate_matrix(matrix, WORKSPACE_ROOT)
    matrix_path = tmp_path / "matrix.json"
    calibration_path = tmp_path / "calibration.json"
    matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
    calibration_path.write_text(json.dumps(calibration), encoding="utf-8")
    out = tmp_path / "metric-aligned.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "duat_predictive_registry.cli",
            "metric-align-r",
            "--calibration",
            str(calibration_path),
            "--matrix",
            str(matrix_path),
            "--out",
            str(out),
            "--pretty",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["run_id"] == RUN_ID
    assert payload["publication_gate"] == "BLOCK"
