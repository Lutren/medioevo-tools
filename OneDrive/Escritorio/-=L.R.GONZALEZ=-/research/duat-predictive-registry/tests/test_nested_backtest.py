from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from duat_predictive_registry.nested_backtest import (
    RUN_ID,
    run_nested_domain_backtest,
    validate_nested_backtest_report,
    write_nested_backtest_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "reports" / "duat-benchmark-matrix-v0-4.json"
METRIC_ALIGNED = ROOT / "reports" / "duat-metric-aligned-r-calibration-v0-5.json"


def _reports():
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    metric = json.loads(METRIC_ALIGNED.read_text(encoding="utf-8"))
    return matrix, metric


def test_nested_backtest_runs_three_real_fixture_objectives():
    matrix, metric = _reports()
    report = run_nested_domain_backtest(matrix["objectives"], matrix, metric)
    assert report["run_id"] == RUN_ID
    assert report["publication_gate"] == "BLOCK"
    assert validate_nested_backtest_report(report) == []
    assert len(report["objectives"]) == 3
    assert all(item["data_mode"] == "real_fixture" for item in report["objectives"])
    assert all(item["n_outer_folds"] >= 2 for item in report["objectives"])


def test_nested_backtest_selected_configs_never_use_outer_test():
    matrix, metric = _reports()
    report = run_nested_domain_backtest(matrix["objectives"], matrix, metric)
    for item in report["objectives"]:
        assert item["backtest_leakage_guard"]["leakage_check"] == "PASS"
        assert all(config["outer_test_used_for_selection"] is False for config in item["selected_configs_by_fold"])


def test_nested_backtest_skips_insufficient_observations():
    matrix, metric = _reports()
    report = run_nested_domain_backtest(matrix["objectives"][:1], matrix, metric, min_observations=999)
    item = report["objectives"][0]
    assert item["oos_classification"] == "OOS_BLOCKED_INSUFFICIENT_DATA"
    assert item["out_of_sample_gate"] == "REVIEW"
    assert item["publication_gate"] == "BLOCK"


def test_nested_backtest_markdown_boundary_phrase(tmp_path):
    matrix, metric = _reports()
    report = run_nested_domain_backtest(matrix["objectives"], matrix, metric)
    out = tmp_path / "nested.md"
    write_nested_backtest_markdown(report, out)
    text = out.read_text(encoding="utf-8")
    assert "nested backtest is internal technical evidence only" in text
    assert "R reduction does not equal predictive validation" in text


def test_nested_backtest_schema_shape():
    schema = json.loads((ROOT / "schemas" / "duat_nested_domain_backtest_v0_6.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["publication_gate"]["const"] == "BLOCK"
    assert "OOS_R_ONLY_IMPROVED" in schema["properties"]["objectives"]["items"]["properties"]["oos_classification"]["enum"]


def test_cli_nested_backtest_generates_json(tmp_path):
    out = tmp_path / "nested.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "duat_predictive_registry.cli",
            "nested-backtest",
            "--matrix",
            str(MATRIX),
            "--metric-aligned",
            str(METRIC_ALIGNED),
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
