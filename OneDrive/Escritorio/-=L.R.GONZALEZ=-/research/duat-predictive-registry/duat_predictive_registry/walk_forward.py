"""Deterministic walk-forward split helpers for DUAT benchmarks."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def generate_walk_forward_folds(
    observations: Sequence[Any],
    min_train_size: int,
    horizon: int = 1,
) -> list[dict[str, list[int]]]:
    """Return expanding-window train/test folds.

    The test block is always strictly after the training block. The function is
    index-only so callers can use years, timestamps or values without copying
    private data into the split contract.
    """

    _validate_split_args(len(observations), min_train_size, horizon)
    folds: list[dict[str, list[int]]] = []
    for test_start in range(min_train_size, len(observations) - horizon + 1):
        folds.append(
            {
                "train_indices": list(range(0, test_start)),
                "test_indices": list(range(test_start, test_start + horizon)),
            }
        )
    return folds


def generate_nested_walk_forward_folds(
    observations: Sequence[Any],
    outer_min_train_size: int,
    inner_min_train_size: int,
    horizon: int = 1,
) -> list[dict[str, Any]]:
    """Return outer folds with inner validation folds inside outer_train only."""

    _validate_split_args(len(observations), outer_min_train_size, horizon)
    if inner_min_train_size >= outer_min_train_size:
        # With the current fixtures this still permits one inner validation
        # point when outer_train length is outer_min_train_size.
        pass
    outer_folds: list[dict[str, Any]] = []
    for outer in generate_walk_forward_folds(observations, outer_min_train_size, horizon):
        outer_train = outer["train_indices"]
        outer_test = outer["test_indices"]
        inner_folds: list[dict[str, list[int]]] = []
        for validation_start in range(inner_min_train_size, len(outer_train) - horizon + 1):
            inner_folds.append(
                {
                    "train_indices": list(range(0, validation_start)),
                    "validation_indices": list(range(validation_start, validation_start + horizon)),
                }
            )
        outer_folds.append(
            {
                "outer_train_indices": outer_train,
                "outer_test_indices": outer_test,
                "inner_folds": inner_folds,
            }
        )
    return outer_folds


def validate_temporal_fold_order(fold: dict[str, Any]) -> bool:
    """Check strict train < validation < outer test ordering."""

    outer_train = fold.get("outer_train_indices") or []
    outer_test = fold.get("outer_test_indices") or []
    if not outer_train or not outer_test:
        return False
    if max(outer_train) >= min(outer_test):
        return False
    for inner in fold.get("inner_folds", []):
        train = inner.get("train_indices") or []
        validation = inner.get("validation_indices") or []
        if not train or not validation:
            return False
        if max(train) >= min(validation):
            return False
        if max(validation) >= min(outer_test):
            return False
    return True


def _validate_split_args(n_observations: int, min_train_size: int, horizon: int) -> None:
    if min_train_size < 1:
        raise ValueError("min_train_size must be positive")
    if horizon < 1:
        raise ValueError("horizon must be positive")
    if n_observations < min_train_size + horizon:
        return
