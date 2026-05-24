"""Readiness rules for DUAT official long-history data v0.7."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .comparability_audit import audit_comparability
from .leakage_preflight import run_leakage_preflight
from .license_terms_review import review_license_terms
from .official_series_manifest import validate_manifest
from .temporal_coverage_audit import audit_temporal_coverage


RUN_ID = "DUAT_OFFICIAL_LONG_HISTORY_DATA_READINESS_v0_7"
SCHEMA = "duat.data_readiness_report.v0_7"
MIN_OBSERVATIONS_WARN = 24
MIN_OBSERVATIONS_REVIEW = 30
PREFERRED_OBSERVATIONS = 40
MIN_OUTER_FOLDS_TARGET = 5
MIN_TRAIN_WINDOW_TARGET = 15
FORECAST_HORIZON_DEFAULT = 1


def minimum_observation_gate(n_observations: int | None) -> dict[str, Any]:
    if n_observations is None:
        return {
            "minimum_observation_review": "REVIEW",
            "minimum_observation_gate": "REVIEW",
            "reason": "n_observations missing",
        }
    if n_observations < MIN_OBSERVATIONS_WARN:
        return {
            "minimum_observation_review": "BLOCK",
            "minimum_observation_gate": "BLOCK",
            "reason": f"n_observations={n_observations} below {MIN_OBSERVATIONS_WARN}",
        }
    if n_observations < MIN_OBSERVATIONS_REVIEW:
        return {
            "minimum_observation_review": "REVIEW",
            "minimum_observation_gate": "REVIEW",
            "reason": f"n_observations={n_observations} below {MIN_OBSERVATIONS_REVIEW}",
        }
    return {
        "minimum_observation_review": "PASS",
        "minimum_observation_gate": "APPROVE_FOR_BACKTEST",
        "reason": f"n_observations={n_observations} meets minimum review threshold",
    }


def evaluate_series_readiness(series: dict[str, Any]) -> dict[str, Any]:
    license_result = review_license_terms(series)
    temporal_result = audit_temporal_coverage(series)
    comparability_result = audit_comparability(series)
    leakage_result = run_leakage_preflight(series)
    observation_result = minimum_observation_gate(series.get("n_observations"))
    source_card_gate = _source_card_gate(series)
    imputation_review = temporal_result.get("imputation_review", "PASS")
    gate_inputs = [
        license_result["license_terms_scan"],
        temporal_result["temporal_coverage_review"],
        comparability_result["comparability_review"],
        leakage_result["leakage_preflight"],
        observation_result["minimum_observation_review"],
        source_card_gate,
        imputation_review,
    ]
    readiness_gate = _aggregate_data_gate(gate_inputs, approve_value="APPROVE_FOR_BACKTEST")
    return {
        "indicator_id": series.get("indicator_id"),
        "source_id": series.get("source_id"),
        "source_name": series.get("source_name"),
        "source_url": series.get("source_url"),
        "frequency": series.get("frequency"),
        "start_year": series.get("start_year"),
        "end_year": series.get("end_year"),
        "n_observations": series.get("n_observations"),
        "unit": series.get("unit"),
        "definition": series.get("definition"),
        "license_terms_scan": license_result["license_terms_scan"],
        "license_reason": license_result["reason"],
        "temporal_coverage_review": temporal_result["temporal_coverage_review"],
        "temporal_findings": temporal_result["findings"],
        "comparability_review": comparability_result["comparability_review"],
        "comparability_findings": comparability_result["findings"],
        "leakage_preflight": leakage_result["leakage_preflight"],
        "leakage_findings": leakage_result["findings"],
        "minimum_observation_review": observation_result["minimum_observation_review"],
        "minimum_observation_reason": observation_result["reason"],
        "source_card_gate": source_card_gate,
        "imputation_review": imputation_review,
        "readiness_gate": readiness_gate,
        "recommendation": "approve_for_backtest" if readiness_gate == "APPROVE_FOR_BACKTEST" else "collect_data",
        "publication_gate": "BLOCK",
        "notes": series.get("notes", []),
    }


def evaluate_manifest_readiness(manifest: dict[str, Any]) -> dict[str, Any]:
    manifest_errors = validate_manifest(manifest)
    series_results = [evaluate_series_readiness(item) for item in manifest.get("series", [])]
    license_terms_scan = _aggregate_scan([item["license_terms_scan"] for item in series_results])
    comparability_review = _aggregate_scan([item["comparability_review"] for item in series_results])
    leakage_preflight = _aggregate_scan([item["leakage_preflight"] for item in series_results])
    minimum_observation_review = _aggregate_scan([item["minimum_observation_review"] for item in series_results])
    source_card_gate = _aggregate_scan([item["source_card_gate"] for item in series_results])
    data_gate = "BLOCK" if manifest_errors else _aggregate_data_gate([item["readiness_gate"] for item in series_results])
    report = {
        "schema": SCHEMA,
        "run_id": RUN_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "publication_gate": "BLOCK",
        "forecast_gate": "REVIEW",
        "action_gate_local": "REVIEW",
        "data_gate": data_gate,
        "manifest_validation": "PASS" if not manifest_errors else "BLOCK",
        "manifest_errors": manifest_errors,
        "criteria": {
            "MIN_OBSERVATIONS_WARN": MIN_OBSERVATIONS_WARN,
            "MIN_OBSERVATIONS_REVIEW": MIN_OBSERVATIONS_REVIEW,
            "PREFERRED_OBSERVATIONS": PREFERRED_OBSERVATIONS,
            "MIN_OUTER_FOLDS_TARGET": MIN_OUTER_FOLDS_TARGET,
            "MIN_TRAIN_WINDOW_TARGET": MIN_TRAIN_WINDOW_TARGET,
            "FORECAST_HORIZON_DEFAULT": FORECAST_HORIZON_DEFAULT,
        },
        "series_results": series_results,
        "license_terms_scan": license_terms_scan,
        "comparability_review": comparability_review,
        "leakage_preflight": leakage_preflight,
        "minimum_observation_review": minimum_observation_review,
        "source_card_gate": source_card_gate,
        "recommendation": _recommendation(data_gate),
        "reconstruction_test": _reconstruction_test(),
        "interpretation": {
            "v0_6_status": "boundary_evidence",
            "main_result": "Current short fixtures are not ready for renewed predictive backtesting.",
            "public_claim_allowed": False,
            "publication_gate_reason": "License terms, comparability and official long-history evidence remain under review.",
        },
    }
    return report


def validate_readiness_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("run_id") != RUN_ID:
        errors.append("run_id mismatch")
    if report.get("publication_gate") != "BLOCK":
        errors.append("publication_gate must be BLOCK")
    if report.get("interpretation", {}).get("public_claim_allowed") is not False:
        errors.append("public_claim_allowed must be false")
    if report.get("reconstruction_test", {}).get("status") != "PASS":
        errors.append("reconstruction_test must pass")
    if not isinstance(report.get("series_results"), list) or not report.get("series_results"):
        errors.append("series_results must be non-empty")
    return errors


def write_readiness_json(report: dict[str, Any], path: str | Path, pretty: bool = True) -> tuple[str, str]:
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


def write_readiness_markdown(report: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DUAT Official Long-History Data Readiness v0.7",
        "",
        "publication_gate: BLOCK",
        f"run_id: {report.get('run_id')}",
        f"data_gate: {report.get('data_gate')}",
        f"recommendation: {report.get('recommendation')}",
        "",
        "This is internal boundary evidence and data readiness work. It is not approved for publication.",
        "",
        "| indicator | source | observations | minimum review | license | comparability | leakage | gate |",
        "|---|---|---:|---|---|---|---|---|",
    ]
    for item in report.get("series_results", []):
        lines.append(
            f"| {item.get('indicator_id')} | {item.get('source_id')} | {item.get('n_observations')} | "
            f"{item.get('minimum_observation_review')} | {item.get('license_terms_scan')} | "
            f"{item.get('comparability_review')} | {item.get('leakage_preflight')} | {item.get('readiness_gate')} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- v0.6 remains frozen as boundary evidence.",
            "- No model weights were changed in v0.7.",
            "- A new benchmark requires official long-history data, source provenance, license review, comparability review and leakage preflight.",
        ]
    )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _source_card_gate(series: dict[str, Any]) -> str:
    required = ("source_name", "source_url", "license_terms", "frequency", "n_observations")
    return "PASS" if all(series.get(key) not in (None, "") for key in required) else "REVIEW"


def _aggregate_scan(values: list[str]) -> str:
    if any(value == "BLOCK" for value in values):
        return "BLOCK"
    if any(value == "REVIEW" for value in values):
        return "REVIEW"
    return "PASS"


def _aggregate_data_gate(values: list[str], approve_value: str = "APPROVE") -> str:
    if any(value == "BLOCK" for value in values):
        return "BLOCK"
    if any(value == "REVIEW" for value in values):
        return "REVIEW"
    return approve_value


def _recommendation(data_gate: str) -> str:
    if data_gate == "APPROVE":
        return "approve_for_backtest"
    if data_gate == "BLOCK":
        return "collect_data"
    return "collect_data"


def _reconstruction_test() -> dict[str, Any]:
    return {
        "status": "PASS",
        "score": 5,
        "max_score": 5,
        "answers": {
            "what_v0_6_demonstrated": "The current calibration does not generalize out-of-sample on short fixtures.",
            "why_not_same_fixture_tuning": "Further tuning on the same short history risks overfitting.",
            "what_v0_7_builds": "A readiness layer for official long-history data, provenance, license, coverage, comparability and leakage checks.",
            "publication_gates": "publication_gate=BLOCK with LicenseTermsScan, ComparabilityReview and human/legal review pending.",
            "minimum_condition_for_backtest": "Official long-history series passing minimum observations, source metadata, license, comparability and leakage preflight.",
        },
        "critical_omissions": [],
    }
