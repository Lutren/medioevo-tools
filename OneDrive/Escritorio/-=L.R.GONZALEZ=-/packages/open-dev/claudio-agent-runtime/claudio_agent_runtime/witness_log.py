from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def witness_path(root: str | Path) -> Path:
    return Path(root) / "witness" / "witness_log.jsonl"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _stable_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def summarize_result(command: str, result: Any) -> dict[str, Any]:
    if not isinstance(result, dict):
        return {
            "kind": type(result).__name__,
            "sha256": _stable_digest(result),
            "redacted": True,
        }

    summary: dict[str, Any] = {
        "kind": "dict",
        "keys": sorted(str(key) for key in result.keys()),
        "sha256": _stable_digest(result),
        "redacted": True,
    }
    if "decision" in result:
        summary["decision"] = result.get("decision")
    if "count" in result:
        summary["count"] = result.get("count")
    if command == "doctor":
        summary["external_channels"] = result.get("external_channels")
        summary["secret_presence_only"] = result.get("secrets", {}).get("presence_only") is True
        summary["secret_values_printed"] = result.get("secrets", {}).get("values_printed") is True
    if command.startswith("skills"):
        summary["skill_count"] = len(result.get("skills", [])) if isinstance(result.get("skills"), list) else None
    return summary


def append_witness_event(
    root: str | Path,
    *,
    command: str,
    status: str,
    result: Any,
    actiongate: str = "APPROVE",
) -> dict[str, Any]:
    event = {
        "schema_version": "claudio.witness_log.v0.1",
        "event_id": f"evt-{uuid.uuid4().hex}",
        "created_at": _utc_now(),
        "command": command,
        "status": status,
        "actiongate": actiongate,
        "result_summary": summarize_result(command, result),
    }
    path = witness_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=True, sort_keys=True) + "\n")
    return {"path": str(path), "event_id": event["event_id"]}


def load_witness_events(root: str | Path) -> list[dict[str, Any]]:
    path = witness_path(root)
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if isinstance(item, dict):
            events.append(item)
    return events


def witness_status(root: str | Path) -> dict[str, Any]:
    events = load_witness_events(root)
    return {
        "path": str(witness_path(root)),
        "exists": witness_path(root).exists(),
        "count": len(events),
        "append_only_contract": True,
        "entries_redacted": True,
        "last_event_id": events[-1].get("event_id") if events else None,
    }

