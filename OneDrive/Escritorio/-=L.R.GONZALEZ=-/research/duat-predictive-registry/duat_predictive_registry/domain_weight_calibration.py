"""Small local grid search for DUAT domain weight calibration."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .evaluation import metric_bundle


RUN_ID = "DUAT_DOMAIN_WEIGHT_CALIBRATION_v0_5"


def calibrate_domain_weights(matrix_report: dict[str, Any]) -> dict[str, Any]:
    """Evaluate small window/weight candidates using fold-local training values.

    The grid is exploratory and remains REVIEW because candidate selection is
    performed over existing folds rather than a nested validation protocol.
    """

    objectives = []
    for report in matrix_report.get("raw_reports", []):
        objective = _calibrate_objective(report)
        objectives.append(objective)
    return {
        "schema": "duat.domain_weight_calibration.v0_5",
        "run_id": RUN_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "publication_gate": "BLOCK",
        "action_gate_local": "REVIEW",
        "domain_weight_calibration_status": _overall_status(objectives),
        "selection_protocol": "fold_local_predictions_with_non_nested_grid_selection_REVIEW_ONLY",
        "candidate_windows": [2, 3, 4, 5],
        "candidate_last_value_weights": [0.25, 0.5, 0.75],
        "objectives": objectives,
        "interpretation": {
            "public_claim_allowed": False,
            "note": "This is a local calibration diagnostic. It does not prove generalization.",
        },
    }


def write_domain_weight_json(report: dict[str, Any], path: str | Path, pretty: bool = True) -> tuple[str, str]:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    clean = dict(report)
    clean.pop("sha256", None)
    clean.pop("file_sha256", None)
    payload = json.dumps(clean, ensure_ascii=False, sort_keys=True).encode("utf-8")
    clean["sha256"] = hashlib.sha256(payload).hexdigest()
    clean["sha256_scope"] = "canonical_json_without_sha256_field"
    target.write_text(json.dumps(clean, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    file_digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return clean["sha256"], file_digest


def write_domain_weight_markdown(report: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DUAT Domain Weight Calibration v0.5",
        "",
        "publication_gate: BLOCK",
        f"status: {report.get('domain_weight_calibration_status')}",
        "",
        "This diagnostic uses fold-local training values and a small grid. It remains REVIEW until a nested backtest exists.",
        "",
        "| indicator | status | baseline MAE | best MAE | baseline RMSE | best RMSE | best window | last value weight |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in report.get("objectives", []):
        best = item.get("best_candidate") or {}
        lines.append(
            f"| {item.get('indicator')} | {item.get('domain_weight_calibration_status')} | "
            f"{item.get('baseline_metrics', {}).get('MAE')} | {best.get('metrics', {}).get('MAE')} | "
            f"{item.get('baseline_metrics', {}).get('RMSE')} | {best.get('metrics', {}).get('RMSE')} | "
            f"{best.get('window')} | {best.get('last_value_weight')} |"
        )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _calibrate_objective(report: dict[str, Any]) -> dict[str, Any]:
    rows = _fold_rows(report)
    if len(rows) < 5:
        return _objective_result(report, "SKIPPED_INSUFFICIENT_DATA", rows, None)
    candidates = []
    for window in [2, 3, 4, 5]:
        for last_weight in [0.25, 0.5, 0.75]:
            actual = []
            predicted = []
            for row in rows:
                train = row["train_values"]
                last = train[-1]
                selected = train[-window:] if len(train) >= window else train
                moving_average = sum(selected) / len(selected)
                prediction = last_weight * last + (1.0 - last_weight) * moving_average
                actual.append(row["actual"])
                predicted.append(prediction)
            candidates.append(
                {
                    "window": window,
                    "last_value_weight": last_weight,
                    "metrics": metric_bundle(actual, predicted),
                }
            )
    baseline = report.get("baseline_metrics", {}).get("selected", {})
    best = min(candidates, key=lambda item: (item["metrics"]["MAE"], item["metrics"]["RMSE"]))
    if best["metrics"]["MAE"] < baseline.get("MAE", math.inf) and best["metrics"]["RMSE"] < baseline.get("RMSE", math.inf):
        status = "REVIEW"
    else:
        status = "NOT_IMPROVED"
    return _objective_result(report, status, rows, best, candidates=candidates)


def _fold_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for series in report.get("series", []):
        by_year = dict(zip(series.get("full_years", []), series.get("full_values", [])))
        for fold in series.get("folds", []):
            train_values = [by_year[year] for year in fold.get("train_years", []) if year in by_year]
            if not train_values:
                continue
            rows.append({"actual": fold["actual"], "train_values": train_values, "target_year": fold.get("target_year")})
    return rows


def _objective_result(
    report: dict[str, Any],
    status: str,
    rows: list[dict[str, Any]],
    best: dict[str, Any] | None,
    candidates: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "objective_id": report.get("objective_id"),
        "indicator": report.get("canonical_indicator_id"),
        "data_mode": report.get("data_mode"),
        "domain_weight_calibration_status": status,
        "n_folds": len(rows),
        "baseline_metrics": report.get("baseline_metrics", {}).get("selected", {}),
        "v0_4_enhanced_metrics": report.get("enhanced_metrics", {}),
        "best_candidate": best,
        "candidate_count": len(candidates or []),
        "leakage_check": report.get("leakage_check", "REVIEW"),
        "publication_gate": "BLOCK",
        "claim_allowed_public": False,
    }


def _overall_status(objectives: list[dict[str, Any]]) -> str:
    if any(item.get("domain_weight_calibration_status") == "SKIPPED_INSUFFICIENT_DATA" for item in objectives):
        return "SKIPPED_INSUFFICIENT_DATA"
    if any(item.get("domain_weight_calibration_status") == "REVIEW" for item in objectives):
        return "REVIEW"
    return "NOT_IMPROVED"
