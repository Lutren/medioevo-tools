"""Transform World Bank WDI raw payloads into DUAT source-pack series."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .world_bank_wdi_ingest import API_BASE, RUN_ID, build_wdi_url, sha256_file


TERMS_URL = "https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets"

DUAT_TO_WDI = {
    "economy.real_growth_rate": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "unit": "annual_percent_growth",
        "comparability_note": "GDP growth is a WDI annual percentage indicator; base and national accounts methodology may vary across revisions.",
    },
    "labor_market.unemployment_rate.total": {
        "code": "SL.UEM.TOTL.ZS",
        "unit": "percent_of_total_labor_force",
        "comparability_note": "Unemployment series may include modeled estimates and national definition differences.",
    },
    "demography.life_expectancy_at_birth.total": {
        "code": "SP.DYN.LE00.IN",
        "unit": "years",
        "comparability_note": "Life expectancy is a WDI annual demographic estimate; source revisions remain possible.",
    },
}

WDI_TO_DUAT = {meta["code"]: duat_id for duat_id, meta in DUAT_TO_WDI.items()}


def load_raw_payload(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def transform_raw_payload(
    *,
    raw_payload: Any,
    country_code: str,
    indicator_code: str,
    raw_file: str | Path,
    raw_sha256: str,
    processed_dir: str | Path,
    accessed_at: str,
    current_year: int | None = None,
) -> dict[str, Any]:
    """Transform a raw WDI response into sorted yearly observations."""

    if not isinstance(raw_payload, list) or len(raw_payload) < 2 or not isinstance(raw_payload[1], list):
        raise ValueError(f"Unexpected WDI payload for {indicator_code}")
    current_year = current_year or datetime.now(timezone.utc).year
    duat_indicator_id = WDI_TO_DUAT[indicator_code]
    metadata = DUAT_TO_WDI[duat_indicator_id]
    data_rows = raw_payload[1]
    country_name = _first_nested_value(data_rows, "country", "value")
    indicator_name = _first_nested_value(data_rows, "indicator", "value")
    records = []
    seen_years: set[int] = set()
    duplicate_years: list[int] = []
    future_years: list[int] = []
    for item in data_rows:
        year_raw = item.get("date")
        value = item.get("value")
        if value is None or year_raw is None:
            continue
        year = int(year_raw)
        if year in seen_years:
            duplicate_years.append(year)
        seen_years.add(year)
        if year > current_year:
            future_years.append(year)
        records.append(
            {
                "year": year,
                "value": float(value),
                "indicator_code": indicator_code,
                "indicator_name": indicator_name,
                "country_code": country_code,
                "country_name": country_name,
            }
        )
    records.sort(key=lambda row: row["year"])
    years = [row["year"] for row in records]
    missing_years = _missing_years(years)
    processed_json = Path(processed_dir) / f"{country_code}_{indicator_code}_processed.json"
    processed_csv = Path(processed_dir) / f"{country_code}_{indicator_code}_processed.csv"
    processed_json.parent.mkdir(parents=True, exist_ok=True)
    processed_payload = {
        "run_id": RUN_ID,
        "duat_indicator_id": duat_indicator_id,
        "wdi_indicator_code": indicator_code,
        "indicator_name": indicator_name,
        "country_code": country_code,
        "country_name": country_name,
        "frequency": "annual",
        "unit": metadata["unit"],
        "accessed_at": accessed_at,
        "source_url": build_wdi_url(country_code, indicator_code),
        "terms_url": TERMS_URL,
        "records": records,
        "missing_years": missing_years,
        "duplicate_years": sorted(set(duplicate_years)),
        "future_years": sorted(set(future_years)),
        "raw_file": Path(raw_file).as_posix(),
        "raw_sha256": raw_sha256,
        "transformation_notes": [
            "Excluded observations with null values.",
            "Sorted observations ascending by year.",
            "No interpolation or imputation applied.",
        ],
    }
    processed_json.write_text(json.dumps(processed_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_csv(records, processed_csv)
    return {
        "duat_indicator_id": duat_indicator_id,
        "wdi_indicator_code": indicator_code,
        "indicator_name": indicator_name,
        "unit": metadata["unit"],
        "frequency": "annual",
        "country_code": country_code,
        "country_name": country_name,
        "start_year": min(years) if years else None,
        "end_year": max(years) if years else None,
        "n_observations": len(records),
        "missing_years": missing_years,
        "duplicate_years": sorted(set(duplicate_years)),
        "future_years": sorted(set(future_years)),
        "raw_file": Path(raw_file).as_posix(),
        "raw_sha256": raw_sha256,
        "processed_file": processed_json.as_posix(),
        "processed_sha256": sha256_file(processed_json),
        "processed_csv_file": processed_csv.as_posix(),
        "processed_csv_sha256": sha256_file(processed_csv),
        "comparability_note": metadata["comparability_note"],
        "transformation_notes": processed_payload["transformation_notes"],
    }


def build_wdi_manifest(
    *,
    country_code: str,
    country_name: str | None,
    selection_reason: str,
    series: list[dict[str, Any]],
    accessed_at: str,
) -> dict[str, Any]:
    return {
        "version": "0.8",
        "run_id": RUN_ID,
        "source": {
            "name": "World Bank World Development Indicators",
            "api_base": API_BASE,
            "license_review_status": "REVIEW",
            "terms_url": TERMS_URL,
            "accessed_at": accessed_at,
        },
        "scope": {
            "country_code": country_code,
            "country_name": country_name,
            "selection_reason": selection_reason,
        },
        "series": series,
        "publication_gate": "BLOCK",
        "external_publication": False,
        "benchmark_executed": False,
    }


def _first_nested_value(rows: list[dict[str, Any]], outer: str, inner: str) -> str | None:
    for item in rows:
        value = item.get(outer)
        if isinstance(value, dict) and value.get(inner):
            return str(value[inner])
    return None


def _missing_years(years: list[int]) -> list[int]:
    if not years:
        return []
    present = set(years)
    return [year for year in range(min(years), max(years) + 1) if year not in present]


def _write_csv(records: list[dict[str, Any]], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["year", "value", "indicator_code", "indicator_name", "country_code", "country_name"])
        writer.writeheader()
        for record in records:
            writer.writerow(record)
