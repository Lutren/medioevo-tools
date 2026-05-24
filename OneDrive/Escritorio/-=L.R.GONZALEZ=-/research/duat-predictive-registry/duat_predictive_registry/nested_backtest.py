"""Nested walk-forward backtest for DUAT domain calibration v0.6."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .backtest_leakage_guard import aggregate_leakage_checks, check_nested_fold_leakage, check_series_temporal_order
from .domain_profiles import infer_domain
from .evaluation import metric_bundle, normalized_error, r_from_error
from .out_of_sample_gate import out_of_sample_gate
from .r_vector import clamp01
from .walk_forward import generate_nested_walk_forward_folds


RUN_ID = "DUAT_NESTED_DOMAIN_BACKTEST_v0_6"
SCHEMA = "duat.nested_domain_backtest.v0_6"

GRID = {
    "moving_average_windows": [2, 3, 4, 5],
    "ensemble_weights": [0.25, 0.5, 0.75],
    "domain_lambdas": {
        "economy": [0.25, 0.35, 0.45],
        "labor_market": [0.35, 0.45, 0.55],
        "demography": [0.30, 0.40, 0.50],
        "unknown": [0.40, 0.50, 0.60],
    },
}


def run_nested_domain_backtest(
    objectives: list[dict[str, Any]],
    matrix_v0_4: dict[str, Any],
    metric_aligned_v0_5: dict[str, Any],
    min_observations: int = 8,
    outer_min_train_size: int = 5,
    inner_min_train_size: int = 4,
    horizon: int = 1,
) -> dict[str, Any]:
    """Run nested walk-forward calibration over existing offline fixture reports."""

    metric_by_indicator = {item.get("indicator"): item for item in metric_aligned_v0_5.get("objectives", [])}
    raw_by_indicator = {report.get("canonical_indicator_id"): report for report in matrix_v0_4.get("raw_reports", [])}
    rows = []
    for objective in objectives:
        indicator = objective.get("indicator")
        raw_report = raw_by_indicator.get(indicator)
        aligned = metric_by_indicator.get(indicator, {})
        rows.append(
            _run_objective_nested_backtest(
                objective,
                raw_report,
                aligned,
                min_observations=min_observations,
                outer_min_train_size=outer_min_train_size,
                inner_min_train_size=inner_min_train_size,
                horizon=horizon,
            )
        )
    report = {
        "schema": SCHEMA,
        "run_id": RUN_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "publication_gate": "BLOCK",
        "action_gate_local": _action_gate(rows),
        "parameters": {
            "min_observations": min_observations,
            "outer_min_train_size": outer_min_train_size,
            "inner_min_train_size": inner_min_train_size,
            "horizon": horizon,
            "grid": GRID,
        },
        "source_runs": {
            "matrix_v0_4": matrix_v0_4.get("run_id"),
            "metric_aligned_v0_5": metric_aligned_v0_5.get("run_id"),
        },
        "objectives": rows,
        "summary": _summary(rows),
        "interpretation": {
            "main_result": _main_result(rows),
            "public_claim_allowed": False,
            "publication_gate_reason": "LicenseTermsScan/ComparabilityReview/human legal review pending.",
            "claim_level": "internal_technical_evidence_only",
        },
        "scans": {
            "LicenseTermsScan": "REVIEW",
            "LeakageCheck": "PASS" if all(row.get("leakage_check") == "PASS" for row in rows) else "BLOCK",
            "BacktestLeakageGuard": "PASS" if all(row.get("backtest_leakage_guard", {}).get("leakage_check") == "PASS" for row in rows) else "BLOCK",
            "PublicationGateScan": "PASS",
            "ComparabilityReview": "REVIEW" if any(row.get("comparability_status") != "PASS" for row in rows) else "PASS",
        },
    }
    return report


def validate_nested_backtest_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("run_id") != RUN_ID:
        errors.append("run_id mismatch")
    if report.get("publication_gate") != "BLOCK":
        errors.append("publication_gate must be BLOCK")
    if report.get("interpretation", {}).get("public_claim_allowed") is not False:
        errors.append("public_claim_allowed must be false")
    objectives = report.get("objectives")
    if not isinstance(objectives, list) or not objectives:
        errors.append("objectives must be a non-empty list")
    else:
        for item in objectives:
            if item.get("claim_allowed_public") is not False:
                errors.append(f"{item.get('indicator')} public claim must be false")
            if item.get("publication_gate") != "BLOCK":
                errors.append(f"{item.get('indicator')} publication_gate must be BLOCK")
            if item.get("backtest_leakage_guard", {}).get("leakage_check") != "PASS":
                errors.append(f"{item.get('indicator')} leakage guard must be PASS")
    return errors


def write_nested_backtest_json(report: dict[str, Any], path: str | Path, pretty: bool = True) -> tuple[str, str]:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    clean = dict(report)
    clean.pop("sha256", None)
    clean.pop("file_sha256", None)
    payload = json.dumps(clean, ensure_ascii=False, sort_keys=True).encode("utf-8")
    clean["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    clean["sha256_scope"] = "canonical_json_without_sha256_fields"
    target.write_text(json.dumps(clean, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    return clean["payload_sha256"], hashlib.sha256(target.read_bytes()).hexdigest()


def write_nested_backtest_markdown(report: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DUAT Nested Domain Backtest v0.6",
        "",
        "publication_gate: BLOCK",
        f"run_id: {report.get('run_id')}",
        f"action_gate_local: {report.get('action_gate_local')}",
        "",
        "nested backtest is internal technical evidence only.",
        "R reduction does not equal predictive validation.",
        "",
        "| indicator | observations | outer folds | OOS classification | MAE delta | RMSE delta | R aligned delta | gate |",
        "|---|---:|---:|---|---:|---:|---:|---|",
    ]
    for item in report.get("objectives", []):
        delta = item.get("metric_delta_outer") or {}
        lines.append(
            f"| {item.get('indicator')} | {item.get('n_observations')} | {item.get('n_outer_folds')} | "
            f"{item.get('oos_classification')} | {delta.get('MAE')} | {delta.get('RMSE')} | "
            f"{item.get('r_aligned_delta_outer')} | {item.get('out_of_sample_gate')} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Walk-forward validation uses only past data for configuration selection.",
            "- Outer test folds are never used to select parameters.",
            "- LicenseTermsScan and ComparabilityReview remain gates for publication.",
            "- No external prediction, causal assertion or social ordering claim is authorized.",
        ]
    )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _run_objective_nested_backtest(
    objective: dict[str, Any],
    raw_report: dict[str, Any] | None,
    aligned_v0_5: dict[str, Any],
    *,
    min_observations: int,
    outer_min_train_size: int,
    inner_min_train_size: int,
    horizon: int,
) -> dict[str, Any]:
    indicator = objective.get("indicator")
    domain = aligned_v0_5.get("domain") or infer_domain(indicator)
    data_mode = objective.get("data_mode", aligned_v0_5.get("data_mode", "blocked_no_data"))
    comparability_status = aligned_v0_5.get("comparability_status", "REVIEW")
    license_terms_scan = aligned_v0_5.get("license_terms_scan", objective.get("license_terms_scan", "REVIEW"))
    leakage_check = objective.get("leakage_check", aligned_v0_5.get("leakage_check", "REVIEW"))
    if not raw_report:
        return _blocked_objective(objective, domain, data_mode, "missing_raw_report")

    series = _series_records(raw_report)
    n_observations = sum(len(item["values"]) for item in series)
    leakage_checks = [check_series_temporal_order(item["years"]) for item in series]
    if n_observations < min_observations:
        gate = out_of_sample_gate(
            data_mode=data_mode,
            leakage_check="PASS",
            comparability_status=comparability_status,
            license_terms_scan=license_terms_scan,
            n_outer_folds=0,
            metric_delta_outer={},
            r_aligned_delta_outer=None,
            insufficient_data=True,
        )
        return _objective_payload(
            objective,
            domain,
            data_mode,
            n_observations,
            0,
            [],
            {},
            {},
            {},
            None,
            None,
            aggregate_leakage_checks(leakage_checks),
            gate,
            comparability_status,
            license_terms_scan,
            leakage_check,
        )

    actual: list[float] = []
    baseline_pred: list[float] = []
    calibrated_pred: list[float] = []
    selected_configs: list[dict[str, Any]] = []
    all_nested_folds: list[dict[str, Any]] = []
    source_qualities: list[float] = []
    for series_index, item in enumerate(series):
        source_qualities.append(float(item.get("source_quality", 0.75)))
        nested_folds = generate_nested_walk_forward_folds(
            item["values"],
            outer_min_train_size=outer_min_train_size,
            inner_min_train_size=inner_min_train_size,
            horizon=horizon,
        )
        for fold_index, fold in enumerate(nested_folds):
            if not fold["inner_folds"]:
                continue
            config, inner_summary = _select_config(item["values"], fold["inner_folds"], domain, item.get("source_quality", 0.75))
            fold = dict(fold)
            fold["selected_config"] = {**config, "uses_outer_test": False}
            all_nested_folds.append(fold)
            test_index = fold["outer_test_indices"][0]
            train_values = [item["values"][idx] for idx in fold["outer_train_indices"]]
            actual_value = item["values"][test_index]
            baseline_value = train_values[-1]
            calibrated_value = _predict(train_values, config["window"], config["last_value_weight"])
            actual.append(actual_value)
            baseline_pred.append(baseline_value)
            calibrated_pred.append(calibrated_value)
            selected_configs.append(
                {
                    "series_id": item.get("series_id"),
                    "series_index": series_index,
                    "outer_fold_index": fold_index,
                    "target_time": item["years"][test_index],
                    "selected_config": config,
                    "inner_folds": len(fold["inner_folds"]),
                    "inner_selection_score": inner_summary["score"],
                    "outer_test_used_for_selection": False,
                }
            )
    leakage_checks.append(check_nested_fold_leakage(all_nested_folds))
    leakage_guard = aggregate_leakage_checks(leakage_checks)
    n_outer_folds = len(actual)
    if n_outer_folds == 0:
        gate = out_of_sample_gate(
            data_mode=data_mode,
            leakage_check=leakage_guard["leakage_check"],
            comparability_status=comparability_status,
            license_terms_scan=license_terms_scan,
            n_outer_folds=0,
            metric_delta_outer={},
            r_aligned_delta_outer=None,
            insufficient_data=True,
        )
        return _objective_payload(
            objective,
            domain,
            data_mode,
            n_observations,
            0,
            selected_configs,
            {},
            {},
            {},
            None,
            None,
            leakage_guard,
            gate,
            comparability_status,
            license_terms_scan,
            leakage_check,
        )

    baseline_metrics = metric_bundle(actual, baseline_pred)
    calibrated_metrics = metric_bundle(actual, calibrated_pred)
    metric_delta = _metric_delta(baseline_metrics, calibrated_metrics)
    source_quality = sum(source_qualities) / len(source_qualities) if source_qualities else 0.75
    r_before = _r_from_metrics(baseline_metrics, actual, source_quality)
    r_after = _r_from_metrics(calibrated_metrics, actual, source_quality)
    r_operational_delta = r_after - r_before
    r_after_aligned = _aligned_r_after(r_before, r_after, baseline_metrics, calibrated_metrics, domain)
    r_aligned_delta = r_after_aligned - r_before
    gate = out_of_sample_gate(
        data_mode=data_mode,
        leakage_check=leakage_guard["leakage_check"],
        comparability_status=comparability_status,
        license_terms_scan=license_terms_scan,
        n_outer_folds=n_outer_folds,
        metric_delta_outer=metric_delta,
        r_aligned_delta_outer=r_aligned_delta,
        insufficient_data=False,
    )
    return _objective_payload(
        objective,
        domain,
        data_mode,
        n_observations,
        n_outer_folds,
        selected_configs,
        baseline_metrics,
        calibrated_metrics,
        metric_delta,
        r_operational_delta,
        r_aligned_delta,
        leakage_guard,
        gate,
        comparability_status,
        license_terms_scan,
        leakage_check,
        n_inner_folds_mean=sum(item["inner_folds"] for item in selected_configs) / len(selected_configs) if selected_configs else 0,
    )


def _series_records(raw_report: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for series in raw_report.get("series", []):
        years = list(series.get("full_years") or [])
        values = [float(value) for value in series.get("full_values") or []]
        pairs = sorted(zip(years, values), key=lambda item: item[0])
        records.append(
            {
                "series_id": series.get("series_id"),
                "years": [year for year, _ in pairs],
                "values": [value for _, value in pairs],
                "source_quality": series.get("source_quality", 0.75),
            }
        )
    return records


def _select_config(values: list[float], inner_folds: list[dict[str, list[int]]], domain: str, source_quality: float) -> tuple[dict[str, Any], dict[str, float]]:
    candidates: list[dict[str, Any]] = []
    for window in GRID["moving_average_windows"]:
        for weight in GRID["ensemble_weights"]:
            for domain_lambda in GRID["domain_lambdas"].get(domain, GRID["domain_lambdas"]["unknown"]):
                actual: list[float] = []
                predicted: list[float] = []
                baseline: list[float] = []
                for fold in inner_folds:
                    train_values = [values[idx] for idx in fold["train_indices"]]
                    validation_index = fold["validation_indices"][0]
                    actual_value = values[validation_index]
                    actual.append(actual_value)
                    predicted.append(_predict(train_values, window, weight))
                    baseline.append(train_values[-1])
                metrics = metric_bundle(actual, predicted)
                baseline_metrics = metric_bundle(actual, baseline)
                scale_values = [values[idx] for fold in inner_folds for idx in fold["train_indices"] + fold["validation_indices"]]
                norm_mae = normalized_error(metrics["MAE"], scale_values)
                norm_rmse = normalized_error(metrics["RMSE"], scale_values)
                r_after = _r_from_metrics(metrics, actual, source_quality)
                r_before = _r_from_metrics(baseline_metrics, actual, source_quality)
                r_aligned = _aligned_r_after(r_before, r_after, baseline_metrics, metrics, domain, domain_lambda)
                score = 0.45 * norm_mae + 0.45 * norm_rmse + 0.10 * r_aligned
                candidates.append(
                    {
                        "window": window,
                        "last_value_weight": weight,
                        "domain_lambda": domain_lambda,
                        "score": score,
                        "metrics": metrics,
                        "uses_outer_test": False,
                    }
                )
    best = min(candidates, key=lambda item: (item["score"], item["metrics"]["MAE"], item["metrics"]["RMSE"]))
    config = {
        "window": best["window"],
        "last_value_weight": best["last_value_weight"],
        "domain_lambda": best["domain_lambda"],
    }
    return config, {"score": best["score"]}


def _predict(train_values: list[float], window: int, last_value_weight: float) -> float:
    selected = train_values[-window:] if len(train_values) >= window else train_values
    moving_average = sum(selected) / len(selected)
    return last_value_weight * train_values[-1] + (1.0 - last_value_weight) * moving_average


def _metric_delta(baseline: dict[str, Any], calibrated: dict[str, Any]) -> dict[str, Any]:
    result = {
        "MAE": calibrated.get("MAE") - baseline.get("MAE"),
        "RMSE": calibrated.get("RMSE") - baseline.get("RMSE"),
    }
    base_mape = baseline.get("MAPE_if_safe", {}).get("value")
    calibrated_mape = calibrated.get("MAPE_if_safe", {}).get("value")
    if base_mape is None or calibrated_mape is None:
        result["MAPE_if_safe"] = None
        result["mape_status"] = "SKIPPED_UNSAFE_DENOMINATOR"
    else:
        result["MAPE_if_safe"] = calibrated_mape - base_mape
        result["mape_status"] = "PASS"
    return result


def _r_from_metrics(metrics: dict[str, Any], values: list[float], source_quality: float) -> float:
    norm = normalized_error(metrics.get("MAE", 1.0), values)
    return r_from_error(
        normalized_error_value=norm,
        coverage_value=1.0,
        source_quality=source_quality,
        calibration_score_value=1.0 - norm,
        temporal_penalty=0.10,
    )


def _aligned_r_after(
    r_before: float,
    r_after: float,
    baseline_metrics: dict[str, Any],
    calibrated_metrics: dict[str, Any],
    domain: str,
    domain_lambda: float | None = None,
) -> float:
    lambda_value = domain_lambda if domain_lambda is not None else _default_lambda(domain)
    mae_base = baseline_metrics.get("MAE")
    mae_cal = calibrated_metrics.get("MAE")
    rmse_base = baseline_metrics.get("RMSE")
    rmse_cal = calibrated_metrics.get("RMSE")
    degradation = 0.0
    if mae_base not in (None, 0):
        degradation += 0.5 * max(0.0, (mae_cal - mae_base) / max(abs(mae_base), 1e-9))
    if rmse_base not in (None, 0):
        degradation += 0.5 * max(0.0, (rmse_cal - rmse_base) / max(abs(rmse_base), 1e-9))
    aligned = clamp01(r_after + clamp01(lambda_value * degradation))
    if mae_cal is not None and rmse_cal is not None and mae_base is not None and rmse_base is not None:
        if mae_cal > mae_base and rmse_cal > rmse_base:
            aligned = max(aligned, r_before)
    return aligned


def _default_lambda(domain: str) -> float:
    return {
        "economy": 0.35,
        "labor_market": 0.45,
        "demography": 0.40,
        "health": 0.50,
        "life": 0.40,
        "education": 0.40,
    }.get(domain, 0.50)


def _objective_payload(
    objective: dict[str, Any],
    domain: str,
    data_mode: str,
    n_observations: int,
    n_outer_folds: int,
    selected_configs: list[dict[str, Any]],
    baseline_metrics: dict[str, Any],
    calibrated_metrics: dict[str, Any],
    metric_delta: dict[str, Any],
    r_operational_delta: float | None,
    r_aligned_delta: float | None,
    leakage_guard: dict[str, Any],
    gate: dict[str, Any],
    comparability_status: str,
    license_terms_scan: str,
    leakage_check: str,
    n_inner_folds_mean: float = 0.0,
) -> dict[str, Any]:
    return {
        "objective_id": objective.get("objective_id"),
        "indicator": objective.get("indicator"),
        "domain": domain,
        "data_mode": data_mode,
        "n_observations": n_observations,
        "n_outer_folds": n_outer_folds,
        "n_inner_folds_mean": n_inner_folds_mean,
        "selected_configs_by_fold": selected_configs,
        "baseline_outer_metrics": baseline_metrics,
        "calibrated_outer_metrics": calibrated_metrics,
        "metric_delta_outer": metric_delta,
        "r_operational_delta_outer": r_operational_delta,
        "r_aligned_delta_outer": r_aligned_delta,
        "oos_classification": gate["oos_classification"],
        "out_of_sample_gate": gate["out_of_sample_gate"],
        "out_of_sample_gate_reason": gate["reason"],
        "claim_allowed_public": False,
        "publication_gate": "BLOCK",
        "comparability_status": comparability_status,
        "license_terms_scan": license_terms_scan,
        "leakage_check": leakage_guard.get("leakage_check", leakage_check),
        "backtest_leakage_guard": leakage_guard,
    }


def _blocked_objective(objective: dict[str, Any], domain: str, data_mode: str, reason: str) -> dict[str, Any]:
    gate = out_of_sample_gate(
        data_mode=data_mode,
        leakage_check="REVIEW",
        comparability_status="REVIEW",
        license_terms_scan="REVIEW",
        n_outer_folds=0,
        metric_delta_outer={},
        r_aligned_delta_outer=None,
        insufficient_data=True,
    )
    payload = _objective_payload(
        objective,
        domain,
        data_mode,
        0,
        0,
        [],
        {},
        {},
        {},
        None,
        None,
        {"leakage_check": "REVIEW", "findings": [reason], "critical": False},
        gate,
        "REVIEW",
        "REVIEW",
        "REVIEW",
    )
    payload["nested_backtest_status"] = "SKIPPED_INSUFFICIENT_OBSERVATIONS"
    return payload


def _summary(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "oos_metrics_improved_count": sum(1 for item in rows if item.get("oos_classification") == "OOS_METRICS_IMPROVED"),
        "oos_metrics_mixed_count": sum(1 for item in rows if item.get("oos_classification") == "OOS_METRICS_MIXED"),
        "oos_metrics_worse_count": sum(1 for item in rows if item.get("oos_classification") == "OOS_METRICS_WORSE"),
        "oos_r_only_improved_count": sum(1 for item in rows if item.get("oos_classification") == "OOS_R_ONLY_IMPROVED"),
        "blocked_insufficient_data_count": sum(1 for item in rows if item.get("oos_classification") == "OOS_BLOCKED_INSUFFICIENT_DATA"),
        "blocked_leakage_count": sum(1 for item in rows if item.get("oos_classification") == "OOS_BLOCKED_LEAKAGE"),
    }


def _action_gate(rows: list[dict[str, Any]]) -> str:
    if any(item.get("out_of_sample_gate") == "BLOCK" for item in rows):
        return "BLOCK"
    if any(item.get("out_of_sample_gate") == "REVIEW" for item in rows):
        return "REVIEW"
    return "APPROVE_LOCAL"


def _main_result(rows: list[dict[str, Any]]) -> str:
    if any(item.get("out_of_sample_gate") == "BLOCK" for item in rows):
        return "Nested backtest found a blocking condition; no predictive claim is allowed."
    if all(item.get("oos_classification") == "OOS_METRICS_IMPROVED" for item in rows):
        return "Out-of-sample metrics improved locally, but publication remains blocked by review gates."
    return "Nested backtest is mixed or review-gated; treat as internal diagnostic only."
