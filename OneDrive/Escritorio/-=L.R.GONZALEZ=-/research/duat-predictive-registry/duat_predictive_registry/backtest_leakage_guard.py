"""Leakage checks for DUAT nested backtests."""

from __future__ import annotations

from typing import Any


def check_series_temporal_order(years: list[int | float]) -> dict[str, Any]:
    """Validate monotonic unique timestamps for one source series."""

    findings: list[str] = []
    if years != sorted(years):
        findings.append("series_timestamps_not_sorted")
    if len(set(years)) != len(years):
        findings.append("duplicate_timestamps")
    return _result(findings, critical=bool(findings))


def check_nested_fold_leakage(folds: list[dict[str, Any]]) -> dict[str, Any]:
    """Ensure outer test points never appear in train/validation or config selection."""

    findings: list[str] = []
    for index, fold in enumerate(folds):
        outer_train = set(fold.get("outer_train_indices") or [])
        outer_test = set(fold.get("outer_test_indices") or [])
        if outer_train & outer_test:
            findings.append(f"fold_{index}_outer_train_test_overlap")
        if not outer_train or not outer_test:
            findings.append(f"fold_{index}_missing_outer_indices")
        if outer_train and outer_test and max(outer_train) >= min(outer_test):
            findings.append(f"fold_{index}_outer_temporal_order_invalid")
        selected = fold.get("selected_config") or {}
        if selected.get("uses_outer_test") or selected.get("selected_using_outer_test"):
            findings.append(f"fold_{index}_config_uses_outer_test")
        for inner_index, inner in enumerate(fold.get("inner_folds") or []):
            train = set(inner.get("train_indices") or [])
            validation = set(inner.get("validation_indices") or [])
            if train & validation:
                findings.append(f"fold_{index}_inner_{inner_index}_train_validation_overlap")
            if validation & outer_test:
                findings.append(f"fold_{index}_inner_{inner_index}_validation_outer_test_overlap")
            if train & outer_test:
                findings.append(f"fold_{index}_inner_{inner_index}_train_outer_test_overlap")
            if train and validation and max(train) >= min(validation):
                findings.append(f"fold_{index}_inner_{inner_index}_temporal_order_invalid")
            if validation and outer_test and max(validation) >= min(outer_test):
                findings.append(f"fold_{index}_inner_{inner_index}_validation_reaches_outer_test")
    return _result(findings, critical=bool(findings))


def aggregate_leakage_checks(checks: list[dict[str, Any]]) -> dict[str, Any]:
    findings: list[str] = []
    critical = False
    for check in checks:
        findings.extend(check.get("findings") or [])
        critical = critical or bool(check.get("critical"))
    return _result(findings, critical)


def _result(findings: list[str], critical: bool) -> dict[str, Any]:
    return {
        "leakage_check": "BLOCK" if critical else "PASS",
        "findings": findings,
        "critical": critical,
    }
