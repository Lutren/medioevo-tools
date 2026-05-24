"""Domain calibration gate for DUAT benchmark rows."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .domain_profiles import get_domain_profile, infer_domain
from .metric_diagnostics import compare_metric_deltas, explain_metric_diagnostics
from .objectives import find_workspace_root, resolve_workspace_path


RUN_ID = "DUAT_DOMAIN_CALIBRATION_GATE_v0_4"
SCHEMA = "duat.domain_calibration_gate.v0_4"

CLASSIFICATIONS = {
    "OPERATIONAL_R_IMPROVED_METRICS_IMPROVED",
    "OPERATIONAL_R_IMPROVED_METRICS_MIXED",
    "OPERATIONAL_R_IMPROVED_METRICS_WORSE",
    "R_NOT_IMPROVED_METRICS_IMPROVED",
    "R_NOT_IMPROVED_METRICS_WORSE",
    "BLOCKED_NO_DATA",
    "REVIEW_COMPARABILITY",
}


def calibrate_benchmark_row(
    row: dict[str, Any],
    comparability_status: str = "REVIEW",
    epsilon: float = 1e-9,
) -> dict[str, Any]:
    """Classify one benchmark row by separating operational R and error metrics."""

    indicator = row.get("indicator")
    domain = row.get("domain") or infer_domain(indicator)
    profile = get_domain_profile(domain)
    publication_gate = "BLOCK"
    data_mode = row.get("data_mode")
    leakage_check = row.get("leakage_check", "REVIEW")
    license_terms_scan = row.get("license_terms_scan", "REVIEW")
    r_delta = row.get("r_delta")

    if data_mode != "real_fixture":
        return _result(
            row=row,
            domain=domain,
            profile=profile,
            classification="BLOCKED_NO_DATA",
            gate="REVIEW",
            diagnostics={},
            comparability_status=comparability_status,
            r_improved=False,
            reason="No real fixture evidence is available; synthetic or blocked rows do not count as predictive evidence.",
            recommended_next_action="Add a real offline fixture or leave this objective out of evidence matrices.",
        )

    if leakage_check != "PASS":
        return _result(
            row=row,
            domain=domain,
            profile=profile,
            classification="BLOCKED_NO_DATA",
            gate="BLOCK",
            diagnostics={},
            comparability_status=comparability_status,
            r_improved=False,
            reason="LeakageCheck is not PASS.",
            recommended_next_action="Fix leakage before any benchmark interpretation.",
        )

    diagnostics = compare_metric_deltas(
        row.get("baseline_metrics", {}),
        row.get("enhanced_metrics", {}),
        epsilon=epsilon,
    )
    r_improved = isinstance(r_delta, (int, float)) and r_delta < -epsilon
    if not isinstance(r_delta, (int, float)):
        classification = "BLOCKED_NO_DATA"
    elif r_improved and diagnostics["metrics_improved"]:
        classification = "OPERATIONAL_R_IMPROVED_METRICS_IMPROVED"
    elif r_improved and diagnostics["metrics_worse"]:
        classification = "OPERATIONAL_R_IMPROVED_METRICS_WORSE"
    elif r_improved:
        classification = "OPERATIONAL_R_IMPROVED_METRICS_MIXED"
    elif diagnostics["metrics_improved"]:
        classification = "R_NOT_IMPROVED_METRICS_IMPROVED"
    else:
        classification = "R_NOT_IMPROVED_METRICS_WORSE"

    gate = "APPROVE_LOCAL"
    reasons: list[str] = []
    if license_terms_scan == "REVIEW":
        gate = "REVIEW"
        reasons.append("LicenseTermsScan remains REVIEW pending human/legal review.")
    if comparability_status != "PASS":
        gate = "REVIEW" if gate != "BLOCK" else gate
        reasons.append(f"ComparabilityReview is {comparability_status}.")
    if classification.endswith("METRICS_WORSE"):
        gate = "REVIEW"
        reasons.append("Operational R improved but direct error metrics worsened.")
    if classification.endswith("METRICS_MIXED"):
        gate = "REVIEW"
        reasons.append("Direct error metrics are mixed.")
    if not r_improved:
        gate = "REVIEW"
        reasons.append("R_delta did not improve.")

    if not reasons:
        reasons.append("Local benchmark passes domain calibration, but publication remains blocked.")

    return _result(
        row=row,
        domain=domain,
        profile=profile,
        classification=classification,
        gate=gate,
        diagnostics=diagnostics,
        comparability_status=comparability_status,
        r_improved=r_improved,
        reason=" ".join(reasons),
        recommended_next_action=_recommended_next_action(classification, domain),
    )


def calibrate_matrix(matrix: dict[str, Any], workspace_root: str | Path | None = None) -> dict[str, Any]:
    """Build the v0.4 domain calibration report from a benchmark matrix."""

    root = Path(workspace_root or find_workspace_root()).resolve()
    comparability_by_indicator = _comparability_status_by_indicator(matrix)
    calibrated = [
        calibrate_benchmark_row(
            row,
            comparability_status=comparability_by_indicator.get(row.get("indicator"), "REVIEW"),
        )
        for row in matrix.get("objectives", [])
    ]
    summary = _summary(calibrated)
    return {
        "schema": SCHEMA,
        "run_id": RUN_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "publication_gate": "BLOCK",
        "action_gate_local": "REVIEW" if any(item["domain_calibration_gate"] == "REVIEW" for item in calibrated) else _action_gate(calibrated),
        "source_matrix_run_id": matrix.get("run_id"),
        "source_matrix_report": _display_path(root / "research" / "duat-predictive-registry" / "reports" / "duat-benchmark-matrix-v0-4.json", root),
        "summary": summary,
        "objectives": calibrated,
        "interpretation": {
            "r_delta_status": _r_delta_status(calibrated),
            "metric_status": _metric_status(calibrated),
            "claim_level": "internal_technical_evidence_only",
            "public_claim_allowed": False,
            "note": "R reduction does not equal predictive validation. Domain calibration separates operational residue from direct forecast error metrics.",
        },
        "scans": {
            "LicenseTermsScan": "REVIEW",
            "LeakageCheck": "PASS" if all(item.get("leakage_check") == "PASS" for item in calibrated) else "BLOCK",
            "PublicationGateScan": "PASS",
            "ComparabilityReview": "REVIEW" if any(item.get("comparability_status") != "PASS" for item in calibrated) else "PASS",
        },
    }


def validate_domain_calibration_report(report: dict[str, Any]) -> list[str]:
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
            if item.get("classification") not in CLASSIFICATIONS:
                errors.append(f"invalid classification: {item.get('classification')}")
            if item.get("publication_gate") != "BLOCK":
                errors.append(f"{item.get('indicator')} publication_gate must be BLOCK")
    return errors


def write_domain_calibration_json(report: dict[str, Any], path: str | Path, pretty: bool = True) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    report["sha256"] = digest
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    return digest


def write_domain_calibration_markdown(report: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DUAT Domain Calibration Gate v0.4",
        "",
        "publication_gate: BLOCK",
        f"run_id: {report.get('run_id')}",
        f"action_gate_local: {report.get('action_gate_local')}",
        "",
        "## Boundary",
        "",
        "This is an internal local benchmark. R reduction does not equal predictive validation.",
        "The report separates operational residue reduction from direct forecast error metrics.",
        "",
        "## Matrix",
        "",
        "| indicator | domain | data_mode | R_delta | MAE delta | RMSE delta | classification | gate |",
        "|---|---|---|---:|---:|---:|---|---|",
    ]
    for item in report.get("objectives", []):
        deltas = item.get("metric_diagnostics", {}).get("metric_deltas", {})
        lines.append(
            f"| {item.get('indicator')} | {item.get('domain')} | {item.get('data_mode')} | "
            f"{item.get('r_delta')} | {deltas.get('MAE')} | {deltas.get('RMSE')} | "
            f"{item.get('classification')} | {item.get('domain_calibration_gate')} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "- Internal technical evidence only.",
            "- No public predictive claim.",
            "- No ranking, causal claim or external release.",
            "- LicenseTermsScan remains REVIEW pending human/legal review.",
            "",
            "## Next Action",
            "",
            "Calibrate per-domain model weights before treating operational R reduction as direct accuracy improvement.",
        ]
    )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _result(
    *,
    row: dict[str, Any],
    domain: str,
    profile: dict[str, Any],
    classification: str,
    gate: str,
    diagnostics: dict[str, Any],
    comparability_status: str,
    r_improved: bool,
    reason: str,
    recommended_next_action: str,
) -> dict[str, Any]:
    return {
        "objective_id": row.get("objective_id"),
        "indicator": row.get("indicator"),
        "domain": domain,
        "domain_profile": profile,
        "data_mode": row.get("data_mode"),
        "r_before": row.get("r_before"),
        "r_after": row.get("r_after"),
        "r_delta": row.get("r_delta"),
        "baseline_metrics": row.get("baseline_metrics", {}),
        "enhanced_metrics": row.get("enhanced_metrics", {}),
        "metric_diagnostics": diagnostics,
        "metric_diagnostics_summary": explain_metric_diagnostics(diagnostics) if diagnostics else "not_available",
        "domain_calibration_gate": gate,
        "classification": classification,
        "r_improved": r_improved,
        "metrics_improved": bool(diagnostics.get("metrics_improved")) if diagnostics else False,
        "metrics_mixed": bool(diagnostics.get("metrics_mixed")) if diagnostics else False,
        "metrics_worse": bool(diagnostics.get("metrics_worse")) if diagnostics else False,
        "comparability_status": comparability_status,
        "license_terms_scan": row.get("license_terms_scan", "REVIEW"),
        "leakage_check": row.get("leakage_check", "REVIEW"),
        "public_claim_allowed": False,
        "publication_gate": "BLOCK",
        "reason": reason,
        "recommended_next_action": recommended_next_action,
    }


def _comparability_status_by_indicator(matrix: dict[str, Any]) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for review in matrix.get("comparability_review", {}).get("reviews", []):
        status = review.get("review_status", "REVIEW")
        if str(status).startswith("PASS"):
            value = "PASS"
        elif str(status).startswith("BLOCK"):
            value = "BLOCK"
        else:
            value = "REVIEW"
        statuses[review.get("indicator")] = value
    return statuses


def _summary(items: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "r_reduction_replicated_count": sum(1 for item in items if item.get("r_improved")),
        "metrics_improved_count": sum(1 for item in items if item.get("metrics_improved")),
        "metrics_mixed_count": sum(1 for item in items if item.get("metrics_mixed")),
        "metrics_worse_count": sum(1 for item in items if item.get("metrics_worse")),
        "blocked_no_data_count": sum(1 for item in items if item.get("classification") == "BLOCKED_NO_DATA"),
    }


def _r_delta_status(items: list[dict[str, Any]]) -> str:
    if any(item.get("classification") == "BLOCKED_NO_DATA" for item in items):
        return "blocked_no_data_present"
    if all(item.get("r_improved") for item in items):
        return "replicated_locally_but_domain_limited"
    if any(item.get("r_improved") for item in items):
        return "mixed_local"
    return "not_replicated"


def _metric_status(items: list[dict[str, Any]]) -> str:
    if any(item.get("metrics_worse") for item in items):
        return "mixed_or_worse_until_calibrated"
    if any(item.get("metrics_mixed") for item in items):
        return "mixed_until_calibrated"
    if all(item.get("metrics_improved") for item in items):
        return "metrics_improved_locally"
    return "not_available"


def _action_gate(items: list[dict[str, Any]]) -> str:
    if any(item.get("domain_calibration_gate") == "BLOCK" for item in items):
        return "BLOCK"
    if any(item.get("domain_calibration_gate") == "REVIEW" for item in items):
        return "REVIEW"
    return "APPROVE_LOCAL"


def _recommended_next_action(classification: str, domain: str) -> str:
    if classification == "OPERATIONAL_R_IMPROVED_METRICS_WORSE":
        return f"Calibrate {domain} model weights; do not treat R_delta as direct accuracy gain."
    if classification == "OPERATIONAL_R_IMPROVED_METRICS_MIXED":
        return f"Inspect {domain} metric disagreement and test an alternate baseline or window."
    if classification == "OPERATIONAL_R_IMPROVED_METRICS_IMPROVED":
        return f"Keep {domain} as local evidence and add more folds before any stronger claim."
    if classification == "BLOCKED_NO_DATA":
        return "Add a real fixture before interpreting this objective."
    return f"Review {domain} calibration before expanding."


def _display_path(path: Path, workspace_root: Path) -> str:
    try:
        return path.relative_to(workspace_root).as_posix()
    except ValueError:
        return str(path)
