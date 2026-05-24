"""Official series manifest helpers for DUAT readiness v0.7."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


MANIFEST_VERSION = "0.7"

SOURCE_URLS = {
    "world_bank_indicators": "https://api.worldbank.org/v2/country/MEX/indicator",
    "eurostat_sdmx": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/",
    "INEGI": "https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/tabulados/enoe_indicadores_estrategicos_2005_2026_mensual.xlsx",
}

SOURCE_NAMES = {
    "world_bank_indicators": "World Bank Indicators fixture",
    "eurostat_sdmx": "Eurostat fixture",
    "INEGI": "INEGI ENOE fixture",
}


def load_manifest(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_manifest_json(manifest: dict[str, Any], path: str | Path, pretty: bool = True) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    return _sha256_file(target)


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("version") != MANIFEST_VERSION:
        errors.append("version must be 0.7")
    if manifest.get("project") != "DUAT Predictive Registry":
        errors.append("project mismatch")
    series = manifest.get("series")
    if not isinstance(series, list) or not series:
        errors.append("series must be a non-empty list")
    else:
        for item in series:
            if not item.get("indicator_id"):
                errors.append("series item missing indicator_id")
            if item.get("readiness_gate") not in {"REVIEW", "BLOCK", "APPROVE_FOR_BACKTEST"}:
                errors.append(f"{item.get('indicator_id')} invalid readiness_gate")
    return errors


def build_manifest_from_matrix(matrix_report: dict[str, Any]) -> dict[str, Any]:
    """Build a conservative manifest from an existing offline benchmark matrix."""

    rows: list[dict[str, Any]] = []
    for raw_report in matrix_report.get("raw_reports", []):
        indicator_id = raw_report.get("canonical_indicator_id")
        for source_series in raw_report.get("series", []):
            source_id = source_series.get("source_id")
            records = _records_from_source_series(source_series)
            years = [int(record["year"]) for record in records if str(record.get("year", "")).isdigit()]
            fixture_path = source_series.get("fixture_path")
            resolved_fixture = _resolve_existing_path(fixture_path) if fixture_path else None
            hash_sha256 = _sha256_file(resolved_fixture) if resolved_fixture else None
            rows.append(
                {
                    "indicator_id": indicator_id,
                    "source_id": source_id,
                    "source_name": SOURCE_NAMES.get(source_id, source_id),
                    "source_url": SOURCE_URLS.get(source_id),
                    "license_terms": _license_terms_for_source(source_id),
                    "license_review_required": True,
                    "country_or_scope": source_series.get("country_or_region"),
                    "frequency": source_series.get("frequency") or "annual",
                    "start_year": min(years) if years else None,
                    "end_year": max(years) if years else None,
                    "n_observations": len(records) if records else None,
                    "unit": source_series.get("unit"),
                    "definition": source_series.get("source_indicator_id"),
                    "download_method": "fixture",
                    "raw_file": fixture_path,
                    "processed_file": None,
                    "hash_sha256": hash_sha256,
                    "readiness_gate": "REVIEW",
                    "features_include_future_values": False,
                    "target_uses_future_values": False,
                    "comparability_status": "REVIEW",
                    "notes": [
                        "Derived from existing offline fixture evidence.",
                        "Short fixture history; not sufficient for official long-history backtest readiness.",
                    ],
                }
            )
    return {
        "version": MANIFEST_VERSION,
        "project": "DUAT Predictive Registry",
        "source_run_id": matrix_report.get("run_id"),
        "series": rows,
    }


def _records_from_source_series(source_series: dict[str, Any]) -> list[dict[str, Any]]:
    records = source_series.get("records")
    if isinstance(records, list):
        return records
    full_years = source_series.get("full_years") or []
    full_values = source_series.get("full_values") or []
    if full_years and full_values:
        return [{"year": year, "value": value} for year, value in zip(full_years, full_values)]
    years = source_series.get("years") or []
    values = source_series.get("values") or []
    if years and not values:
        values = source_series.get("actual") or []
    return [{"year": year, "value": value} for year, value in zip(years, values)]


def _license_terms_for_source(source_id: str | None) -> str:
    if source_id in {"world_bank_indicators", "eurostat_sdmx", "INEGI"}:
        return "TERMS_DOCUMENTED_HUMAN_REVIEW_REQUIRED"
    return "UNKNOWN"


def _sha256_file(path: str | Path) -> str:
    target = Path(path)
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_existing_path(path: str | Path | None) -> Path | None:
    if not path:
        return None
    raw = Path(path)
    candidates = [raw]
    if not raw.is_absolute():
        cwd = Path.cwd()
        candidates.append(cwd / raw)
        if cwd.name == "duat-predictive-registry" and len(cwd.parents) >= 2:
            candidates.append(cwd.parents[1] / raw)
        module_workspace = Path(__file__).resolve().parents[3]
        candidates.append(module_workspace / raw)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None
