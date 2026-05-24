"""Comparability review helpers for DUAT/GEODIA benchmark objectives."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .objectives import find_workspace_root, resolve_workspace_path
from .registry_loader import load_json


def comparability_entries_for_objective(
    objective: dict[str, Any],
    workspace_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    root = Path(workspace_root or find_workspace_root()).resolve()
    crosswalk = load_json(resolve_workspace_path(objective["inputs"]["crosswalk_path"], root))
    canonical_id = objective.get("canonical_indicator_id") or objective.get("target_indicator")
    accepted = set(objective["inputs"].get("accepted_comparability_classes") or [])
    entries = []
    for entry in crosswalk.get("entries", []):
        if entry.get("canonical_indicator_id") != canonical_id:
            continue
        if accepted and entry.get("comparability_class") not in accepted:
            continue
        entries.append(entry)
    return entries


def build_comparability_review(
    objectives: list[dict[str, Any]],
    workspace_root: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(workspace_root or find_workspace_root()).resolve()
    reviews: list[dict[str, Any]] = []
    for objective in objectives:
        entries = comparability_entries_for_objective(objective, root)
        reviews.append(
            {
                "objective_id": objective["objective_id"],
                "indicator": objective.get("canonical_indicator_id") or objective.get("target_indicator"),
                "entries": [
                    {
                        "source_id": entry.get("source_id"),
                        "source_indicator_id": entry.get("source_indicator_id"),
                        "country_or_region": entry.get("country_or_region"),
                        "year_range": entry.get("year_range"),
                        "frequency": entry.get("frequency"),
                        "unit_original": entry.get("unit_original"),
                        "unit_canonical": entry.get("unit_canonical"),
                        "polarity_original": entry.get("polarity_original"),
                        "polarity_canonical": entry.get("polarity_canonical"),
                        "transformation_applied": entry.get("transformation_applied"),
                        "comparability_class": entry.get("comparability_class"),
                        "caveats": entry.get("caveats", []),
                    }
                    for entry in entries
                ],
                "review_status": _review_status(entries),
                "publication_gate": "BLOCK",
            }
        )
    return {
        "schema": "duat.license_comparability_review.v0_1",
        "publication_gate": "BLOCK",
        "reviews": reviews,
        "summary": "Technical comparability only; no ranking, public prediction or causal claim.",
    }


def _review_status(entries: list[dict[str, Any]]) -> str:
    if not entries:
        return "BLOCKED_NO_CROSSWALK_ENTRY"
    classes = {entry.get("comparability_class") for entry in entries}
    if classes == {"EXACT"}:
        return "PASS_TECHNICAL_EXACT_LICENSE_STILL_REVIEW"
    if classes.issubset({"STRONG_PROXY"}):
        return "REVIEW_STRONG_PROXY_NOT_EXACT"
    return "REVIEW_MIXED_OR_WEAK_COMPARABILITY"
