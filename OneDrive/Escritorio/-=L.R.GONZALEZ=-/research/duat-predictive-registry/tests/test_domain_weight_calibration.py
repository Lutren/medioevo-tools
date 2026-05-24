from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from duat_predictive_registry.benchmark_matrix import RUN_ID_V0_4, run_benchmark_matrix
from duat_predictive_registry.domain_weight_calibration import calibrate_domain_weights
from duat_predictive_registry.objectives import find_workspace_root


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = find_workspace_root(ROOT)
ECONOMY = ROOT / "fixtures" / "duat_first_predictive_objective_v0_1.json"
LABOR = ROOT / "fixtures" / "duat_labor_market_unemployment_objective_v0_1.json"
THIRD = ROOT / "fixtures" / "duat_non_economic_third_indicator_objective_v0_1.json"


def test_domain_weight_calibration_runs_locally_with_publication_block():
    matrix = run_benchmark_matrix([ECONOMY, LABOR, THIRD], WORKSPACE_ROOT, run_id=RUN_ID_V0_4, schema="duat.benchmark_matrix.v0_4")
    report = calibrate_domain_weights(matrix)
    assert report["run_id"] == "DUAT_DOMAIN_WEIGHT_CALIBRATION_v0_5"
    assert report["publication_gate"] == "BLOCK"
    assert report["action_gate_local"] == "REVIEW"
    assert report["domain_weight_calibration_status"] in {"REVIEW", "NOT_IMPROVED", "SKIPPED_INSUFFICIENT_DATA"}
    assert len(report["objectives"]) == 3
    assert all(item["claim_allowed_public"] is False for item in report["objectives"])


def test_domain_weight_calibration_does_not_hide_not_improved_status():
    matrix = {
        "raw_reports": [
            {
                "objective_id": "x",
                "canonical_indicator_id": "economy.real_growth_rate",
                "data_mode": "real_fixture",
                "baseline_metrics": {"selected": {"MAE": 0.01, "RMSE": 0.01}},
                "enhanced_metrics": {"MAE": 0.02, "RMSE": 0.02},
                "series": [
                    {
                        "full_years": [2018, 2019, 2020, 2021, 2022],
                        "full_values": [1, 2, 3, 4, 5],
                        "folds": [
                            {"train_years": [2018, 2019], "actual": 3, "target_year": 2020},
                            {"train_years": [2018, 2019, 2020], "actual": 4, "target_year": 2021},
                            {"train_years": [2018, 2019, 2020, 2021], "actual": 5, "target_year": 2022},
                            {"train_years": [2018, 2019, 2020, 2021], "actual": 5, "target_year": 2022},
                            {"train_years": [2018, 2019, 2020, 2021], "actual": 5, "target_year": 2022},
                        ],
                    }
                ],
            }
        ]
    }
    report = calibrate_domain_weights(matrix)
    assert report["objectives"][0]["domain_weight_calibration_status"] == "NOT_IMPROVED"


def test_cli_calibrate_domain_weights_generates_json(tmp_path):
    matrix = run_benchmark_matrix([ECONOMY, LABOR, THIRD], WORKSPACE_ROOT, run_id=RUN_ID_V0_4, schema="duat.benchmark_matrix.v0_4")
    matrix_path = tmp_path / "matrix.json"
    matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
    out = tmp_path / "domain-weights.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "duat_predictive_registry.cli",
            "calibrate-domain-weights",
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
    assert payload["publication_gate"] == "BLOCK"
    assert payload["run_id"] == "DUAT_DOMAIN_WEIGHT_CALIBRATION_v0_5"
