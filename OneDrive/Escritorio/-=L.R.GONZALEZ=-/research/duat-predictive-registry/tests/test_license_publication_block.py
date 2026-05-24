from __future__ import annotations

from pathlib import Path

from duat_predictive_registry.license_review import build_license_review
from duat_predictive_registry.objectives import find_workspace_root, load_objective


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = find_workspace_root(ROOT)


def test_license_review_blocks_publication_until_human_review():
    objectives = [
        load_objective(ROOT / "fixtures" / "duat_first_predictive_objective_v0_1.json"),
        load_objective(ROOT / "fixtures" / "duat_labor_market_unemployment_objective_v0_1.json"),
    ]
    review = build_license_review(objectives, WORKSPACE_ROOT)
    assert review["publication_gate"] == "BLOCK"
    assert review["license_terms_scan"] == "REVIEW"
    assert "human/legal review" in review["missing_for_pass"][0]
    assert len(review["fixtures"]) >= 3
