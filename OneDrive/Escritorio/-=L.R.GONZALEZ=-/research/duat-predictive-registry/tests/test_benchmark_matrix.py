from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from duat_predictive_registry.benchmark_matrix import (
    classify_replication,
    run_benchmark_matrix,
    validate_matrix_shape,
    write_license_comparability_markdown,
    write_matrix_json,
    write_matrix_markdown,
)
from duat_predictive_registry.objectives import find_workspace_root


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = find_workspace_root(ROOT)
ECONOMY = ROOT / "fixtures" / "duat_first_predictive_objective_v0_1.json"
LABOR = ROOT / "fixtures" / "duat_labor_market_unemployment_objective_v0_1.json"


def test_benchmark_matrix_runs_two_real_objectives():
    matrix = run_benchmark_matrix([ECONOMY, LABOR], WORKSPACE_ROOT)
    assert validate_matrix_shape(matrix) == []
    assert matrix["publication_gate"] == "BLOCK"
    assert {row["indicator"] for row in matrix["objectives"]} == {
        "economy.real_growth_rate",
        "labor_market.unemployment_rate.total",
    }
    assert all(row["data_mode"] == "real_fixture" for row in matrix["objectives"])


def test_matrix_preserves_economy_result_from_previous_benchmark():
    matrix = run_benchmark_matrix([ECONOMY, LABOR], WORKSPACE_ROOT)
    economy = next(row for row in matrix["objectives"] if row["indicator"] == "economy.real_growth_rate")
    assert round(economy["r_before"], 12) == round(0.22888520901307724, 12)
    assert round(economy["r_after"], 12) == round(0.16431596112341315, 12)
    assert round(economy["r_delta"], 12) == round(-0.06456924788966409, 12)


def test_replication_status_rules():
    replicated = [
        {"data_mode": "real_fixture", "indicator": "economy.real_growth_rate", "r_delta": -0.02, "leakage_check": "PASS"},
        {"data_mode": "real_fixture", "indicator": "labor_market.unemployment_rate.total", "r_delta": -0.03, "leakage_check": "PASS"},
    ]
    mixed = [
        {"data_mode": "real_fixture", "indicator": "economy.real_growth_rate", "r_delta": -0.001, "leakage_check": "PASS"},
        {"data_mode": "real_fixture", "indicator": "labor_market.unemployment_rate.total", "r_delta": -0.03, "leakage_check": "PASS"},
    ]
    not_replicated = [
        {"data_mode": "real_fixture", "indicator": "economy.real_growth_rate", "r_delta": -0.02, "leakage_check": "PASS"},
        {"data_mode": "real_fixture", "indicator": "labor_market.unemployment_rate.total", "r_delta": 0.01, "leakage_check": "PASS"},
    ]
    blocked = [
        {"data_mode": "blocked_no_data", "indicator": "labor_market.unemployment_rate.total", "r_delta": None, "leakage_check": "REVIEW"}
    ]
    assert classify_replication(replicated) == "REPLICATED_LOCAL"
    assert classify_replication(mixed) == "MIXED_LOCAL"
    assert classify_replication(not_replicated) == "NOT_REPLICATED"
    assert classify_replication(blocked) == "BLOCKED_NO_DATA"


def test_matrix_writers_and_claim_boundary(tmp_path):
    matrix = run_benchmark_matrix([ECONOMY, LABOR], WORKSPACE_ROOT)
    json_out = tmp_path / "matrix.json"
    md_out = tmp_path / "matrix.md"
    review_out = tmp_path / "review.md"
    digest = write_matrix_json(matrix, json_out)
    write_matrix_markdown(matrix, md_out)
    write_license_comparability_markdown(matrix, review_out)
    assert digest
    assert json.loads(json_out.read_text(encoding="utf-8"))["publication_gate"] == "BLOCK"
    md_text = md_out.read_text(encoding="utf-8")
    assert "Internal local benchmark only" in md_text
    assert "not a public predictive claim" in md_text
    review_text = review_out.read_text(encoding="utf-8")
    assert "LicenseTermsScan remains REVIEW" in review_text


def test_cli_benchmark_matrix_generates_json(tmp_path):
    out = tmp_path / "matrix.json"
    command = [
        sys.executable,
        "-m",
        "duat_predictive_registry.cli",
        "benchmark-matrix",
        "--objectives",
        "fixtures/duat_first_predictive_objective_v0_1.json",
        "fixtures/duat_labor_market_unemployment_objective_v0_1.json",
        "--out",
        str(out),
        "--pretty",
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["run_id"] == "DUAT_PREDICTIVE_BENCHMARK_MATRIX_v0_3"
    assert payload["publication_gate"] == "BLOCK"
    assert payload["matrix_interpretation"]["public_claim_allowed"] is False
