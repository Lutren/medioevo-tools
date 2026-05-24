from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from .jsonutil import read_json, write_json


def task_board_path(root: str | Path) -> Path:
    return Path(root) / "tasks" / "task_board.json"


def load_task_board(root: str | Path) -> dict[str, Any]:
    path = task_board_path(root)
    if not path.exists():
        return {"schema_version": "claudio.task_board.v0.1", "tasks": []}
    data = read_json(path)
    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        data["tasks"] = []
    return data


def list_tasks(root: str | Path) -> dict[str, Any]:
    data = load_task_board(root)
    tasks = []
    for task in data.get("tasks", []):
        if not isinstance(task, dict):
            continue
        tasks.append(
            {
                "id": task.get("id"),
                "title": task.get("title"),
                "status": task.get("status", "pending"),
                "priority": task.get("priority", "P2"),
                "owner": task.get("owner", "unassigned"),
                "evidence_count": len(task.get("evidence") or []),
            }
        )
    return {"path": str(task_board_path(root)), "count": len(tasks), "tasks": tasks}


def add_task(root: str | Path, task_payload: dict[str, Any]) -> dict[str, Any]:
    data = load_task_board(root)
    task = dict(task_payload)
    task.setdefault("id", f"task-{uuid.uuid4().hex[:8]}")
    task.setdefault("status", "pending")
    task.setdefault("priority", "P2")
    task.setdefault("owner", "claudio-agent-runtime")
    task.setdefault("evidence", [])
    data.setdefault("tasks", []).append(task)
    write_json(task_board_path(root), data)
    return {"added": task["id"], "path": str(task_board_path(root)), "count": len(data["tasks"])}

