from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from data_readiness.world_bank_wdi_governance_review import (
    RUN_ID,
    calculate_backtest_open_gate,
    calculate_data_gate,
    license_terms_scan,
    review_series,
    validate_governance_decision,
    verify_world_bank_terms,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data_sources" / "world_bank_wdi" / "world_bank_wdi_manifest_v0_8.json"


def _series(n: int = 35, future: bool = False):
    return {
        "duat_indicator_id": "labor_market.unemployment_rate.total",
        "wdi_indicator_code": "SL.UEM.TOTL.ZS",
        "indicator_name": "Unemployment, total (% of total labor force) (modeled ILO estimate)",
        "unit": "percent_of_total_labor_force",
        "frequency": "annual",
        "start_year": 1991,
        "end_year": 2025,
        "n_observations": n,
        "missing_years": [],
        "duplicate_years": [],
        "future_years": [2099] if future else [],
    }


def test_terms_unavailable_keeps_license_review():
    terms = verify_world_bank_terms(verify_external=False)
    assert terms["external_terms_verification"] == "UNAVAILABLE"
    assert license_terms_scan(terms, []) == "REVIEW"


def test_series_with_modeled_estimate_stays_comparability_review():
    metadata = {
        "title": "Unemployment, total (% of total labor force) (modeled ILO estimate)",
        "source_organization": "ILO Modelled Estimates database",
        "long_definition": "Unemployment refers to a labor force share.",
    }
    reviewed = review_series(_series(), metadata)
    assert reviewed["comparability_review"] == "REVIEW"
    assert "modeled_estimate" in reviewed["modeled_or_estimate_flags"]


def test_data_gate_review_when_license_or_comparability_review():
    series_reviews = [review_series(_series(), {"title": "x", "source_organization": "ILO Modelled Estimates database"})]
    gate = calculate_data_gate(
        series_reviews=series_reviews,
        license_terms_scan="REVIEW",
        comparability_review="REVIEW",
        leakage_preflight="PASS",
        secret_scan="PASS",
        boundary_check="PASS",
        schema_validation="PASS",
    )
    assert gate == "REVIEW"


def test_data_gate_blocks_leakage_or_short_series():
    reviewed = review_series(_series(n=10), {"title": "x", "source_organization": ""})
    gate = calculate_data_gate(
        series_reviews=[reviewed],
        license_terms_scan="PASS",
        comparability_review="PASS",
        leakage_preflight="PASS",
        secret_scan="PASS",
        boundary_check="PASS",
        schema_validation="PASS",
    )
    assert gate == "BLOCK"
    leakage_gate = calculate_data_gate(
        series_reviews=[review_series(_series(future=True), {"title": "x", "source_organization": ""})],
        license_terms_scan="PASS",
        comparability_review="PASS",
        leakage_preflight="BLOCK",
        secret_scan="PASS",
        boundary_check="PASS",
        schema_validation="PASS",
    )
    assert leakage_gate == "BLOCK"


def test_backtest_open_gate_review_only_dry_run():
    series_reviews = [review_series(_series(), {"title": "x", "source_organization": "ILO Modelled Estimates database"})]
    assert calculate_backtest_open_gate("REVIEW", series_reviews, "REVIEW", "REVIEW", "PASS") == "REVIEW_ONLY_DRY_RUN"


def test_governance_schema_shape():
    schema = json.loads((ROOT / "schemas" / "world_bank_wdi_governance_decision_v0_8_1.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["publication_gate"]["const"] == "BLOCK"
    assert "REVIEW_ONLY_DRY_RUN" in schema["properties"]["backtest_open_gate"]["enum"]


def test_cli_wdi_governance_review_generates_json(tmp_path):
    out = tmp_path / "governance.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "duat_predictive_registry.cli",
            "wdi-governance-review",
            "--manifest",
            str(MANIFEST),
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
    assert payload["benchmark_executed"] is False
    assert validate_governance_decision(payload) == []
