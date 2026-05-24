from __future__ import annotations

from pathlib import Path

from duat_predictive_registry.benchmarking import load_benchmark_series, run_benchmark
from duat_predictive_registry.objectives import find_workspace_root, load_objective, validate_objective


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = find_workspace_root(ROOT)
OBJECTIVE_PATH = ROOT / "fixtures" / "duat_labor_market_unemployment_objective_v0_1.json"


def test_labor_market_objective_validates_and_uses_real_fixture():
    objective = load_objective(OBJECTIVE_PATH)
    assert validate_objective(objective) == []
    assert objective["synthetic"] is False
    assert objective["canonical_indicator_id"] == "labor_market.unemployment_rate.total"
    assert objective["data_policy"]["publication_gate"] == "BLOCK"


def test_labor_market_objective_has_three_real_series():
    objective = load_objective(OBJECTIVE_PATH)
    records = load_benchmark_series(objective, WORKSPACE_ROOT)
    assert {record.source_id for record in records} == {"world_bank_indicators", "eurostat_sdmx", "INEGI"}
    assert all(record.comparability_class == "STRONG_PROXY" for record in records)
    assert all(len(record.values) == 6 for record in records)


def test_labor_market_benchmark_reports_real_fixture_and_no_leakage():
    report = run_benchmark(OBJECTIVE_PATH, WORKSPACE_ROOT)
    assert report["data_mode"] == "real_fixture"
    assert report["leakage_check"] == "PASS"
    assert report["publication_gate"] == "BLOCK"
    for series in report["series"]:
        for fold in series["folds"]:
            assert max(fold["train_years"]) < fold["target_year"]
