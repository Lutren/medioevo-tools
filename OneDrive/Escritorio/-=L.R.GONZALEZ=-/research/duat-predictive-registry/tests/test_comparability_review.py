from __future__ import annotations

from pathlib import Path

from duat_predictive_registry.comparability import build_comparability_review
from duat_predictive_registry.objectives import find_workspace_root, load_objective


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = find_workspace_root(ROOT)


def test_comparability_review_marks_labor_as_strong_proxy_review():
    objective = load_objective(ROOT / "fixtures" / "duat_labor_market_unemployment_objective_v0_1.json")
    review = build_comparability_review([objective], WORKSPACE_ROOT)
    item = review["reviews"][0]
    assert item["review_status"] == "REVIEW_STRONG_PROXY_NOT_EXACT"
    assert len(item["entries"]) == 3
    assert all(entry["comparability_class"] == "STRONG_PROXY" for entry in item["entries"])


def test_comparability_review_keeps_publication_blocked():
    objective = load_objective(ROOT / "fixtures" / "duat_first_predictive_objective_v0_1.json")
    review = build_comparability_review([objective], WORKSPACE_ROOT)
    assert review["publication_gate"] == "BLOCK"
    assert review["reviews"][0]["review_status"].startswith("REVIEW")
