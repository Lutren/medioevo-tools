"""Predictive claim gate for metric-aligned DUAT benchmarks."""

from __future__ import annotations

from typing import Any


ALLOWED_LANGUAGE_REVIEW = [
    "internal local benchmark",
    "operational R reduction",
    "metric caveat",
    "not predictive validation",
    "not public claim",
]

BLOCKED_LANGUAGE = [
    "validated prediction",
    "proven forecasting",
    "scientifically validated",
    "commercially validated",
    "public forecast",
    "guaranteed",
    "causal",
    "ranking",
    "electoral prediction",
    "voter targeting",
]


def predictive_claim_gate(
    *,
    metric_status: str,
    r_delta_aligned: float | None,
    comparability_status: str,
    license_terms_scan: str,
    leakage_check: str,
    data_mode: str,
) -> dict[str, Any]:
    """Decide whether a benchmark may make a local predictive claim."""

    if leakage_check != "PASS":
        return _gate("BLOCK", "LeakageCheck is not PASS.")
    if data_mode != "real_fixture":
        return _gate("BLOCK", "Predictive claim blocked because data_mode is not real_fixture.")
    if comparability_status == "BLOCK":
        return _gate("BLOCK", "ComparabilityReview is BLOCK.")
    if license_terms_scan == "BLOCK":
        return _gate("BLOCK", "LicenseTermsScan is BLOCK.")

    review_reasons: list[str] = []
    if metric_status in {"MIXED", "WORSE", "UNKNOWN"}:
        review_reasons.append(f"metric_status is {metric_status}.")
    if comparability_status == "REVIEW":
        review_reasons.append("ComparabilityReview is REVIEW.")
    if license_terms_scan == "REVIEW":
        review_reasons.append("LicenseTermsScan is REVIEW.")
    if r_delta_aligned is None or r_delta_aligned >= 0:
        review_reasons.append("R_delta_aligned is not negative.")

    if review_reasons:
        return _gate("REVIEW", " ".join(review_reasons))

    if metric_status == "IMPROVED" and r_delta_aligned < 0 and comparability_status == "PASS" and license_terms_scan == "PASS":
        return _gate("APPROVE_LOCAL", "Metric-aligned local benchmark passes non-public gates.")

    return _gate("REVIEW", "Insufficient evidence for local predictive claim approval.")


def _gate(gate: str, reason: str) -> dict[str, Any]:
    return {
        "predictive_claim_gate": gate,
        "publication_gate": "BLOCK",
        "claim_allowed_internal": gate == "APPROVE_LOCAL",
        "claim_allowed_public": False,
        "allowed_language": ALLOWED_LANGUAGE_REVIEW,
        "blocked_language": BLOCKED_LANGUAGE,
        "reason": reason,
    }
