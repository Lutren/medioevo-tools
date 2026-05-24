from __future__ import annotations

from duat_predictive_registry.backtest_leakage_guard import (
    check_nested_fold_leakage,
    check_series_temporal_order,
)


def test_leakage_guard_passes_clean_nested_fold():
    result = check_nested_fold_leakage(
        [
            {
                "outer_train_indices": [0, 1, 2, 3, 4],
                "outer_test_indices": [5],
                "inner_folds": [{"train_indices": [0, 1, 2, 3], "validation_indices": [4]}],
                "selected_config": {"uses_outer_test": False},
            }
        ]
    )
    assert result["leakage_check"] == "PASS"
    assert result["critical"] is False


def test_leakage_guard_blocks_train_test_overlap():
    result = check_nested_fold_leakage(
        [
            {
                "outer_train_indices": [0, 1, 2, 3, 4, 5],
                "outer_test_indices": [5],
                "inner_folds": [{"train_indices": [0, 1, 2, 3], "validation_indices": [4]}],
                "selected_config": {"uses_outer_test": False},
            }
        ]
    )
    assert result["leakage_check"] == "BLOCK"
    assert any("outer_train_test_overlap" in finding for finding in result["findings"])


def test_leakage_guard_blocks_config_using_outer_test():
    result = check_nested_fold_leakage(
        [
            {
                "outer_train_indices": [0, 1, 2, 3, 4],
                "outer_test_indices": [5],
                "inner_folds": [{"train_indices": [0, 1, 2, 3], "validation_indices": [4]}],
                "selected_config": {"uses_outer_test": True},
            }
        ]
    )
    assert result["leakage_check"] == "BLOCK"
    assert any("config_uses_outer_test" in finding for finding in result["findings"])


def test_leakage_guard_blocks_unsorted_or_duplicate_time():
    unsorted = check_series_temporal_order([2020, 2019, 2021])
    duplicate = check_series_temporal_order([2019, 2020, 2020])
    assert unsorted["leakage_check"] == "BLOCK"
    assert duplicate["leakage_check"] == "BLOCK"
