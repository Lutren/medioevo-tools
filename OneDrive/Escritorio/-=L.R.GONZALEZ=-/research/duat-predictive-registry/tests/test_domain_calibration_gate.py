from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from duat_predictive_registry.benchmark_matrix import RUN_ID_V0_4, run_benchmark_matrix
from duat_predictive_registry.domain_calibration import (
    calibrate_benchmark_row,
    calibrate_matrix,
    validate_domain_calibration_report,
)
from duat_predictive_registry.objectives import find_workspace_root


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = find_workspace_root(ROOT)
ECONOMY = ROOT / "fixtures" / "duat_first_predictive_objective_v0_1.json"
LABOR = ROOT / "fixtures" / "duat_labor_market_unemployment_objective_v0_1.json"
THIRD = ROOT / "fixtures" / "duat_non_economic_third_indicator_objective_v0_1.json"


def _row(r_delta=-0.1, mae_base=2.0, rmse_base=3.0, mae_enh=1.0, rmse_enh=2.0):
    return {
        "objective_id": "x",
        "indicator": "economy.real_growth_rate",
        "data_mode": "real_fixture",
        "r_delta": r_delta,
        "baseline_metrics": {"MAE": mae_base, "RMSE": rmse_base, "MAPE_if_safe": {"value": None, "reason": "skip"}},
        "enhanced_metrics": {"MAE": mae_enh, "RMSE": rmse_enh, "MAPE_if_safe": {"value": None, "reason": "skip"}},
        "license_terms_scan": "REVIEW",
        "leakage_check": "PASS",
    }


def test_domain_calibration_classifies_r_improved_metrics_improved():
    result = calibrate_benchmark_row(_row(), comparability_status="PASS")
    assert result["classification"] == "OPERATIONAL_R_IMPROVED_METRICS_IMPROVED"
    assert result["r_improved"] is True
    assert result["metrics_improved"] is True
    assert result["publication_gate"] == "BLOCK"
    assert result["domain_calibration_gate"] == "REVIEW"


def test_domain_calibration_classifies_r_improved_metrics_worse():
    result = calibrate_benchmark_row(_row(mae_enh=2.2, rmse_enh=3.4), comparability_status="PASS")
    assert result["classification"] == "OPERATIONAL_R_IMPROVED_METRICS_WORSE"
    assert result["metrics_worse"] is True
    assert "direct error metrics worsened" in result["reason"]


def test_domain_calibration_classifies_mixed_metrics():
    result = calibrate_benchmark_row(_row(mae_enh=1.8, rmse_enh=3.4), comparability_status="PASS")
    assert result["classification"] == "OPERATIONAL_R_IMPROVED_METRICS_MIXED"
    assert result["metrics_mixed"] is True


def test_domain_calibration_blocks_synthetic_as_evidence():
    row = _row()
    row["data_mode"] = "synthetic_fixture"
    result = calibrate_benchmark_row(row, comparability_status="PASS")
    assert result["classification"] == "BLOCKED_NO_DATA"
    assert result["public_claim_allowed"] is False


def test_domain_calibration_report_validates_three_objectives():
    matrix = run_benchmark_matrix(
        [ECONOMY, LABOR, THIRD],
        WORKSPACE_ROOT,
        run_id=RUN_ID_V0_4,
        schema="duat.benchmark_matrix.v0_4",
    )
    report = calibrate_matrix(matrix, WORKSPACE_ROOT)
    assert validate_domain_calibration_report(report) == []
    assert report["publication_gate"] == "BLOCK"
    assert len(report["objectives"]) == 3
    labor = next(item for item in report["objectives"] if item["indicator"] == "labor_market.unemployment_rate.total")
    assert labor["classification"] == "OPERATIONAL_R_IMPROVED_METRICS_WORSE"


def test_domain_calibration_schema_shape():
    schema = json.loads((ROOT / "schemas" / "duat_domain_calibration_gate_v0_4.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["publication_gate"]["const"] == "BLOCK"
    assert "OPERATIONAL_R_IMPROVED_METRICS_WORSE" in schema["properties"]["objectives"]["items"]["properties"]["classification"]["enum"]


def test_cli_calibrate_domains_generates_json(tmp_path):
    matrix_path = tmp_path / "matrix.json"
    matrix = run_benchmark_matrix([ECONOMY, LABOR, THIRD], WORKSPACE_ROOT, run_id=RUN_ID_V0_4, schema="duat.benchmark_matrix.v0_4")
    matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
    out = tmp_path / "calibration.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "duat_predictive_registry.cli",
            "calibrate-domains",
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
    assert payload["run_id"] == "DUAT_DOMAIN_CALIBRATION_GATE_v0_4"
    assert payload["publication_gate"] == "BLOCK"
