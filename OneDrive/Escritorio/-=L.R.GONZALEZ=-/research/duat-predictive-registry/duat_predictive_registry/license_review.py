"""License and publication-boundary review helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .objectives import find_workspace_root, resolve_workspace_path
from .registry_loader import load_json


def build_license_review(
    objectives: list[dict[str, Any]],
    workspace_root: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(workspace_root or find_workspace_root()).resolve()
    fixture_paths = sorted(
        {
            resolve_workspace_path(path, root)
            for objective in objectives
            for path in objective.get("inputs", {}).get("fixture_paths", [])
        }
    )
    fixtures: list[dict[str, Any]] = []
    for path in fixture_paths:
        payload = load_json(path)
        fixtures.append(
            {
                "fixture": path.relative_to(root).as_posix(),
                "source_id": payload.get("source_id"),
                "source_url": payload.get("source_url") or payload.get("source_download_url") or payload.get("landing_url"),
                "geography": payload.get("geography") or payload.get("country_or_region"),
                "period": payload.get("period") or payload.get("year_range") or payload.get("temporal_coverage"),
                "license_status": payload.get("license_status") or payload.get("data_license") or payload.get("license_terms_summary"),
                "license_review_required": payload.get("license_review_required", True),
                "publication_gate": payload.get("publication_gate", "BLOCK"),
            }
        )
    return {
        "schema": "duat.license_review.v0_1",
        "publication_gate": "BLOCK",
        "license_terms_scan": "REVIEW",
        "reason": "LicenseTermsScan remains REVIEW pending human/legal review.",
        "fixtures": fixtures,
        "missing_for_pass": [
            "human/legal review of source-specific redistribution terms",
            "public-safe attribution text approved for each source",
            "explicit decision that derived fixture redistribution is allowed",
        ],
    }
