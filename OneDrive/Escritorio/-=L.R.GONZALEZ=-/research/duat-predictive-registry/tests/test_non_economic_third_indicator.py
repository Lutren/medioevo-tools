from __future__ import annotations

from pathlib import Path

from duat_predictive_registry.benchmarking import load_benchmark_series, run_benchmark
from duat_predictive_registry.objectives import find_workspace_root, load_objective, validate_objective


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = find_workspace_root(ROOT)
OBJECTIVE_PATH = ROOT / "fixtures" / "duat_non_economic_third_indicator_objective_v0_1.json"


def test_third_indicator_objective_is_real_fixture():
    objective = load_objective(OBJECTIVE_PATH)
    assert validate_objective(objective) == []
    assert objective["synthetic"] is False
    assert objective["canonical_indicator_id"] == "demography.life_expectancy_at_birth.total"
    assert objective["data_policy"]["publication_gate"] == "BLOCK"


def test_third_indicator_has_real_series():
    objective = load_objective(OBJECTIVE_PATH)
    records = load_benchmark_series(objective, WORKSPACE_ROOT)
    assert {record.source_id for record in records} == {"world_bank_indicators", "eurostat_sdmx"}
    assert all(record.comparability_class == "STRONG_PROXY" for record in records)
    assert all(len(record.values) == 6 for record in records)


def test_third_indicator_benchmark_stays_local_and_blocked():
    report = run_benchmark(OBJECTIVE_PATH, WORKSPACE_ROOT)
    assert report["data_mode"] == "real_fixture"
    assert report["leakage_check"] == "PASS"
    assert report["publication_gate"] == "BLOCK"
    assert report["forecast_gate"] in {"REVIEW", "APPROVE_LOCAL"}
