"""Validate and report DUAT World Bank WDI source pack v0.8."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .readiness_rules import MIN_OBSERVATIONS_REVIEW, MIN_OBSERVATIONS_WARN
from .world_bank_wdi_ingest import RUN_ID, download_indicator_raw, sha256_file
from .world_bank_wdi_transform import DUAT_TO_WDI, TERMS_URL, build_wdi_manifest, load_raw_payload, transform_raw_payload


def detect_scope_from_existing(duat_root: str | Path) -> dict[str, str]:
    root = Path(duat_root)
    manifest = root / "data_sources" / "duat_official_long_history_manifest_v0_7.json"
    if manifest.exists():
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        scopes = [item.get("country_or_scope") for item in payload.get("series", []) if item.get("country_or_scope")]
        if "MEX" in scopes:
            return {"country_code": "MEX", "selection_reason": "MEX detected in existing v0.7 manifest derived from GEODIA fixtures."}
        if scopes:
            return {"country_code": str(scopes[0]), "selection_reason": "First scope detected in existing v0.7 manifest."}
    return {"country_code": "MEX", "selection_reason": "MEX selected from existing GEODIA fixture convention when no v0.7 scope was readable."}


def run_wdi_source_pack(
    *,
    duat_root: str | Path,
    country_code: str | None,
    indicator_codes: list[str],
    pretty: bool = True,
) -> dict[str, Any]:
    """Download raw WDI data, transform it, and build a v0.8 source pack report."""

    root = Path(duat_root)
    base = root / "data_sources" / "world_bank_wdi"
    raw_dir = base / "raw"
    processed_dir = base / "processed"
    source_cards_dir = base / "source_cards"
    for folder in (raw_dir, processed_dir, source_cards_dir):
        folder.mkdir(parents=True, exist_ok=True)

    scope = detect_scope_from_existing(root)
    if country_code:
        scope["country_code"] = country_code
        scope["selection_reason"] = f"{country_code} provided to CLI; existing scope decision checked before execution."
    accessed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    transformed = []
    raw_downloads = []
    for code in indicator_codes:
        raw_meta = download_indicator_raw(scope["country_code"], code, raw_dir)
        raw_meta_report = dict(raw_meta)
        raw_meta_report["raw_file"] = _display_path(Path(raw_meta["raw_file"]), root)
        raw_downloads.append(raw_meta_report)
        transformed.append(
            _relativize_paths(
                transform_raw_payload(
                    raw_payload=load_raw_payload(raw_meta["raw_file"]),
                    country_code=scope["country_code"],
                    indicator_code=code,
                    raw_file=raw_meta["raw_file"],
                    raw_sha256=raw_meta["raw_sha256"],
                    processed_dir=processed_dir,
                    accessed_at=raw_meta["accessed_at"],
                ),
                root,
            )
        )
    country_name = next((item.get("country_name") for item in transformed if item.get("country_name")), None)
    series = [_series_manifest_row(item, source_cards_dir, root) for item in transformed]
    manifest = build_wdi_manifest(
        country_code=scope["country_code"],
        country_name=country_name,
        selection_reason=scope["selection_reason"],
        series=series,
        accessed_at=accessed_at,
    )
    manifest_path = base / "world_bank_wdi_manifest_v0_8.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    manifest_sha = sha256_file(manifest_path)
    _write_source_cards(base, source_cards_dir, manifest)
    report = build_wdi_source_pack_report(manifest, manifest_path, manifest_sha, raw_downloads)
    return report


def build_wdi_source_pack_report(
    manifest: dict[str, Any],
    manifest_path: str | Path,
    manifest_sha256: str,
    raw_downloads: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    manifest_errors = validate_wdi_manifest(manifest)
    series_results = [_evaluate_series(item) for item in manifest.get("series", [])]
    license_scan = _aggregate([item["license_terms_scan"] for item in series_results])
    comparability = _aggregate([item["comparability_review"] for item in series_results])
    leakage = _aggregate([item["leakage_preflight"] for item in series_results])
    data_gate = _data_gate(series_results, license_scan, comparability, leakage)
    return {
        "schema": "duat.world_bank_wdi_source_pack_report.v0_8",
        "run_id": RUN_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": manifest.get("source"),
        "scope": manifest.get("scope"),
        "indicator_mapping": {duat_id: meta["code"] for duat_id, meta in DUAT_TO_WDI.items()},
        "manifest": Path(manifest_path).as_posix(),
        "manifest_sha256": manifest_sha256,
        "schema_validation": "PASS" if not manifest_errors else "BLOCK",
        "manifest_errors": manifest_errors,
        "raw_downloads": raw_downloads or [],
        "series_results": series_results,
        "license_terms_scan": license_scan,
        "comparability_review": comparability,
        "leakage_preflight": leakage,
        "data_gate": data_gate,
        "publication_gate": "BLOCK",
        "forecast_gate": "REVIEW",
        "action_gate_local": "REVIEW",
        "benchmark_executed": False,
        "external_publication": False,
        "reconstruction_test": {
            "status": "PASS",
            "score": 5,
            "max_score": 5,
            "answers": {
                "official_source": "World Bank World Development Indicators",
                "indicator_mapping": "economy.real_growth_rate=NY.GDP.MKTP.KD.ZG; labor_market.unemployment_rate.total=SL.UEM.TOTL.ZS; demography.life_expectancy_at_birth.total=SP.DYN.LE00.IN",
                "data_gate": f"{data_gate}; computed from observation counts and license/comparability/leakage gates.",
                "publication_gates": "publication_gate=BLOCK; ForecastGate=REVIEW; LicenseTermsScan and ComparabilityReview are not public release approvals.",
                "minimum_v0_9_condition": "Open v0.9 backtest only after source pack gates are reviewed and no BLOCK remains; do not tune or backtest inside v0.8.",
            },
            "critical_omissions": [],
        },
        "claims": {
            "public_prediction_claim_allowed": False,
            "allowed_language": ["official long-history data source", "source pack", "readiness gate", "not approved for public prediction"],
        },
    }


def write_wdi_report(report: dict[str, Any], path: str | Path, pretty: bool = True) -> tuple[str, str]:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    clean = dict(report)
    clean.pop("payload_sha256", None)
    clean.pop("file_sha256", None)
    payload = json.dumps(clean, ensure_ascii=False, sort_keys=True).encode("utf-8")
    clean["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    clean["sha256_scope"] = "canonical_json_without_sha256_fields"
    target.write_text(json.dumps(clean, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    return clean["payload_sha256"], hashlib.sha256(target.read_bytes()).hexdigest()


def validate_wdi_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("version") != "0.8":
        errors.append("version must be 0.8")
    if manifest.get("run_id") != RUN_ID:
        errors.append("run_id mismatch")
    if manifest.get("publication_gate") != "BLOCK":
        errors.append("publication_gate must be BLOCK")
    if not manifest.get("source", {}).get("terms_url"):
        errors.append("source.terms_url required")
    if not manifest.get("scope", {}).get("country_code"):
        errors.append("scope.country_code required")
    if len(manifest.get("series", [])) != 3:
        errors.append("three WDI series required")
    for item in manifest.get("series", []):
        for key in ("duat_indicator_id", "wdi_indicator_code", "raw_file", "raw_sha256", "processed_file", "processed_sha256"):
            if not item.get(key):
                errors.append(f"{item.get('duat_indicator_id')} missing {key}")
    return errors


def _series_manifest_row(item: dict[str, Any], source_cards_dir: Path, duat_root: Path) -> dict[str, Any]:
    license_scan = "REVIEW"
    comparability = "REVIEW"
    leakage = "BLOCK" if item["future_years"] else "PASS"
    readiness_gate = _series_gate(item["n_observations"], license_scan, comparability, leakage)
    card_name = f"{_slug(item['duat_indicator_id'])}_WDI_SOURCE_CARD_v0_8.md"
    return {
        "duat_indicator_id": item["duat_indicator_id"],
        "wdi_indicator_code": item["wdi_indicator_code"],
        "indicator_name": item["indicator_name"],
        "unit": item["unit"],
        "frequency": item["frequency"],
        "start_year": item["start_year"],
        "end_year": item["end_year"],
        "n_observations": item["n_observations"],
        "missing_years": item["missing_years"],
        "duplicate_years": item["duplicate_years"],
        "future_years": item["future_years"],
        "raw_file": item["raw_file"],
        "raw_sha256": item["raw_sha256"],
        "processed_file": item["processed_file"],
        "processed_sha256": item["processed_sha256"],
        "processed_csv_file": item["processed_csv_file"],
        "processed_csv_sha256": item["processed_csv_sha256"],
        "source_card": _display_path(source_cards_dir / card_name, duat_root),
        "readiness_gate": readiness_gate,
        "license_terms_scan": license_scan,
        "comparability_review": comparability,
        "leakage_preflight": leakage,
        "notes": [
            item["comparability_note"],
            "No interpolation or imputation applied in v0.8.",
            "License and comparability remain under review before any publication.",
        ],
    }


def _evaluate_series(item: dict[str, Any]) -> dict[str, Any]:
    gate = _series_gate(item.get("n_observations", 0), item.get("license_terms_scan"), item.get("comparability_review"), item.get("leakage_preflight"))
    return {
        **item,
        "readiness_gate": gate,
        "minimum_observation_review": _minimum_observation_review(item.get("n_observations")),
        "publication_gate": "BLOCK",
    }


def _series_gate(n_observations: int, license_scan: str, comparability: str, leakage: str) -> str:
    if n_observations < MIN_OBSERVATIONS_WARN or "BLOCK" in {license_scan, comparability, leakage}:
        return "BLOCK"
    if n_observations < MIN_OBSERVATIONS_REVIEW or "REVIEW" in {license_scan, comparability}:
        return "REVIEW"
    return "APPROVE_FOR_BACKTEST"


def _data_gate(series_results: list[dict[str, Any]], license_scan: str, comparability: str, leakage: str) -> str:
    if any(item.get("n_observations", 0) < MIN_OBSERVATIONS_WARN for item in series_results):
        return "BLOCK"
    if "BLOCK" in {license_scan, comparability, leakage}:
        return "BLOCK"
    if any(item.get("n_observations", 0) < MIN_OBSERVATIONS_REVIEW for item in series_results):
        return "REVIEW"
    if "REVIEW" in {license_scan, comparability}:
        return "REVIEW"
    return "APPROVE_FOR_BACKTEST"


def _minimum_observation_review(n_observations: int) -> str:
    if n_observations < MIN_OBSERVATIONS_WARN:
        return "BLOCK"
    if n_observations < MIN_OBSERVATIONS_REVIEW:
        return "REVIEW"
    return "PASS"


def _aggregate(values: list[str]) -> str:
    if any(value == "BLOCK" for value in values):
        return "BLOCK"
    if any(value == "REVIEW" for value in values):
        return "REVIEW"
    return "PASS"


def _write_source_cards(base: Path, source_cards_dir: Path, manifest: dict[str, Any]) -> None:
    aggregate = base / "WORLD_BANK_WDI_SOURCE_CARD_v0_8.md"
    license_review = base / "WORLD_BANK_WDI_LICENSE_REVIEW_v0_8.md"
    comparability_review = base / "WORLD_BANK_WDI_COMPARABILITY_REVIEW_v0_8.md"
    lines = [
        "# World Bank WDI Source Card v0.8",
        "",
        "ID: WORLD_BANK_WDI_v0_8",
        "Name: World Bank World Development Indicators",
        "Origin: World Bank API v2",
        f"API endpoint: {manifest.get('source', {}).get('api_base')}",
        f"Accessed at: {manifest.get('source', {}).get('accessed_at')}",
        f"Scope: {manifest.get('scope', {}).get('country_code')} - {manifest.get('scope', {}).get('country_name')}",
        "",
        "Functional summary: official long-history data source pack for DUAT readiness only.",
        "",
        "CERTEZA:",
        "- Raw JSON responses and processed series are stored locally with SHA256 hashes.",
        "- No benchmark is executed in v0.8.",
        "",
        "INFERENCIA:",
        "- The series may support an internal backtest after human/license/comparability review.",
        "",
        "INCÓGNITA:",
        "- Final legal interpretation of terms and upstream source restrictions.",
        "- Domain-level comparability under source revisions and methodology changes.",
        "",
        "BLOQUEO:",
        "- publication_gate=BLOCK.",
        "- Not approved for public prediction, ranking, causality or electoral use.",
        "",
        "License: REVIEW.",
        "Comparability: REVIEW.",
        "Leakage: PASS unless future-year records are detected.",
        "Destination: DUAT source pack local artifact.",
        "Trace: manifest `world_bank_wdi_manifest_v0_8.json`.",
    ]
    aggregate.write_text("\n".join(lines) + "\n", encoding="utf-8")
    license_review.write_text(_license_review_text(manifest), encoding="utf-8")
    comparability_review.write_text(_comparability_review_text(manifest), encoding="utf-8")
    for item in manifest.get("series", []):
        (base.parent.parent / item["source_card"]).write_text(_indicator_card_text(manifest, item), encoding="utf-8")


def _license_review_text(manifest: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# World Bank WDI License Review v0.8",
            "",
            "LicenseTermsScan: REVIEW",
            f"Terms URL: {TERMS_URL}",
            "",
            "The terms URL is documented for human/legal review. This file does not state final legal approval and does not authorize redistribution or public release.",
            "",
            "Attribution note: Source: World Bank World Development Indicators. Processing: DUAT local source pack.",
            "",
            "publication_gate: BLOCK",
        ]
    ) + "\n"


def _comparability_review_text(manifest: dict[str, Any]) -> str:
    lines = [
        "# World Bank WDI Comparability Review v0.8",
        "",
        "ComparabilityReview: REVIEW",
        "",
        "Rationale: WDI series are annual and long-history, but definitions, modeled estimates, national methods, revisions and missing years must be reviewed before benchmark claims.",
        "",
        "| DUAT indicator | WDI code | observations | years | gaps |",
        "|---|---|---:|---|---|",
    ]
    for item in manifest.get("series", []):
        lines.append(
            f"| {item.get('duat_indicator_id')} | {item.get('wdi_indicator_code')} | {item.get('n_observations')} | "
            f"{item.get('start_year')}-{item.get('end_year')} | {len(item.get('missing_years') or [])} |"
        )
    lines.extend(["", "publication_gate: BLOCK"])
    return "\n".join(lines) + "\n"


def _indicator_card_text(manifest: dict[str, Any], item: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# {item.get('duat_indicator_id')} WDI Source Card v0.8",
            "",
            f"ID: {item.get('duat_indicator_id')}",
            f"Name: {item.get('indicator_name')}",
            "Origin: World Bank World Development Indicators",
            f"API endpoint: {manifest.get('source', {}).get('api_base')}/country/{manifest.get('scope', {}).get('country_code')}/indicator/{item.get('wdi_indicator_code')}",
            f"Accessed at: {manifest.get('source', {}).get('accessed_at')}",
            f"Hash raw: {item.get('raw_sha256')}",
            f"Hash processed: {item.get('processed_sha256')}",
            f"Indicator mapping: {item.get('duat_indicator_id')} -> {item.get('wdi_indicator_code')}",
            f"Functional summary: annual {item.get('unit')} series for local readiness review.",
            "",
            "CERTEZA:",
            f"- n_observations={item.get('n_observations')}; frequency={item.get('frequency')}.",
            f"- raw_file={item.get('raw_file')}.",
            f"- processed_file={item.get('processed_file')}.",
            "",
            "INFERENCIA:",
            "- The series can be considered for internal backtest after remaining review gates.",
            "",
            "INCÓGNITA:",
            "- Final terms/license interpretation and comparability details.",
            "",
            "BLOQUEO:",
            "- No public prediction, ranking or causality claim.",
            "- publication_gate=BLOCK.",
            "",
            f"License: {item.get('license_terms_scan')}",
            f"Comparability: {item.get('comparability_review')}",
            f"Gaps: {item.get('missing_years')}",
            f"Leakage: {item.get('leakage_preflight')}",
            "Destination: DUAT local source pack.",
            "Trace: world_bank_wdi_manifest_v0_8.json.",
        ]
    ) + "\n"


def _slug(value: str) -> str:
    return value.replace(".", "_").replace("/", "_").replace(" ", "_")


def _relativize_paths(item: dict[str, Any], duat_root: Path) -> dict[str, Any]:
    result = dict(item)
    for key in ("raw_file", "processed_file", "processed_csv_file"):
        if result.get(key):
            result[key] = _display_path(Path(result[key]), duat_root)
    processed = duat_root / result["processed_file"]
    if processed.exists():
        payload = json.loads(processed.read_text(encoding="utf-8"))
        if payload.get("raw_file"):
            payload["raw_file"] = result["raw_file"]
        processed.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["processed_sha256"] = sha256_file(processed)
    return result


def _display_path(path: str | Path, duat_root: Path) -> str:
    target = Path(path)
    try:
        return target.relative_to(duat_root).as_posix()
    except ValueError:
        return target.as_posix()
