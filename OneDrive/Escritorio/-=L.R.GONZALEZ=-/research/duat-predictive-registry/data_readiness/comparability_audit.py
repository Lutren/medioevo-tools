"""Comparability audit helpers for DUAT data readiness."""

from __future__ import annotations

from typing import Any


def audit_comparability(series: dict[str, Any]) -> dict[str, Any]:
    """Check whether a series has enough metadata for comparable backtests."""

    explicit = str(series.get("comparability_status") or "").upper()
    findings: list[str] = []
    if explicit == "BLOCK":
        return {"comparability_review": "BLOCK", "findings": ["explicit_comparability_block"]}
    if explicit == "REVIEW":
        findings.append("explicit_comparability_review")

    if not series.get("unit"):
        findings.append("missing_unit")
    if not series.get("definition"):
        findings.append("missing_definition")
    if series.get("definition_change_without_crosswalk"):
        findings.append("definition_change_without_crosswalk")
    if series.get("unit_change_without_crosswalk"):
        findings.append("unit_change_without_crosswalk")

    if any(item.endswith("without_crosswalk") for item in findings):
        gate = "REVIEW"
    elif findings:
        gate = "REVIEW"
    else:
        gate = "PASS"
    return {"comparability_review": gate, "findings": findings}
