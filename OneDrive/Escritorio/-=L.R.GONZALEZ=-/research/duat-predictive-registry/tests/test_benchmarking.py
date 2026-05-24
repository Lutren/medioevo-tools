from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from duat_predictive_registry.benchmarking import (
    _benchmark_forecast_gate,
    _evaluate_series,
    load_benchmark_series,
    run_benchmark,
)
from duat_predictive_registry.objectives import find_workspace_root, load_objective


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = find_workspace_root(ROOT)
OBJECTIVE_PATH = ROOT / "fixtures" / "duat_first_predictive_objective_v0_1.json"


def test_loads_real_geodia_fixture_series():
    objective = load_objective(OBJECTIVE_PATH)
    records = load_benchmark_series(objective, WORKSPACE_ROOT)
    assert len(records) >= 2
    assert {record.source_id for record in records} == {"world_bank_indicators", "eurostat_sdmx"}
    assert all(record.comparability_class == "REVIEW" for record in records)
    assert all(len(record.values) == 6 for record in records)


def test_timeseries_split_is_one_step_and_no_leakage():
    objective = load_objective(OBJECTIVE_PATH)
    record = load_benchmark_series(objective, WORKSPACE_ROOT)[0]
    report = _evaluate_series(record, objective)
    for fold in report["folds"]:
        assert max(fold["train_years"]) < fold["target_year"]
        assert fold["leakage_check"] == "PASS"


def test_run_benchmark_produces_r_before_after_report():
    report = run_benchmark(OBJECTIVE_PATH, WORKSPACE_ROOT)
    assert report["data_mode"] == "real_fixture"
    assert report["publication_gate"] == "BLOCK"
    assert report["r_before"] is not None
    assert report["r_after"] is not None
    assert report["r_delta"] == report["r_after"] - report["r_before"]
    assert report["leakage_check"] == "PASS"


def test_cli_generates_report_json(tmp_path):
    out = tmp_path / "benchmark.json"
    command = [
        sys.executable,
        "-m",
        "duat_predictive_registry.cli",
        "benchmark",
        "--objective",
        "fixtures/duat_first_predictive_objective_v0_1.json",
        "--out",
        str(out),
        "--pretty",
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["publication_gate"] == "BLOCK"
    assert payload["forecast_gate"] in {"APPROVE_LOCAL", "REVIEW"}
    assert payload["sha256"]


def test_forecast_gate_blocks_secret_and_private_data_flags():
    secret_gate = _benchmark_forecast_gate(
        r_after=0.2,
        r_delta=-0.1,
        enhanced_mae=1.0,
        baseline_mae=1.1,
        minimum_evidence_passed=True,
        leakage_check="PASS",
        license_terms_scan="PASS",
        secret_detected=True,
    )
    private_gate = _benchmark_forecast_gate(
        r_after=0.2,
        r_delta=-0.1,
        enhanced_mae=1.0,
        baseline_mae=1.1,
        minimum_evidence_passed=True,
        leakage_check="PASS",
        license_terms_scan="PASS",
        private_data_detected=True,
    )
    assert secret_gate["forecast_gate"] == "BLOCK"
    assert private_gate["forecast_gate"] == "BLOCK"


def test_forecast_gate_keeps_publication_block_when_license_review():
    gate = _benchmark_forecast_gate(
        r_after=0.2,
        r_delta=-0.1,
        enhanced_mae=1.0,
        baseline_mae=1.1,
        minimum_evidence_passed=True,
        leakage_check="PASS",
        license_terms_scan="REVIEW",
    )
    assert gate["forecast_gate"] == "REVIEW"
    assert gate["publication_gate"] == "BLOCK"
