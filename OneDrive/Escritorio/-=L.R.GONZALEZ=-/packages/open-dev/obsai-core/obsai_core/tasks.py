from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal


TaskStatus = Literal["OPEN", "CLOSED", "BLOCKED"]
TaskPriority = Literal["P0", "P1", "P2", "P3"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TaskEvidence:
    label: str
    source: str
    verified: bool = False
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "source": self.source,
            "verified": self.verified,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TaskEvidence":
        return cls(
            label=str(payload.get("label") or ""),
            source=str(payload.get("source") or ""),
            verified=bool(payload.get("verified")),
            note=str(payload.get("note") or ""),
        )


@dataclass
class TaskRecord:
    title: str
    priority: TaskPriority = "P2"
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus = "OPEN"
    evidence: list[TaskEvidence] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    closed_at: str | None = None
    note: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.task_id,
            "title": self.title,
            "priority": self.priority,
            "status": self.status,
            "evidence": [item.to_dict() for item in self.evidence],
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "closedAt": self.closed_at,
            "note": self.note,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TaskRecord":
        return cls(
            task_id=str(payload.get("id") or uuid.uuid4()),
            title=str(payload.get("title") or ""),
            priority=_priority(payload.get("priority")),
            status=_status(payload.get("status")),
            evidence=[
                TaskEvidence.from_dict(item)
                for item in payload.get("evidence", [])
                if isinstance(item, dict)
            ],
            created_at=str(payload.get("createdAt") or utc_now()),
            updated_at=str(payload.get("updatedAt") or utc_now()),
            closed_at=payload.get("closedAt"),
            note=str(payload.get("note") or ""),
            metadata=payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {},
        )


class TaskManager:
    """Small local task ledger with evidence-gated closure."""

    schema_version = "obsai.task_manager.v1"

    def __init__(self, tasks: list[TaskRecord] | None = None):
        self._tasks: dict[str, TaskRecord] = {}
        for task in tasks or []:
            self._tasks[task.task_id] = task

    def add_task(
        self,
        title: str,
        *,
        priority: TaskPriority = "P2",
        evidence: list[TaskEvidence] | None = None,
        note: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> TaskRecord:
        if not title.strip():
            raise ValueError("task title is required")
        task = TaskRecord(
            title=title.strip(),
            priority=_priority(priority),
            evidence=evidence or [],
            note=note,
            metadata=metadata or {},
        )
        self._tasks[task.task_id] = task
        return task

    def add_evidence(self, task_id: str, evidence: TaskEvidence) -> TaskRecord:
        task = self.get_task(task_id)
        task.evidence.append(evidence)
        task.updated_at = utc_now()
        return task

    def close_task(self, task_id: str, *, evidence: TaskEvidence | None = None, note: str = "") -> TaskRecord:
        task = self.get_task(task_id)
        if evidence is not None:
            task.evidence.append(evidence)
        if not task.evidence:
            raise ValueError("cannot close task without evidence")
        task.status = "CLOSED"
        task.closed_at = utc_now()
        task.updated_at = task.closed_at
        if note:
            task.note = note
        return task

    def block_task(self, task_id: str, *, note: str) -> TaskRecord:
        if not note.strip():
            raise ValueError("blocked task note is required")
        task = self.get_task(task_id)
        task.status = "BLOCKED"
        task.note = note.strip()
        task.updated_at = utc_now()
        return task

    def get_task(self, task_id: str) -> TaskRecord:
        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise KeyError(f"unknown task id: {task_id}") from exc

    def list_tasks(self, *, status: TaskStatus | None = None) -> list[TaskRecord]:
        tasks = list(self._tasks.values())
        if status is not None:
            normalized = _status(status)
            tasks = [task for task in tasks if task.status == normalized]
        return sorted(tasks, key=lambda task: (task.status, task.priority, task.created_at, task.title))

    def summary(self) -> dict[str, Any]:
        counts = {"OPEN": 0, "CLOSED": 0, "BLOCKED": 0}
        for task in self._tasks.values():
            counts[task.status] = counts.get(task.status, 0) + 1
        return {
            "schemaVersion": self.schema_version,
            "total": len(self._tasks),
            "byStatus": counts,
            "open": [task.to_dict() for task in self.list_tasks(status="OPEN")],
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": self.schema_version,
            "tasks": [task.to_dict() for task in self.list_tasks()],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TaskManager":
        tasks = [
            TaskRecord.from_dict(item)
            for item in payload.get("tasks", [])
            if isinstance(item, dict)
        ]
        return cls(tasks)

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "TaskManager":
        source = Path(path)
        if not source.exists():
            return cls()
        return cls.from_dict(json.loads(source.read_text(encoding="utf-8")))


def _priority(value: Any) -> TaskPriority:
    normalized = str(value or "P2").upper()
    if normalized not in {"P0", "P1", "P2", "P3"}:
        raise ValueError("priority must be P0, P1, P2 or P3")
    return normalized  # type: ignore[return-value]


def _status(value: Any) -> TaskStatus:
    normalized = str(value or "OPEN").upper()
    if normalized not in {"OPEN", "CLOSED", "BLOCKED"}:
        raise ValueError("status must be OPEN, CLOSED or BLOCKED")
    return normalized  # type: ignore[return-value]
