from __future__ import annotations

from duat_predictive_registry.walk_forward import (
    generate_nested_walk_forward_folds,
    generate_walk_forward_folds,
    validate_temporal_fold_order,
)


def test_walk_forward_generates_temporal_folds():
    folds = generate_walk_forward_folds([1, 2, 3, 4, 5, 6], min_train_size=3)
    assert folds[0]["train_indices"] == [0, 1, 2]
    assert folds[0]["test_indices"] == [3]
    assert all(max(fold["train_indices"]) < min(fold["test_indices"]) for fold in folds)


def test_nested_walk_forward_keeps_outer_test_after_inner_validation():
    folds = generate_nested_walk_forward_folds([1, 2, 3, 4, 5, 6], outer_min_train_size=5, inner_min_train_size=4)
    assert len(folds) == 1
    assert len(folds[0]["inner_folds"]) == 1
    assert validate_temporal_fold_order(folds[0]) is True
    inner = folds[0]["inner_folds"][0]
    assert max(inner["validation_indices"]) < min(folds[0]["outer_test_indices"])
