"""Leakage preflight checks for DUAT official long-history readiness."""

from __future__ import annotations

from typing import Any


CRITICAL_FLAGS = {
    "features_include_future_values",
    "target_uses_future_values",
    "outer_test_used_for_selection",
    "future_values_in_features",
}


def run_leakage_preflight(series: dict[str, Any]) -> dict[str, Any]:
    """Return a conservative leakage preflight result for a source series."""

    findings: list[str] = []
    for flag in CRITICAL_FLAGS:
        if series.get(flag) is True:
            findings.append(flag)
    for flag in series.get("leakage_flags") or []:
        if flag:
            findings.append(str(flag))

    if findings:
        return {
            "leakage_preflight": "BLOCK",
            "findings": sorted(set(findings)),
            "critical": True,
        }
    return {
        "leakage_preflight": "PASS",
        "findings": [],
        "critical": False,
    }
