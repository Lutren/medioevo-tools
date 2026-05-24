"""Temporal coverage audit for DUAT official series readiness."""

from __future__ import annotations

from typing import Any


def audit_temporal_coverage(series: dict[str, Any]) -> dict[str, Any]:
    frequency = str(series.get("frequency") or "unknown").lower()
    start_year = series.get("start_year")
    end_year = series.get("end_year")
    n_observations = series.get("n_observations")
    findings: list[str] = []
    if start_year is None or end_year is None:
        findings.append("missing_start_or_end_year")
    if n_observations is None:
        findings.append("missing_n_observations")
    if frequency == "annual" and start_year is not None and end_year is not None and n_observations is not None:
        expected = int(end_year) - int(start_year) + 1
        if int(n_observations) < expected:
            findings.append("annual_series_has_gaps")
    if series.get("imputation_method"):
        findings.append("imputation_present")
    if any(item in findings for item in ("missing_start_or_end_year", "missing_n_observations")):
        gate = "REVIEW"
    elif "annual_series_has_gaps" in findings:
        gate = "REVIEW"
    else:
        gate = "PASS"
    return {
        "temporal_coverage_review": gate,
        "frequency": frequency,
        "findings": findings,
        "imputation_review": "REVIEW" if series.get("imputation_method") else "PASS",
    }
