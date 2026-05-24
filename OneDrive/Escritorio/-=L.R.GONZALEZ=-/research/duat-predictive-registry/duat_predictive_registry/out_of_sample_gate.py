"""Out-of-sample gate for DUAT nested benchmark diagnostics."""

from __future__ import annotations

from typing import Any


def out_of_sample_gate(
    *,
    data_mode: str,
    leakage_check: str,
    comparability_status: str,
    license_terms_scan: str,
    n_outer_folds: int,
    metric_delta_outer: dict[str, Any],
    r_aligned_delta_outer: float | None,
    insufficient_data: bool = False,
) -> dict[str, Any]:
    """Classify out-of-sample behavior without allowing public claims."""

    if insufficient_data:
        return _gate("REVIEW", "OOS_BLOCKED_INSUFFICIENT_DATA", "Insufficient observations for nested backtest.")
    if leakage_check != "PASS":
        return _gate("BLOCK", "OOS_BLOCKED_LEAKAGE", "BacktestLeakageGuard is not PASS.")
    if data_mode != "real_fixture":
        return _gate("BLOCK", "OOS_BLOCKED_INSUFFICIENT_DATA", "Only real_fixture can support predictive diagnostics.")
    if comparability_status == "BLOCK" or license_terms_scan == "BLOCK":
        return _gate("BLOCK", "OOS_REVIEW_COMPARABILITY", "Comparability or license scan is BLOCK.")

    mae_delta = metric_delta_outer.get("MAE")
    rmse_delta = metric_delta_outer.get("RMSE")
    if mae_delta is None or rmse_delta is None:
        classification = "OOS_REVIEW_COMPARABILITY"
    elif mae_delta < 0 and rmse_delta < 0 and (r_aligned_delta_outer is not None and r_aligned_delta_outer < 0):
        classification = "OOS_METRICS_IMPROVED"
    elif mae_delta > 0 and rmse_delta > 0 and (r_aligned_delta_outer is not None and r_aligned_delta_outer < 0):
        classification = "OOS_R_ONLY_IMPROVED"
    elif mae_delta > 0 and rmse_delta > 0:
        classification = "OOS_METRICS_WORSE"
    else:
        classification = "OOS_METRICS_MIXED"

    review_reasons: list[str] = []
    if classification != "OOS_METRICS_IMPROVED":
        review_reasons.append(f"classification={classification}.")
    if comparability_status == "REVIEW":
        review_reasons.append("ComparabilityReview is REVIEW.")
    if license_terms_scan == "REVIEW":
        review_reasons.append("LicenseTermsScan is REVIEW.")
    if n_outer_folds < 2:
        review_reasons.append("n_outer_folds < 2.")
    if r_aligned_delta_outer is None or r_aligned_delta_outer >= 0:
        review_reasons.append("R_aligned_delta_outer is not negative.")

    if review_reasons:
        return _gate("REVIEW", classification, " ".join(review_reasons))
    return _gate("APPROVE_LOCAL", classification, "Out-of-sample local diagnostic passed non-public gates.")


def _gate(gate: str, classification: str, reason: str) -> dict[str, Any]:
    return {
        "out_of_sample_gate": gate,
        "oos_classification": classification,
        "publication_gate": "BLOCK",
        "claim_allowed_public": False,
        "reason": reason,
    }
