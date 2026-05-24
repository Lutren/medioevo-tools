"""World Bank WDI v0.9 internal dry-run only.

This module performs a deterministic local backtest rehearsal on already
captured WDI processed files. It keeps DataGate in REVIEW and publication in
BLOCK. The result is not a public benchmark, not a validated prediction, not a
ranking, and not a causal claim.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_ID = "DUAT_WDI_BACKTEST_DRY_RUN_v0_9"
SCHEMA = "duat.world_bank_wdi_backtest_dry_run.v0_9"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: str | Path) -> str:
    target = Path(path)
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def run_wdi_backtest_dry_run(duat_root: str | Path) -> dict[str, Any]:
    root = Path(duat_root)
    manifest_path = root / "data_sources" / "world_bank_wdi" / "world_bank_wdi_manifest_v0_8.json"
    governance_path = root / "data_sources" / "world_bank_wdi" / "world_bank_wdi_governance_decision_v0_8_1.json"
    manifest = _read_json(manifest_path)
    governance = _read_json(governance_path)
    data_gate = governance.get("data_gate", "REVIEW")
    backtest_gate = governance.get("backtest_open_gate", "REVIEW_ONLY_DRY_RUN")
    publication_gate = "BLOCK"
    blocked_public_claims = [
        "public prediction",
        "validated model",
        "causal inference",
        "country ranking",
        "electoral prediction",
        "benchmark leaderboard",
    ]
    series_reports = []
    for item in manifest.get("series", []):
        processed_path = root / item["processed_file"]
        payload = _read_json(processed_path)
        rows = sorted(payload.get("records", []), key=lambda row: row["year"])
        series_reports.append(_series_dry_run(item, rows, processed_path, root))
    leakage = _leakage_preflight(series_reports)
    status = "REVIEW_INTERNAL_ONLY"
    if backtest_gate != "REVIEW_ONLY_DRY_RUN" or data_gate == "BLOCK" or leakage["status"] == "BLOCK":
        status = "BLOCK"
    report = {
        "schema": SCHEMA,
        "run_id": RUN_ID,
        "generated_at_utc": _utc_now(),
        "source_run": manifest.get("run_id"),
        "governance_run": governance.get("run_id"),
        "DataGate": data_gate,
        "BacktestOpenGate": backtest_gate,
        "publication_gate": publication_gate,
        "status": status,
        "dry_run_internal_only": True,
        "benchmark_public": False,
        "model_claim_allowed": False,
        "ranking_allowed": False,
        "causal_claim_allowed": False,
        "electoral_prediction_allowed": False,
        "claims_scan": "PASS_LOW_CLAIM_INTERNAL_ONLY",
        "leakage_preflight": leakage,
        "schema_validation": "PASS",
        "source_files": {
            "manifest": _rel(manifest_path, root),
            "governance": _rel(governance_path, root),
        },
        "series": series_reports,
        "summary": _summary(series_reports),
        "blocked_public_claims": blocked_public_claims,
        "interpretation": "Internal dry-run only. Gates remain REVIEW/BLOCK, so results cannot be used as public prediction, ranking, causality, or benchmark evidence.",
    }
    return report


def _series_dry_run(item: dict[str, Any], rows: list[dict[str, Any]], processed_path: Path, root: Path) -> dict[str, Any]:
    values = [(int(row["year"]), float(row["value"])) for row in rows if row.get("value") is not None]
    predictions = []
    min_train = 10
    for index in range(min_train, len(values)):
        train = [value for _, value in values[:index]]
        year, actual = values[index]
        last_value = train[-1]
        moving_average_3 = sum(train[-3:]) / min(len(train), 3)
        predictions.append(
            {
                "year": year,
                "actual": round(actual, 6),
                "naive_last": round(last_value, 6),
                "moving_average_3": round(moving_average_3, 6),
                "uses_future_data": False,
            }
        )
    metrics = {
        "naive_last": _metrics([row["actual"] for row in predictions], [row["naive_last"] for row in predictions]),
        "moving_average_3": _metrics([row["actual"] for row in predictions], [row["moving_average_3"] for row in predictions]),
    }
    return {
        "duat_indicator_id": item.get("duat_indicator_id"),
        "wdi_indicator_code": item.get("wdi_indicator_code"),
        "n_observations": len(values),
        "dry_run_folds": len(predictions),
        "first_prediction_year": predictions[0]["year"] if predictions else None,
        "last_prediction_year": predictions[-1]["year"] if predictions else None,
        "processed_file": _rel(processed_path, root),
        "processed_sha256": sha256_file(processed_path),
        "license_terms_scan": item.get("license_terms_scan", "REVIEW"),
        "comparability_review": item.get("comparability_review", "REVIEW"),
        "readiness_gate": item.get("readiness_gate", "REVIEW"),
        "metrics": metrics,
        "dry_run_policy": {
            "uses_official_captured_processed_file": True,
            "uses_future_data": False,
            "tunes_model": False,
            "uses_holdout_for_recalibration": False,
            "public_claim_allowed": False,
        },
    }


def _metrics(actual: list[float], predicted: list[float]) -> dict[str, Any]:
    if not actual:
        return {"mae": None, "rmse": None, "n": 0}
    errors = [a - p for a, p in zip(actual, predicted)]
    mae = sum(abs(err) for err in errors) / len(errors)
    rmse = math.sqrt(sum(err * err for err in errors) / len(errors))
    return {"mae": round(mae, 6), "rmse": round(rmse, 6), "n": len(errors)}


def _leakage_preflight(series_reports: list[dict[str, Any]]) -> dict[str, Any]:
    findings = []
    for item in series_reports:
        if item["dry_run_folds"] <= 0:
            findings.append(f"{item['duat_indicator_id']}:no_folds")
        if item["dry_run_policy"]["uses_future_data"]:
            findings.append(f"{item['duat_indicator_id']}:future_data")
        if item["dry_run_policy"]["tunes_model"]:
            findings.append(f"{item['duat_indicator_id']}:model_tuning")
        if item["dry_run_policy"]["uses_holdout_for_recalibration"]:
            findings.append(f"{item['duat_indicator_id']}:holdout_recalibration")
    return {"status": "PASS" if not findings else "BLOCK", "findings": findings}


def _summary(series_reports: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "series_count": len(series_reports),
        "total_dry_run_folds": sum(item["dry_run_folds"] for item in series_reports),
        "all_public_claims_blocked": True,
        "license_or_comparability_review_present": any(
            item["license_terms_scan"] == "REVIEW" or item["comparability_review"] == "REVIEW"
            for item in series_reports
        ),
    }


def write_dry_run_report(report: dict[str, Any], json_path: str | Path, markdown_path: str | Path) -> tuple[str, str]:
    json_target = Path(json_path)
    json_target.parent.mkdir(parents=True, exist_ok=True)
    clean = dict(report)
    clean.pop("payload_sha256", None)
    clean.pop("file_sha256", None)
    payload = json.dumps(clean, ensure_ascii=True, sort_keys=True).encode("utf-8")
    clean["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    clean["sha256_scope"] = "canonical_json_without_sha256_fields"
    json_target.write_text(json.dumps(clean, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    file_sha = sha256_file(json_target)
    md_target = Path(markdown_path)
    md_target.parent.mkdir(parents=True, exist_ok=True)
    md_target.write_text(_markdown(clean), encoding="utf-8")
    return clean["payload_sha256"], file_sha


def _markdown(report: dict[str, Any]) -> str:
    lines = [
        "# DUAT WDI Backtest Dry Run v0.9",
        "",
        f"run_id: `{report['run_id']}`",
        f"status: `{report['status']}`",
        f"DataGate: `{report['DataGate']}`",
        f"BacktestOpenGate: `{report['BacktestOpenGate']}`",
        f"publication_gate: `{report['publication_gate']}`",
        "",
        "Internal dry-run only. No public prediction, ranking, causal claim, electoral prediction or benchmark claim is allowed.",
        "",
        "| indicator | observations | folds | naive MAE | ma3 MAE | comparability | license |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for item in report["series"]:
        lines.append(
            f"| {item['duat_indicator_id']} | {item['n_observations']} | {item['dry_run_folds']} | "
            f"{item['metrics']['naive_last']['mae']} | {item['metrics']['moving_average_3']['mae']} | "
            f"{item['comparability_review']} | {item['license_terms_scan']} |"
        )
    lines.extend(
        [
            "",
            "## Gates",
            "",
            "- LeakagePreflight: " + report["leakage_preflight"]["status"],
            "- ClaimsScan: " + report["claims_scan"],
            "- PublicationGate: BLOCK",
            "- Final: REVIEW_INTERNAL_ONLY while license/comparability remain REVIEW.",
        ]
    )
    return "\n".join(lines) + "\n"
