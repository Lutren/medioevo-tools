from __future__ import annotations

from pathlib import PureWindowsPath
from typing import Any


BLOCK_ACTIONS = {
    "delete_secret",
    "destructive_cleanup",
    "format_disk",
    "private_game_write",
    "raw_secret_read",
    "touch_secret",
}

REVIEW_ACTIONS = {
    "external_publish",
    "external_write",
    "github_write",
    "install_dependency",
    "network",
    "public_publish",
    "service_install",
    "spotify_action",
    "telegram_message",
}

BLOCK_TAGS = {
    "book_fulltext",
    "destructive",
    "private_game",
    "rpg",
    "secret",
    "tcg",
    "touches_secret",
}

REVIEW_TAGS = {
    "credential",
    "dependency",
    "external",
    "github",
    "legal",
    "network",
    "payment",
    "publication",
    "service",
    "social",
}

SENSITIVE_PATH_PARTS = {
    ".env",
    ".claude",
    ".claw",
    ".wrangler",
    "credential",
    "credentials",
    "secret",
    "secrets",
    "token",
    "tokens",
}

PRIVATE_PATH_PARTS = {
    "metaevo-tcg",
    "game-private",
    "runtime\\game_bridge",
    "claudio\\tcg",
    "04_audiovisual_y_tcg",
}


def _norm(value: Any) -> str:
    return str(value or "").strip().lower()


def _tags(payload: dict[str, Any]) -> set[str]:
    raw = payload.get("risk_tags") or payload.get("policy_tags") or payload.get("tags") or []
    if not isinstance(raw, list):
        return set()
    return {_norm(item) for item in raw}


def _path_parts(target: str) -> set[str]:
    lowered = target.replace("/", "\\").lower()
    parts = {part for part in PureWindowsPath(lowered).parts if part}
    parts.add(lowered)
    return parts


def evaluate_permission(payload: dict[str, Any]) -> dict[str, Any]:
    action = _norm(payload.get("action") or payload.get("action_type"))
    target = _norm(payload.get("target") or payload.get("path"))
    tags = _tags(payload)
    parts = _path_parts(target)

    reasons: list[str] = []

    if action in BLOCK_ACTIONS:
        reasons.append(f"blocked action: {action}")
    if tags & BLOCK_TAGS:
        reasons.append(f"blocked tags: {', '.join(sorted(tags & BLOCK_TAGS))}")
    if any(part in SENSITIVE_PATH_PARTS for part in parts) or any(key in target for key in SENSITIVE_PATH_PARTS):
        reasons.append("target looks secret-like")
    if any(key in target for key in PRIVATE_PATH_PARTS):
        reasons.append("target is inside a private boundary")

    if reasons:
        return {
            "decision": "BLOCK",
            "reason": "; ".join(reasons),
            "review_required": False,
            "blocked": True,
            "risk_tags": sorted(tags),
        }

    review_reasons: list[str] = []
    if action in REVIEW_ACTIONS:
        review_reasons.append(f"review action: {action}")
    if tags & REVIEW_TAGS:
        review_reasons.append(f"review tags: {', '.join(sorted(tags & REVIEW_TAGS))}")

    if review_reasons:
        return {
            "decision": "REVIEW",
            "reason": "; ".join(review_reasons),
            "review_required": True,
            "blocked": False,
            "risk_tags": sorted(tags),
        }

    local = "local" in tags or _norm(payload.get("scope")) in {"workspace", "local"}
    reversible = "reversible" in tags or bool(payload.get("reversible"))
    if local and reversible:
        reason = "local reversible action inside declared scope"
    else:
        reason = "low-risk dry-run/local action"

    return {
        "decision": "APPROVE",
        "reason": reason,
        "review_required": False,
        "blocked": False,
        "risk_tags": sorted(tags),
    }

