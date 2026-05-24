from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


def memory_path(root: str | Path) -> Path:
    return Path(root) / "memory" / "memory_lite.jsonl"


def load_memory(root: str | Path) -> list[dict[str, Any]]:
    path = memory_path(root)
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if isinstance(item, dict):
            records.append(item)
    return records


def memory_status(root: str | Path) -> dict[str, Any]:
    records = load_memory(root)
    by_type = Counter(str(item.get("type") or "unknown") for item in records)
    by_durability = Counter(str(item.get("durability") or "unknown") for item in records)
    return {
        "path": str(memory_path(root)),
        "exists": memory_path(root).exists(),
        "count": len(records),
        "by_type": dict(sorted(by_type.items())),
        "by_durability": dict(sorted(by_durability.items())),
        "entries_redacted": True,
    }


def search_memory(root: str | Path, query: str) -> list[dict[str, Any]]:
    q = query.lower().strip()
    if not q:
        return []
    results: list[dict[str, Any]] = []
    for item in load_memory(root):
        haystack = " ".join(
            str(item.get(key) or "")
            for key in ("type", "summary", "source", "durability")
        ).lower()
        if q in haystack:
            results.append(
                {
                    "type": item.get("type"),
                    "summary": item.get("summary"),
                    "source": item.get("source"),
                    "confidence": item.get("confidence"),
                    "durability": item.get("durability"),
                }
            )
    return results

