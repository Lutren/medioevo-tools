from __future__ import annotations

import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .permissions import evaluate_permission


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _contain(root: Path, target: str) -> Path:
    candidate = Path(target)
    if candidate.is_absolute():
        raise ValueError("absolute targets are not allowed")
    resolved_root = root.resolve()
    resolved_target = (resolved_root / candidate).resolve()
    if resolved_root != resolved_target and resolved_root not in resolved_target.parents:
        raise ValueError("target escapes root")
    return resolved_target


def rollback_root(root: str | Path) -> Path:
    return Path(root) / "runtime" / "rollback"


def execute_write_file(root: str | Path, payload: dict[str, Any]) -> dict[str, Any]:
    gate = evaluate_permission(payload)
    if gate["decision"] != "APPROVE":
        return {
            "status": "not_executed",
            "actiongate": gate["decision"],
            "reason": gate["reason"],
            "target": payload.get("target"),
        }

    base = Path(root)
    target = _contain(base, str(payload.get("target") or ""))
    content = str(payload.get("content") or "")
    rollback_id = f"rollback-{uuid.uuid4().hex}"
    rollback_dir = rollback_root(base) / rollback_id
    rollback_dir.mkdir(parents=True, exist_ok=False)
    backup_path = rollback_dir / "backup"
    existed = target.exists()
    if existed:
        shutil.copy2(target, backup_path)
    manifest = {
        "schema_version": "claudio.rollback.v0.1",
        "rollback_id": rollback_id,
        "created_at": _utc_now(),
        "target": str(target.relative_to(base.resolve())),
        "existed": existed,
        "backup": str(backup_path.relative_to(base)) if existed else None,
    }
    (rollback_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {
        "status": "executed",
        "actiongate": "APPROVE",
        "target": str(target.relative_to(base.resolve())),
        "rollback_id": rollback_id,
        "bytes_written": len(content.encode("utf-8")),
    }


def restore_rollback(root: str | Path, rollback_id: str) -> dict[str, Any]:
    base = Path(root)
    rollback_dir = rollback_root(base) / rollback_id
    manifest_path = rollback_dir / "manifest.json"
    if not manifest_path.exists():
        return {"status": "not_found", "rollback_id": rollback_id}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    target = _contain(base, str(manifest["target"]))
    if manifest.get("existed"):
        backup = base / str(manifest["backup"])
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup, target)
        restored = "file_restored"
    else:
        if target.exists():
            target.unlink()
        restored = "new_file_removed"
    return {
        "status": "restored",
        "rollback_id": rollback_id,
        "target": manifest["target"],
        "result": restored,
    }

