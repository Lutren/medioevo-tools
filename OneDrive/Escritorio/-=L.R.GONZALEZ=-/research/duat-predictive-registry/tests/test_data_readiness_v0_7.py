from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from data_readiness.comparability_audit import audit_comparability
from data_readiness.leakage_preflight import run_leakage_preflight
from data_readiness.license_terms_review import review_license_terms
from data_readiness.official_series_manifest import build_manifest_from_matrix, validate_manifest
from data_readiness.readiness_rules import (
    RUN_ID,
    evaluate_manifest_readiness,
    minimum_observation_gate,
    validate_readiness_report,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX_V0_4 = ROOT / "reports" / "duat-benchmark-matrix-v0-4.json"


def _matrix() -> dict:
    return json.loads(MATRIX_V0_4.read_text(encoding="utf-8"))


def test_minimum_observation_gate_thresholds():
    assert minimum_observation_gate(6)["minimum_observation_review"] == "BLOCK"
    assert minimum_observation_gate(24)["minimum_observation_review"] == "REVIEW"
    assert minimum_observation_gate(30)["minimum_observation_gate"] == "APPROVE_FOR_BACKTEST"
    assert minimum_observation_gate(None)["minimum_observation_review"] == "REVIEW"


def test_license_terms_unknown_and_blocked_are_gated():
    assert review_license_terms({"license_terms": "UNKNOWN"})["license_terms_scan"] == "REVIEW"
    blocked = review_license_terms({"license_terms": "internal use prohibited"})
    assert blocked["license_terms_scan"] == "BLOCK"


def test_comparability_missing_definition_is_review():
    result = audit_comparability({"unit": "percent", "definition": None})
    assert result["comparability_review"] == "REVIEW"
    assert "missing_definition" in result["findings"]


def test_leakage_preflight_blocks_future_features():
    result = run_leakage_preflight({"features_include_future_values": True})
    assert result["leakage_preflight"] == "BLOCK"
    assert result["critical"] is True


def test_manifest_builds_from_existing_matrix_without_inventing_long_history():
    manifest = build_manifest_from_matrix(_matrix())
    assert validate_manifest(manifest) == []
    assert manifest["version"] == "0.7"
    assert len(manifest["series"]) >= 3
    assert all(item["download_method"] == "fixture" for item in manifest["series"])
    assert all(item["n_observations"] == 6 for item in manifest["series"])


def test_readiness_report_blocks_short_fixture_history_and_publication():
    report = evaluate_manifest_readiness(build_manifest_from_matrix(_matrix()))
    assert report["run_id"] == RUN_ID
    assert report["publication_gate"] == "BLOCK"
    assert report["data_gate"] == "BLOCK"
    assert report["minimum_observation_review"] == "BLOCK"
    assert report["recommendation"] == "collect_data"
    assert validate_readiness_report(report) == []


def test_reconstruction_test_is_complete():
    report = evaluate_manifest_readiness(build_manifest_from_matrix(_matrix()))
    reconstruction = report["reconstruction_test"]
    assert reconstruction["status"] == "PASS"
    assert reconstruction["score"] == 5
    assert reconstruction["max_score"] == 5
    assert reconstruction["critical_omissions"] == []


def test_schema_v0_7_shapes():
    manifest_schema = json.loads((ROOT / "schemas" / "duat_official_series_manifest_v0_7.schema.json").read_text(encoding="utf-8"))
    report_schema = json.loads((ROOT / "schemas" / "duat_data_readiness_report_v0_7.schema.json").read_text(encoding="utf-8"))
    assert manifest_schema["properties"]["version"]["const"] == "0.7"
    assert report_schema["properties"]["publication_gate"]["const"] == "BLOCK"
    assert "APPROVE" in report_schema["properties"]["data_gate"]["enum"]


def test_cli_data_readiness_generates_json(tmp_path):
    manifest = tmp_path / "manifest.json"
    report = tmp_path / "readiness.json"
    manifest.write_text(json.dumps(build_manifest_from_matrix(_matrix()), ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "duat_predictive_registry.cli",
            "data-readiness",
            "--manifest",
            str(manifest),
            "--schema",
            str(ROOT / "schemas" / "duat_data_readiness_report_v0_7.schema.json"),
            "--out",
            str(report),
            "--pretty",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["run_id"] == RUN_ID
    assert payload["publication_gate"] == "BLOCK"
    assert payload["data_gate"] == "BLOCK"
