"""Predictive objective loading and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_OBJECTIVE_FIELDS = {
    "objective_id",
    "version",
    "status",
    "synthetic",
    "target_type",
    "prediction_task",
    "canonical_indicator_id",
    "data_policy",
    "inputs",
    "evaluation",
    "gates",
}


def find_workspace_root(start: str | Path | None = None) -> Path:
    """Find the MEDIOEVO workspace root without relying on private absolute paths."""

    current = Path(start or __file__).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").exists() and (candidate / "research").exists():
            return candidate
    raise FileNotFoundError("Could not locate workspace root with AGENTS.md and research/")


def resolve_workspace_path(path: str | Path, workspace_root: str | Path | None = None) -> Path:
    """Resolve a path relative to the workspace root if it is not absolute."""

    raw = Path(path)
    if raw.is_absolute():
        return raw
    return Path(workspace_root or find_workspace_root()).resolve() / raw


def load_objective(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_objective(objective: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_OBJECTIVE_FIELDS.difference(objective))
    if missing:
        errors.append(f"objective missing required fields: {missing}")
        return errors

    data_policy = objective.get("data_policy", {})
    if data_policy.get("offline_only") is not True:
        errors.append("data_policy.offline_only must be true")
    if data_policy.get("private_data") is not False:
        errors.append("data_policy.private_data must be false")
    if data_policy.get("external_api") is not False:
        errors.append("data_policy.external_api must be false")
    if data_policy.get("publication_gate") != "BLOCK":
        errors.append("data_policy.publication_gate must be BLOCK")
    if objective.get("prediction_task") != "one_step_ahead_forecast":
        errors.append("prediction_task must be one_step_ahead_forecast")

    inputs = objective.get("inputs", {})
    if not inputs.get("fixture_paths"):
        errors.append("inputs.fixture_paths must not be empty")
    if not inputs.get("crosswalk_path"):
        errors.append("inputs.crosswalk_path is required")

    gates = objective.get("gates", {})
    if gates.get("stop_on_secret") is not True:
        errors.append("gates.stop_on_secret must be true")
    if gates.get("stop_on_private_data") is not True:
        errors.append("gates.stop_on_private_data must be true")
    if gates.get("license_review_is_publication_block") is not True:
        errors.append("gates.license_review_is_publication_block must be true")
    return errors
