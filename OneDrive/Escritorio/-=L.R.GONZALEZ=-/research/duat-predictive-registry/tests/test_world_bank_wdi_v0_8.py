from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from data_readiness.world_bank_wdi_ingest import build_wdi_url, write_raw_json
from data_readiness.world_bank_wdi_transform import DUAT_TO_WDI, build_wdi_manifest, transform_raw_payload
from data_readiness.world_bank_wdi_validate import (
    RUN_ID,
    build_wdi_source_pack_report,
    validate_wdi_manifest,
)


ROOT = Path(__file__).resolve().parents[1]


def _sample_payload(code: str, start: int = 1990, end: int = 2021, future: bool = False):
    rows = []
    for year in range(end, start - 1, -1):
        rows.append(
            {
                "indicator": {"id": code, "value": f"Indicator {code}"},
                "country": {"id": "MX", "value": "Mexico"},
                "countryiso3code": "MEX",
                "date": str(year),
                "value": float(year - start + 1),
            }
        )
    if future:
        rows.append(
            {
                "indicator": {"id": code, "value": f"Indicator {code}"},
                "country": {"id": "MX", "value": "Mexico"},
                "countryiso3code": "MEX",
                "date": "2099",
                "value": 1.0,
            }
        )
    return [{"page": 1, "pages": 1, "per_page": 20000, "total": len(rows)}, rows]


def _manifest(tmp_path: Path, future: bool = False):
    series = []
    for duat_id, meta in DUAT_TO_WDI.items():
        code = meta["code"]
        raw = tmp_path / "raw" / f"MEX_{code}_raw.json"
        raw_sha = write_raw_json(_sample_payload(code, future=future and code == "NY.GDP.MKTP.KD.ZG"), raw)
        transformed = transform_raw_payload(
            raw_payload=json.loads(raw.read_text(encoding="utf-8")),
            country_code="MEX",
            indicator_code=code,
            raw_file=raw,
            raw_sha256=raw_sha,
            processed_dir=tmp_path / "processed",
            accessed_at="2026-05-15T00:00:00Z",
            current_year=2026,
        )
        series.append(
            {
                "duat_indicator_id": transformed["duat_indicator_id"],
                "wdi_indicator_code": transformed["wdi_indicator_code"],
                "indicator_name": transformed["indicator_name"],
                "unit": transformed["unit"],
                "frequency": transformed["frequency"],
                "start_year": transformed["start_year"],
                "end_year": transformed["end_year"],
                "n_observations": transformed["n_observations"],
                "missing_years": transformed["missing_years"],
                "duplicate_years": transformed["duplicate_years"],
                "future_years": transformed["future_years"],
                "raw_file": transformed["raw_file"],
                "raw_sha256": transformed["raw_sha256"],
                "processed_file": transformed["processed_file"],
                "processed_sha256": transformed["processed_sha256"],
                "processed_csv_file": transformed["processed_csv_file"],
                "processed_csv_sha256": transformed["processed_csv_sha256"],
                "source_card": f"source_cards/{duat_id}.md",
                "readiness_gate": "BLOCK" if transformed["future_years"] else "REVIEW",
                "license_terms_scan": "REVIEW",
                "comparability_review": "REVIEW",
                "leakage_preflight": "BLOCK" if transformed["future_years"] else "PASS",
                "notes": [],
            }
        )
    return build_wdi_manifest(
        country_code="MEX",
        country_name="Mexico",
        selection_reason="test fixture",
        series=series,
        accessed_at="2026-05-15T00:00:00Z",
    )


def test_wdi_url_uses_no_key_endpoint():
    url = build_wdi_url("MEX", "NY.GDP.MKTP.KD.ZG")
    assert url == "https://api.worldbank.org/v2/country/MEX/indicator/NY.GDP.MKTP.KD.ZG?format=json&per_page=20000"
    assert "key" not in url.lower()


def test_wdi_transform_orders_years_and_hashes_processed(tmp_path):
    code = "NY.GDP.MKTP.KD.ZG"
    raw = tmp_path / "raw.json"
    raw_sha = write_raw_json(_sample_payload(code), raw)
    transformed = transform_raw_payload(
        raw_payload=json.loads(raw.read_text(encoding="utf-8")),
        country_code="MEX",
        indicator_code=code,
        raw_file=raw,
        raw_sha256=raw_sha,
        processed_dir=tmp_path,
        accessed_at="2026-05-15T00:00:00Z",
        current_year=2026,
    )
    assert transformed["duat_indicator_id"] == "economy.real_growth_rate"
    assert transformed["n_observations"] == 32
    assert transformed["start_year"] == 1990
    assert transformed["end_year"] == 2021
    assert transformed["processed_sha256"]


def test_wdi_manifest_validates_three_series(tmp_path):
    manifest = _manifest(tmp_path)
    assert validate_wdi_manifest(manifest) == []
    assert manifest["run_id"] == RUN_ID
    assert len(manifest["series"]) == 3
    assert manifest["publication_gate"] == "BLOCK"


def test_wdi_report_reviews_license_and_comparability_even_with_long_history(tmp_path):
    manifest = _manifest(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    report = build_wdi_source_pack_report(manifest, manifest_path, "abc123")
    assert report["data_gate"] == "REVIEW"
    assert report["license_terms_scan"] == "REVIEW"
    assert report["comparability_review"] == "REVIEW"
    assert report["leakage_preflight"] == "PASS"
    assert report["benchmark_executed"] is False


def test_wdi_report_blocks_future_year_leakage(tmp_path):
    manifest = _manifest(tmp_path, future=True)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    report = build_wdi_source_pack_report(manifest, manifest_path, "abc123")
    assert report["data_gate"] == "BLOCK"
    assert report["leakage_preflight"] == "BLOCK"


def test_wdi_schema_shapes():
    manifest_schema = json.loads((ROOT / "schemas" / "world_bank_wdi_manifest_v0_8.schema.json").read_text(encoding="utf-8"))
    series_schema = json.loads((ROOT / "schemas" / "world_bank_wdi_series_v0_8.schema.json").read_text(encoding="utf-8"))
    assert manifest_schema["properties"]["publication_gate"]["const"] == "BLOCK"
    assert series_schema["properties"]["frequency"]["const"] == "annual"


def test_cli_data_readiness_accepts_wdi_manifest(tmp_path):
    manifest = _manifest(tmp_path)
    manifest_path = tmp_path / "world_bank_wdi_manifest_v0_8.json"
    report_path = tmp_path / "report.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "duat_predictive_registry.cli",
            "data-readiness",
            "--manifest",
            str(manifest_path),
            "--schema",
            str(ROOT / "schemas" / "world_bank_wdi_manifest_v0_8.schema.json"),
            "--pretty",
            "--out",
            str(report_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["run_id"] == RUN_ID
    assert report["publication_gate"] == "BLOCK"
