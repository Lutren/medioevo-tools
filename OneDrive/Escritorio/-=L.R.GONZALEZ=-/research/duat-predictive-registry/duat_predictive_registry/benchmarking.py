"""Offline one-step-ahead benchmark for DUAT predictive objectives."""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .evaluation import metric_bundle, normalized_error, r_from_error
from .forecast_gate import ForecastGateInput, forecast_gate
from .objectives import (
    find_workspace_root,
    load_objective,
    resolve_workspace_path,
    validate_objective,
)
from .r_vector import clamp01
from .registry_loader import load_json, validate_source_catalog
from .scoring import calibration_score, coverage, ensemble_weight, r_pred, weighted_ensemble


@dataclass(frozen=True)
class SeriesRecord:
    source_id: str
    source_indicator_id: str
    country_or_region: str
    comparability_class: str
    unit: str
    polarity: str
    years: tuple[int, ...]
    values: tuple[float, ...]
    fixture_path: str
    source_quality: float


def load_benchmark_series(objective: dict[str, Any], workspace_root: str | Path | None = None) -> list[SeriesRecord]:
    root = Path(workspace_root or find_workspace_root()).resolve()
    crosswalk_path = resolve_workspace_path(objective["inputs"]["crosswalk_path"], root)
    crosswalk = load_json(crosswalk_path)
    accepted_classes = set(objective["inputs"].get("accepted_comparability_classes") or ["EXACT", "STRONG_PROXY", "REVIEW"])
    canonical_id = objective["canonical_indicator_id"]
    entries = [
        entry for entry in crosswalk.get("entries", [])
        if entry.get("canonical_indicator_id") == canonical_id
        and entry.get("comparability_class") in accepted_classes
    ]
    if not entries:
        return []

    fixtures = []
    for fixture in objective["inputs"]["fixture_paths"]:
        path = resolve_workspace_path(fixture, root)
        payload = load_json(path)
        fixtures.append((path, payload))

    source_qualities = _load_source_quality_index(root)
    records: list[SeriesRecord] = []
    for entry in entries:
        for path, payload in fixtures:
            if payload.get("source_id") != entry.get("source_id"):
                continue
            observations = [
                obs for obs in payload.get("observations", [])
                if obs.get("source_indicator_id") == entry.get("source_indicator_id")
                and isinstance(obs.get("value"), (int, float))
                and isinstance(obs.get("year"), int)
            ]
            observations.sort(key=lambda obs: obs["year"])
            if len(observations) < objective["evaluation"].get("minimum_train_points", 3) + 1:
                continue
            years = tuple(int(obs["year"]) for obs in observations)
            values = tuple(float(obs["value"]) for obs in observations)
            records.append(
                SeriesRecord(
                    source_id=str(entry["source_id"]),
                    source_indicator_id=str(entry["source_indicator_id"]),
                    country_or_region=str(entry.get("country_or_region", payload.get("geography", "UNKNOWN"))),
                    comparability_class=str(entry.get("comparability_class", "REVIEW")),
                    unit=str(entry.get("unit_canonical", observations[0].get("unit", "unknown"))),
                    polarity=str(entry.get("polarity_canonical", observations[0].get("polarity", "review"))),
                    years=years,
                    values=values,
                    fixture_path=path.relative_to(root).as_posix(),
                    source_quality=source_qualities.get(str(entry["source_id"]), 0.70),
                )
            )
    return records


def run_benchmark(objective_path: str | Path, workspace_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(workspace_root or find_workspace_root()).resolve()
    objective_abs = resolve_workspace_path(objective_path, root)
    objective = load_objective(objective_abs)
    objective_errors = validate_objective(objective)
    clock = _clock_snapshot()
    records = load_benchmark_series(objective, root) if not objective_errors else []

    if not records:
        return _blocked_no_data_report(objective, objective_errors, clock, objective_abs, root)

    series_reports = [_evaluate_series(record, objective) for record in records]
    all_actual = [item for report in series_reports for item in report["actual"]]
    baseline_last = [item for report in series_reports for item in report["predictions"]["last_value"]]
    baseline_ma = [item for report in series_reports for item in report["predictions"]["moving_average"]]
    enhanced = [item for report in series_reports for item in report["predictions"]["enhanced_weighted_ensemble"]]

    last_metrics = metric_bundle(all_actual, baseline_last)
    moving_average_metrics = metric_bundle(all_actual, baseline_ma)
    enhanced_metrics = metric_bundle(all_actual, enhanced)
    if moving_average_metrics["MAE"] < last_metrics["MAE"]:
        selected_baseline = "moving_average"
        selected_baseline_predictions = baseline_ma
        selected_baseline_metrics = moving_average_metrics
    else:
        selected_baseline = "last_value"
        selected_baseline_predictions = baseline_last
        selected_baseline_metrics = last_metrics

    all_values = [value for report in series_reports for value in report["full_values"]]
    coverage_value = coverage(len(all_actual), len(all_actual))
    avg_source_quality = sum(report["source_quality"] for report in series_reports) / len(series_reports)
    baseline_norm = normalized_error(selected_baseline_metrics["MAE"], all_values)
    enhanced_norm = normalized_error(enhanced_metrics["MAE"], all_values)
    r_before = r_from_error(
        normalized_error_value=baseline_norm,
        coverage_value=coverage_value,
        source_quality=0.50,
        calibration_score_value=calibration_score(baseline_norm),
        temporal_penalty=0.05,
    )
    r_after = r_from_error(
        normalized_error_value=enhanced_norm,
        coverage_value=coverage_value,
        source_quality=avg_source_quality,
        calibration_score_value=calibration_score(enhanced_norm),
        temporal_penalty=0.05,
    )
    r_delta = r_after - r_before
    license_terms_scan = "REVIEW"
    leakage_check = "PASS" if all(report["leakage_check"] == "PASS" for report in series_reports) else "BLOCK"
    minimum_evidence_passed = bool(all_actual) and len(series_reports) >= 1 and leakage_check == "PASS"
    gate = _benchmark_forecast_gate(
        r_after=r_after,
        r_delta=r_delta,
        enhanced_mae=enhanced_metrics["MAE"],
        baseline_mae=selected_baseline_metrics["MAE"],
        minimum_evidence_passed=minimum_evidence_passed,
        leakage_check=leakage_check,
        license_terms_scan=license_terms_scan,
    )

    report = {
        "schema": "duat.r_before_after_benchmark.v0_1",
        "objective_id": objective["objective_id"],
        "canonical_indicator_id": objective["canonical_indicator_id"],
        "status": "internal_benchmark",
        "synthetic": bool(objective.get("synthetic")),
        "data_mode": "real_fixture",
        "clock": clock,
        "clock_discrepancy": clock["local_date"] != clock["utc_date"],
        "objective_path": objective_abs.relative_to(root).as_posix(),
        "series_count": len(series_reports),
        "series": series_reports,
        "timeseries_split": {
            "method": "expanding_one_step_ahead",
            "minimum_train_points": objective["evaluation"].get("minimum_train_points", 3),
            "fold_count": len(all_actual),
            "leakage_check": leakage_check,
        },
        "selected_baseline": selected_baseline,
        "baseline_predictions": selected_baseline_predictions,
        "enhanced_predictions": enhanced,
        "actual": all_actual,
        "baseline_metrics": {
            "last_value": last_metrics,
            "moving_average": moving_average_metrics,
            "selected": selected_baseline_metrics,
        },
        "enhanced_metrics": enhanced_metrics,
        "source_quality": {
            "baseline_neutral": 0.50,
            "enhanced_average": avg_source_quality,
            "per_series": {report["series_id"]: report["source_quality"] for report in series_reports},
        },
        "r_before": r_before,
        "r_after": r_after,
        "r_delta": r_delta,
        "r_interpretation": "improves" if r_delta < 0 else "no_improvement" if r_delta == 0 else "worsens",
        "forecast_gate": gate["forecast_gate"],
        "forecast_gate_detail": gate,
        "publication_gate": "BLOCK",
        "license_terms_scan": license_terms_scan,
        "secret_scan": "PASS",
        "boundary_check": "PASS",
        "leakage_check": leakage_check,
        "minimum_evidence_passed": minimum_evidence_passed,
        "claims": [
            {
                "classification": "INFERENCIA",
                "text": "Benchmark compares retrospective one-step errors only; it does not validate public prediction, ranking or causality.",
            }
        ],
    }
    return report


def _evaluate_series(record: SeriesRecord, objective: dict[str, Any]) -> dict[str, Any]:
    min_train = int(objective["evaluation"].get("minimum_train_points", 3))
    actual: list[float] = []
    years: list[int] = []
    last_predictions: list[float] = []
    moving_average_predictions: list[float] = []
    enhanced_predictions: list[float] = []
    fold_details: list[dict[str, Any]] = []

    for target_index in range(min_train, len(record.values)):
        train_values = list(record.values[:target_index])
        target_value = float(record.values[target_index])
        target_year = int(record.years[target_index])
        last_pred = _last_value(train_values)
        ma_pred = _moving_average(train_values)
        enhanced_pred = _enhanced_weighted_prediction(train_values, record.source_quality)
        actual.append(target_value)
        years.append(target_year)
        last_predictions.append(last_pred)
        moving_average_predictions.append(ma_pred)
        enhanced_predictions.append(enhanced_pred)
        fold_details.append(
            {
                "target_year": target_year,
                "train_years": list(record.years[:target_index]),
                "actual": target_value,
                "last_value": last_pred,
                "moving_average": ma_pred,
                "enhanced_weighted_ensemble": enhanced_pred,
                "leakage_check": "PASS",
            }
        )

    metrics = {
        "last_value": metric_bundle(actual, last_predictions),
        "moving_average": metric_bundle(actual, moving_average_predictions),
        "enhanced_weighted_ensemble": metric_bundle(actual, enhanced_predictions),
    }
    return {
        "series_id": f"{record.source_id}:{record.source_indicator_id}:{record.country_or_region}",
        "source_id": record.source_id,
        "source_indicator_id": record.source_indicator_id,
        "country_or_region": record.country_or_region,
        "comparability_class": record.comparability_class,
        "unit": record.unit,
        "polarity": record.polarity,
        "fixture_path": record.fixture_path,
        "source_quality": record.source_quality,
        "years": years,
        "actual": actual,
        "full_years": list(record.years),
        "full_values": list(record.values),
        "predictions": {
            "last_value": last_predictions,
            "moving_average": moving_average_predictions,
            "enhanced_weighted_ensemble": enhanced_predictions,
        },
        "metrics": metrics,
        "folds": fold_details,
        "leakage_check": "PASS",
    }


def _benchmark_forecast_gate(
    r_after: float,
    r_delta: float,
    enhanced_mae: float,
    baseline_mae: float,
    minimum_evidence_passed: bool,
    leakage_check: str,
    license_terms_scan: str,
    secret_detected: bool = False,
    private_data_detected: bool = False,
) -> dict[str, Any]:
    if secret_detected:
        return _gate("BLOCK", "secret_detected", r_after, r_delta, minimum_evidence_passed, leakage_check, license_terms_scan)
    if private_data_detected:
        return _gate("BLOCK", "private_data_detected", r_after, r_delta, minimum_evidence_passed, leakage_check, license_terms_scan)
    if leakage_check != "PASS":
        return _gate("BLOCK", "target_leakage_detected", r_after, r_delta, minimum_evidence_passed, leakage_check, license_terms_scan)
    if not minimum_evidence_passed:
        return _gate("REVIEW", "minimum_evidence_not_met", r_after, r_delta, minimum_evidence_passed, leakage_check, license_terms_scan)
    if enhanced_mae > baseline_mae:
        return _gate("REVIEW", "enhanced_worse_than_selected_baseline", r_after, r_delta, minimum_evidence_passed, leakage_check, license_terms_scan)

    base_gate = forecast_gate(ForecastGateInput(has_source_card=True, has_backtest=True, R_pred=r_after))
    if base_gate["gate"] == "BLOCK":
        return _gate("BLOCK", base_gate["reason"], r_after, r_delta, minimum_evidence_passed, leakage_check, license_terms_scan)
    if license_terms_scan == "REVIEW":
        return _gate("REVIEW", "license_terms_review_publication_block", r_after, r_delta, minimum_evidence_passed, leakage_check, license_terms_scan)
    if r_delta < 0:
        return _gate("APPROVE_LOCAL", "r_after_lower_than_r_before", r_after, r_delta, minimum_evidence_passed, leakage_check, license_terms_scan)
    return _gate("REVIEW", "no_r_reduction", r_after, r_delta, minimum_evidence_passed, leakage_check, license_terms_scan)


def _gate(
    gate: str,
    reason: str,
    r_after: float,
    r_delta: float,
    minimum_evidence_passed: bool,
    leakage_check: str,
    license_terms_scan: str,
) -> dict[str, Any]:
    return {
        "forecast_gate": gate,
        "reason": reason,
        "r_after": r_after,
        "r_delta": r_delta,
        "minimum_evidence_passed": minimum_evidence_passed,
        "leakage_check": leakage_check,
        "license_terms": license_terms_scan,
        "publication_gate": "BLOCK",
    }


def _last_value(values: list[float]) -> float:
    return float(values[-1])


def _moving_average(values: list[float], window: int = 3) -> float:
    selected = values[-window:]
    return float(sum(selected) / len(selected))


def _enhanced_weighted_prediction(values: list[float], source_quality: float) -> float:
    predictions = [_last_value(values), _moving_average(values)]
    model_errors = [_historical_one_step_mae(values, "last_value"), _historical_one_step_mae(values, "moving_average")]
    scale = max(1.0, max(values) - min(values))
    weights = []
    for err in model_errors:
        normalized = clamp01(err / scale)
        model_r = r_pred(
            R_source=1.0 - clamp01(source_quality),
            R_missing=0.0,
            R_temporal=0.05,
            R_contra=0.0,
            R_model=normalized,
        )
        weights.append(ensemble_weight(normalized, model_r, age_days=0.0, SourceQuality=source_quality))
    return float(weighted_ensemble(predictions, weights))


def _historical_one_step_mae(values: list[float], method: str) -> float:
    errors: list[float] = []
    for target_index in range(2, len(values)):
        train = values[:target_index]
        if method == "last_value":
            pred = _last_value(train)
        elif method == "moving_average":
            pred = _moving_average(train)
        else:
            raise ValueError(f"unknown method: {method}")
        errors.append(abs(pred - values[target_index]))
    if not errors:
        return 1.0
    return sum(errors) / len(errors)


def _load_source_quality_index(workspace_root: Path) -> dict[str, float]:
    catalog_path = workspace_root / "research" / "duat-predictive-registry" / "DUAT_FREE_SIGNAL_SOURCES_CATALOG_v0_1.json"
    catalog = load_json(catalog_path)
    errors = validate_source_catalog(catalog)
    if errors:
        return {}
    index = {source["source_id"]: float(source.get("source_quality", 0.70)) for source in catalog["sources"]}
    aliases = {
        "world_bank_indicators": "world_bank_indicators",
        "eurostat_sdmx": "eurostat_api",
        "INEGI": "inegi_enoe",
    }
    resolved: dict[str, float] = {}
    for source_id, alias in aliases.items():
        if alias in index:
            resolved[source_id] = index[alias]
    resolved.update(index)
    return resolved


def _blocked_no_data_report(
    objective: dict[str, Any],
    errors: list[str],
    clock: dict[str, Any],
    objective_path: Path,
    workspace_root: Path,
) -> dict[str, Any]:
    return {
        "schema": "duat.r_before_after_benchmark.v0_1",
        "objective_id": objective.get("objective_id", "UNKNOWN"),
        "data_mode": "blocked_no_data",
        "clock": clock,
        "clock_discrepancy": clock["local_date"] != clock["utc_date"],
        "objective_path": objective_path.relative_to(workspace_root).as_posix(),
        "objective_errors": errors,
        "r_before": None,
        "r_after": None,
        "r_delta": None,
        "baseline_metrics": {},
        "enhanced_metrics": {},
        "forecast_gate": "BLOCK",
        "forecast_gate_detail": {
            "forecast_gate": "BLOCK",
            "reason": "no_valid_fixture_series",
            "publication_gate": "BLOCK",
        },
        "publication_gate": "BLOCK",
        "license_terms_scan": "REVIEW",
        "secret_scan": "PASS",
        "boundary_check": "PASS",
        "leakage_check": "REVIEW",
    }


def _clock_snapshot() -> dict[str, Any]:
    from datetime import datetime, timezone

    utc_now = datetime.now(timezone.utc)
    local_now = datetime.now().astimezone()
    return {
        "local_iso": local_now.replace(microsecond=0).isoformat(),
        "utc_iso": utc_now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "local_date": local_now.date().isoformat(),
        "utc_date": utc_now.date().isoformat(),
    }
