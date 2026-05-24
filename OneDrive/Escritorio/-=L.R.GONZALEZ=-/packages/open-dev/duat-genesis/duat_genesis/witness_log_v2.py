from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal


WitnessEventName = Literal[
    "artifact_created",
    "test_run",
    "gate_decision",
    "publication_update",
    "cleanup_delete",
    "handoff_created",
]


@dataclass(frozen=True)
class WitnessEvent:
    ts: str
    actor: str
    event: WitnessEventName
    path: str
    reason: str
    gate: Literal["APPROVE", "REVIEW", "BLOCK"]
    risk: Literal["low", "medium", "high"]
    hash: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


def make_witness_event(
    *,
    actor: str,
    event: WitnessEventName,
    path: str,
    reason: str,
    gate: Literal["APPROVE", "REVIEW", "BLOCK"],
    risk: Literal["low", "medium", "high"],
    hash: str = "",
    extra: dict[str, Any] | None = None,
) -> WitnessEvent:
    return WitnessEvent(
        ts=datetime.now(UTC).isoformat(),
        actor=actor,
        event=event,
        path=path,
        reason=reason,
        gate=gate,
        risk=risk,
        hash=hash,
        extra=dict(extra or {}),
    )


def event_to_jsonl(event: WitnessEvent) -> str:
    return json.dumps(asdict(event), sort_keys=True, separators=(",", ":"))


def append_witness_event(path: Path, event: WitnessEvent) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(event_to_jsonl(event) + "\n")
