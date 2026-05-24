"""Metric-aligned R calibration for DUAT benchmark outputs."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .metric_diagnostics import compare_metric_deltas, metric_value
from .predictive_claim_gate import predictive_claim_gate
from .r_vector import clamp01


RUN_ID = "DUAT_METRIC_ALIGNED_R_CALIBRATION_v0_5"
SCHEMA = "duat.metric_aligned_r.v0_5"
EPSILON = 1e-9

DOMAIN_LAMBDA = {
    "economy": 0.35,
    "labor_market": 0.45,
    "demography": 0.40,
    "health": 0.50,
    "life": 0.40,
    "education": 0.40,
    "unknown": 0.50,
}


def compute_metric_aligned_r(
    r_before: float,
    r_after: float,
    baseline_metrics: dict[str, Any],
    enhanced_metrics: dict[str, Any],
    domain: str,
    comparability_status: str,
    license_terms_scan: str,
    leakage_check: str,
    data_mode: str = "real_fixture",
) -> dict[str, Any]:
    """Preserve operational R and add a metric-aligned R layer."""

    r_operational_before = float(r_before)
    r_operational_after = float(r_after)
    r_operational_delta = r_operational_after - r_operational_before
    diagnostics = compare_metric_deltas(baseline_metrics, enhanced_metrics)
    components = _metric_components(baseline_metrics, enhanced_metrics)
    weights = _metric_weights(components)
    metric_degradation_score = sum(components[name]["degradation_component"] * weight for name, weight in weights.items())
    metric_penalty = clamp01(DOMAIN_LAMBDA.get(domain, DOMAIN_LAMBDA["unknown"]) * metric_degradation_score)
    r_after_penalized = clamp01(r_operational_after + metric_penalty)
    primary_status = diagnostics["metric_status"]
    metric_status = _overall_metric_status(primary_status)
    alignment_floor_applied = False
    if primary_status.get("MAE") == "WORSE" and primary_status.get("RMSE") == "WORSE":
        r_after_aligned = max(r_after_penalized, r_operational_before)
        alignment_floor_applied = True
    else:
        r_after_aligned = r_after_penalized
    r_delta_aligned = r_after_aligned - r_operational_before
    claim_gate = predictive_claim_gate(
        metric_status=metric_status,
        r_delta_aligned=r_delta_aligned,
        comparability_status=comparability_status,
        license_terms_scan=license_terms_scan,
        leakage_check=leakage_check,
        data_mode=data_mode,
    )
    alignment_classification = _alignment_classification(metric_status, r_delta_aligned, claim_gate["predictive_claim_gate"])
    return {
        "r_operational_before": r_operational_before,
        "r_operational_after": r_operational_after,
        "r_operational_delta": r_operational_delta,
        "metric_components": components,
        "metric_weights": weights,
        "metric_degradation_score": metric_degradation_score,
        "metric_penalty": metric_penalty,
        "r_after_aligned": r_after_aligned,
        "r_delta_aligned": r_delta_aligned,
        "alignment_floor_applied": alignment_floor_applied,
        "metric_status": metric_status,
        "metric_diagnostics": diagnostics,
        "alignment_classification": alignment_classification,
        "predictive_claim_gate": claim_gate["predictive_claim_gate"],
        "predictive_claim_gate_detail": claim_gate,
        "publication_gate": "BLOCK",
        "reason": _reason(metric_status, alignment_floor_applied, claim_gate["reason"]),
    }


def build_metric_aligned_report(
    calibration_report: dict[str, Any],
    matrix_report: dict[str, Any],
) -> dict[str, Any]:
    objectives = []
    for item in calibration_report.get("objectives", []):
        aligned = compute_metric_aligned_r(
            r_before=item["r_before"],
            r_after=item["r_after"],
            baseline_metrics=item.get("baseline_metrics", {}),
            enhanced_metrics=item.get("enhanced_metrics", {}),
            domain=item.get("domain", "unknown"),
            comparability_status=item.get("comparability_status", "REVIEW"),
            license_terms_scan=item.get("license_terms_scan", "REVIEW"),
            leakage_check=item.get("leakage_check", "REVIEW"),
            data_mode=item.get("data_mode", "blocked_no_data"),
        )
        objectives.append(
            {
                "objective_id": item.get("objective_id"),
                "indicator": item.get("indicator"),
                "domain": item.get("domain", "unknown"),
                "data_mode": item.get("data_mode"),
                "comparability_status": item.get("comparability_status", "REVIEW"),
                "license_terms_scan": item.get("license_terms_scan", "REVIEW"),
                "leakage_check": item.get("leakage_check", "REVIEW"),
                **aligned,
            }
        )
    return {
        "schema": SCHEMA,
        "run_id": RUN_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_calibration_run_id": calibration_report.get("run_id"),
        "source_matrix_run_id": matrix_report.get("run_id"),
        "publication_gate": "BLOCK",
        "action_gate_local": _action_gate(objectives),
        "objectives": objectives,
        "summary": _summary(objectives),
        "interpretation": {
            "main_result": "R operational improved, but predictive claim remains gated by metric alignment.",
            "public_claim_allowed": False,
            "publication_gate_reason": "LicenseTermsScan/ComparabilityReview/human legal review pending.",
            "claim_level": "internal_technical_evidence_only",
        },
        "scans": {
            "LicenseTermsScan": "REVIEW",
            "LeakageCheck": "PASS" if all(item.get("leakage_check") == "PASS" for item in objectives) else "BLOCK",
            "PublicationGateScan": "PASS",
            "ComparabilityReview": "REVIEW" if any(item.get("comparability_status") != "PASS" for item in objectives) else "PASS",
        },
    }


def validate_metric_aligned_report(report: dict[str, Any]) -> list[str]:
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
            if item.get("publication_gate") != "BLOCK":
                errors.append(f"{item.get('indicator')} publication_gate must be BLOCK")
            if item.get("r_operational_delta") != item.get("r_operational_after") - item.get("r_operational_before"):
                errors.append(f"{item.get('indicator')} operational delta mismatch")
    return errors


def write_metric_aligned_json(report: dict[str, Any], path: str | Path, pretty: bool = True) -> tuple[str, str]:
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


def write_metric_aligned_markdown(report: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DUAT Metric-Aligned R Calibration v0.5",
        "",
        "publication_gate: BLOCK",
        f"run_id: {report.get('run_id')}",
        f"action_gate_local: {report.get('action_gate_local')}",
        "",
        "R reduction does not equal predictive validation.",
        "This report preserves operational R and adds metric-aligned R with explicit penalties.",
        "",
        "| indicator | metric_status | R operational delta | R aligned delta | floor | predictive claim gate |",
        "|---|---|---:|---:|---|---|",
    ]
    for item in report.get("objectives", []):
        lines.append(
            f"| {item.get('indicator')} | {item.get('metric_status')} | "
            f"{item.get('r_operational_delta')} | {item.get('r_delta_aligned')} | "
            f"{item.get('alignment_floor_applied')} | {item.get('predictive_claim_gate')} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Internal local benchmark only.",
            "- Operational R reduction is not a public predictive claim.",
            "- Metrics that worsen force REVIEW or BLOCK behavior.",
            "- publication_gate remains BLOCK.",
        ]
    )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _metric_components(baseline_metrics: dict[str, Any], enhanced_metrics: dict[str, Any]) -> dict[str, dict[str, Any]]:
    components: dict[str, dict[str, Any]] = {}
    for metric in ("MAE", "RMSE", "MAPE_if_safe"):
        baseline = metric_value(baseline_metrics, metric)
        enhanced = metric_value(enhanced_metrics, metric)
        if baseline is None or enhanced is None:
            components[metric] = {
                "baseline": baseline,
                "enhanced": enhanced,
                "relative_delta": None,
                "degradation_component": 0.0,
                "improvement_component": 0.0,
                "status": "SKIPPED",
            }
            continue
        relative_delta = (enhanced - baseline) / max(abs(baseline), EPSILON)
        components[metric] = {
            "baseline": baseline,
            "enhanced": enhanced,
            "relative_delta": relative_delta,
            "degradation_component": max(0.0, relative_delta),
            "improvement_component": max(0.0, -relative_delta),
            "status": "WORSE" if relative_delta > EPSILON else "IMPROVED" if relative_delta < -EPSILON else "SAME",
        }
    return components


def _metric_weights(components: dict[str, dict[str, Any]]) -> dict[str, float]:
    if components["MAPE_if_safe"]["status"] == "SKIPPED":
        return {"MAE": 0.50, "RMSE": 0.50}
    return {"MAE": 0.45, "RMSE": 0.45, "MAPE_if_safe": 0.10}


def _overall_metric_status(primary_status: dict[str, str]) -> str:
    mae = primary_status.get("MAE", "UNKNOWN")
    rmse = primary_status.get("RMSE", "UNKNOWN")
    mape = primary_status.get("MAPE_if_safe", "SKIPPED")
    if mae == "IMPROVED" and rmse == "IMPROVED" and mape in {"IMPROVED", "SAME", "SKIPPED"}:
        return "IMPROVED"
    if mae == "WORSE" and rmse == "WORSE":
        return "WORSE"
    if mae == "UNKNOWN" or rmse == "UNKNOWN":
        return "UNKNOWN"
    return "MIXED"


def _alignment_classification(metric_status: str, r_delta_aligned: float, gate: str) -> str:
    if gate == "BLOCK":
        return "BLOCKED"
    if metric_status == "IMPROVED" and r_delta_aligned < 0:
        return "PREDICTIVE_ALIGNED_IMPROVED"
    if metric_status == "WORSE":
        return "METRIC_DEGRADED_NO_PREDICTIVE_CLAIM"
    return "OPERATIONAL_ONLY_WITH_METRIC_CAVEAT"


def _reason(metric_status: str, floor_applied: bool, gate_reason: str) -> str:
    parts = [f"metric_status={metric_status}."]
    if floor_applied:
        parts.append("Alignment floor applied because MAE and RMSE worsened.")
    parts.append(gate_reason)
    return " ".join(parts)


def _summary(objectives: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "operational_r_improved_count": sum(1 for item in objectives if item.get("r_operational_delta", 0) < 0),
        "metric_improved_count": sum(1 for item in objectives if item.get("metric_status") == "IMPROVED"),
        "metric_mixed_count": sum(1 for item in objectives if item.get("metric_status") == "MIXED"),
        "metric_worse_count": sum(1 for item in objectives if item.get("metric_status") == "WORSE"),
        "alignment_floor_applied_count": sum(1 for item in objectives if item.get("alignment_floor_applied")),
        "predictive_claim_approve_local_count": sum(1 for item in objectives if item.get("predictive_claim_gate") == "APPROVE_LOCAL"),
        "predictive_claim_review_count": sum(1 for item in objectives if item.get("predictive_claim_gate") == "REVIEW"),
        "predictive_claim_block_count": sum(1 for item in objectives if item.get("predictive_claim_gate") == "BLOCK"),
    }


def _action_gate(objectives: list[dict[str, Any]]) -> str:
    if any(item.get("predictive_claim_gate") == "BLOCK" for item in objectives):
        return "BLOCK"
    if any(item.get("predictive_claim_gate") == "REVIEW" for item in objectives):
        return "REVIEW"
    return "APPROVE_LOCAL"
