"""Registry JSON loaders and shape validators."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SOURCE_REQUIRED_FIELDS = {
    "source_id",
    "name",
    "domain",
    "official_url",
    "api_docs_url",
    "access_type",
    "license_status",
    "integration_gate",
    "publication_gate",
}

METHOD_REQUIRED_FIELDS = {
    "method_id",
    "name",
    "type",
    "formula",
    "best_for",
    "failure_modes",
    "metrics_required",
    "integration_gate",
    "publication_gate",
}


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_source_catalog(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("publication_gate") != "BLOCK":
        errors.append("catalog publication_gate must be BLOCK")
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty list")
        return errors
    for index, source in enumerate(sources):
        missing = sorted(SOURCE_REQUIRED_FIELDS.difference(source))
        if missing:
            errors.append(f"sources[{index}] missing {missing}")
        if source.get("access_type") in {"FREE_KEY", "REVIEW_KEY_REQUIRED"}:
            if "REVIEW" not in str(source.get("integration_gate", "")):
                errors.append(f"sources[{index}] key-based sources must be REVIEW")
    return errors


def validate_methods_catalog(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("publication_gate") != "BLOCK":
        errors.append("catalog publication_gate must be BLOCK")
    methods = payload.get("methods")
    if not isinstance(methods, list) or not methods:
        errors.append("methods must be a non-empty list")
        return errors
    for index, method in enumerate(methods):
        missing = sorted(METHOD_REQUIRED_FIELDS.difference(method))
        if missing:
            errors.append(f"methods[{index}] missing {missing}")
    return errors
