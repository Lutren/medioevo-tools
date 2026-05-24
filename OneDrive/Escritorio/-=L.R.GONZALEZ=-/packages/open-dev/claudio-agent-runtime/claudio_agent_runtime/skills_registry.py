from __future__ import annotations

from pathlib import Path
from typing import Any


def _parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    meta: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def discover_skills(root: str | Path) -> list[dict[str, Any]]:
    base = Path(root)
    if not base.exists():
        return []
    records: list[dict[str, Any]] = []
    for skill_path in sorted(base.rglob("SKILL.md")):
        text = skill_path.read_text(encoding="utf-8")
        meta = _parse_frontmatter(text)
        name = meta.get("name") or skill_path.parent.name
        description = meta.get("description") or ""
        gate = meta.get("gate") or "REVIEW"
        records.append(
            {
                "name": name,
                "description": description,
                "gate": gate,
                "path": str(skill_path),
                "loaded": False,
            }
        )
    return records


def inspect_skill(path: str | Path) -> dict[str, Any]:
    skill_path = Path(path)
    text = skill_path.read_text(encoding="utf-8")
    meta = _parse_frontmatter(text)
    return {
        "name": meta.get("name") or skill_path.parent.name,
        "description": meta.get("description") or "",
        "gate": meta.get("gate") or "REVIEW",
        "path": str(skill_path),
        "body": text,
        "loaded": True,
    }

