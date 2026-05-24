from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .jsonutil import write_json
from .memory_lite import load_memory, memory_path
from .task_board import load_task_board, task_board_path
from .witness_log import load_witness_events, witness_path


WEIGHTS = {
    "uncertainty_component": 0.14,
    "contradiction_component": 0.14,
    "missing_evidence_component": 0.16,
    "ambiguity_component": 0.08,
    "stale_state_component": 0.08,
    "irreversible_risk_component": 0.14,
    "coordination_overhead_component": 0.10,
    "rollback_component": 0.06,
    "failure_component": 0.05,
    "review_block_component": 0.05,
}

SECRET_PRIVATE_MARKERS = {
    ".env",
    ".claw",
    ".claude",
    ".wrangler",
    "credential",
    "private_key",
    "secret",
    "token",
}

PRIVATE_PATH_MARKERS = {
    "metaevo-tcg",
    "game-private",
    "runtime/game_bridge",
    "runtime\\game_bridge",
    "claudio/tcg",
    "claudio\\tcg",
    "04_audiovisual_y_tcg",
}

PUBLICATION_MARKERS = {
    "deploy",
    "external_publish",
    "git_push",
    "github_write",
    "public_publish",
    "publish",
}

DESTRUCTIVE_MARKERS = {
    "delete",
    "destructive",
    "format_disk",
    "remove",
    "wipe",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, round(float(value), 4)))


def classify_regime(r_total: float) -> str:
    if r_total < 0.15:
        return "OPTIMO"
    if r_total < 0.40:
        return "FUNCIONAL"
    if r_total < 0.70:
        return "CARGADO"
    if r_total < 0.90:
        return "SATURADO"
    return "JAMMING"


def _component(count: int, denominator: int = 5) -> float:
    if count <= 0:
        return 0.0
    return _clamp(count / max(denominator, 1))


def _safe_contains(value: Any, markers: set[str]) -> bool:
    text = str(value or "").replace("\\", "/").lower()
    return any(marker.lower().replace("\\", "/") in text for marker in markers)


def _safe_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name


def _read_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _package_roots(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for candidate in [root, root.parent, root.parent.parent]:
        if candidate not in candidates:
            candidates.append(candidate)
    return candidates


def _find_first(root: Path, filename: str) -> Path | None:
    for candidate in _package_roots(root):
        path = candidate / filename
        if path.exists():
            return path
    return None


def _load_tasks(root: Path, source_files: list[str]) -> list[dict[str, Any]]:
    path = task_board_path(root)
    try:
        board = load_task_board(root)
    except (OSError, json.JSONDecodeError, ValueError):
        board = {"tasks": []}
    if path.exists():
        source_files.append(_safe_path(path, root))
    tasks = board.get("tasks")
    return [task for task in tasks if isinstance(task, dict)] if isinstance(tasks, list) else []


def _load_memory(root: Path, source_files: list[str]) -> list[dict[str, Any]]:
    path = memory_path(root)
    try:
        records = load_memory(root)
    except (OSError, json.JSONDecodeError, ValueError):
        records = []
    if path.exists():
        source_files.append(_safe_path(path, root))
    return records


def _load_witness(root: Path, source_files: list[str]) -> list[dict[str, Any]]:
    path = witness_path(root)
    try:
        events = load_witness_events(root)
    except (OSError, json.JSONDecodeError, ValueError):
        events = []
    if path.exists():
        source_files.append(_safe_path(path, root))
    return events


def _rollback_manifests(root: Path, source_files: list[str]) -> list[dict[str, Any]]:
    rollback_dir = root / "runtime" / "rollback"
    manifests: list[dict[str, Any]] = []
    if not rollback_dir.exists():
        return manifests
    for manifest_path in sorted(rollback_dir.glob("*/manifest.json")):
        data = _read_json_if_exists(manifest_path)
        if data is not None:
            manifests.append(data)
            source_files.append(_safe_path(manifest_path, root))
    return manifests


def _load_fingerprint(root: Path, source_files: list[str]) -> dict[str, Any] | None:
    path = _find_first(root, "SESSION_FINGERPRINT.json")
    if path is None:
        return None
    data = _read_json_if_exists(path)
    if data is not None:
        source_files.append(_safe_path(path, root))
    return data


def _load_test_report(root: Path, source_files: list[str]) -> str:
    path = _find_first(root, "TEST_REPORT.md")
    if path is None:
        return ""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    source_files.append(_safe_path(path, root))
    return text


def _count_task_signals(tasks: list[dict[str, Any]]) -> dict[str, int]:
    statuses = Counter(str(task.get("status") or "pending").strip().lower() for task in tasks)
    completed = statuses["completed"] + statuses["done"] + statuses["closed"] + statuses["passed"]
    failed = statuses["failed"] + statuses["error"]
    blocked = statuses["blocked"] + statuses["block"]
    reviewed = statuses["review"] + statuses["review_required"] + statuses["reviewed"]
    handoff_created = sum(
        1
        for task in tasks
        if task.get("handoff_created") is True or bool(task.get("handoff")) or bool(task.get("handoff_path"))
    )
    handoff_missing = sum(
        1
        for task in tasks
        if str(task.get("status") or "").lower() in {"completed", "done", "closed"} and not (
            task.get("handoff_created") is True or task.get("handoff") or task.get("handoff_path")
        )
    )
    evidence_missing = sum(1 for task in tasks if not task.get("evidence"))
    return {
        "tasks_created": len(tasks),
        "tasks_completed": completed,
        "tasks_failed": failed,
        "tasks_blocked": blocked,
        "tasks_reviewed": reviewed,
        "handoff_created": handoff_created,
        "handoff_missing": handoff_missing,
        "task_missing_evidence": evidence_missing,
    }


def _count_memory_signals(records: list[dict[str, Any]]) -> dict[str, int]:
    missing = stale = contradictions = unresolved = ambiguous = evidence_backed = 0
    for record in records:
        joined = " ".join(
            str(record.get(key) or "")
            for key in ("type", "summary", "source", "durability", "evidence_status", "claim_class", "status")
        ).lower()
        tags = " ".join(str(tag).lower() for tag in record.get("boundary_tags") or [])
        haystack = f"{joined} {tags}"
        if "missing evidence" in haystack or "evidence_missing" in haystack or "needs_evidence" in haystack:
            missing += 1
        if "stale" in haystack or "obsolete" in haystack or "outdated" in haystack:
            stale += 1
        if "contradiction" in haystack or "contradicted" in haystack or "conflict" in haystack:
            contradictions += 1
        if "unknown" in haystack or "unresolved" in haystack or "incognita" in haystack:
            unresolved += 1
        if "ambiguous" in haystack or "ambiguity" in haystack:
            ambiguous += 1
        if record.get("source") and float(record.get("confidence") or 0) >= 0.7:
            evidence_backed += 1
    return {
        "memory_records": len(records),
        "missing_evidence": missing,
        "stale_state": stale,
        "contradictions": contradictions,
        "unresolved_items": unresolved,
        "ambiguity": ambiguous,
        "evidence_backed_claims": evidence_backed,
    }


def _count_witness_signals(events: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "total_actions": len(events),
        "approve_count": 0,
        "review_count": 0,
        "block_count": 0,
        "failed_commands": 0,
        "errors": 0,
        "claims": 0,
        "evidence_backed_claims": 0,
        "plan_only_violations": 0,
        "rollback_success": 0,
        "rollback_failure": 0,
        "publication_attempts": 0,
        "secret_private_path_findings": 0,
        "destructive_actions": 0,
    }
    for event in events:
        gate = str(event.get("actiongate") or event.get("decision") or "").upper()
        command = str(event.get("command") or event.get("action") or "").lower()
        status = str(event.get("status") or "").lower()
        summary = event.get("result_summary") if isinstance(event.get("result_summary"), dict) else {}
        payload_text = json.dumps(event, ensure_ascii=True, sort_keys=True, default=str).lower()
        risk_text = " ".join(
            str(event.get(key) or "")
            for key in ("target", "path", "reason", "action", "command")
        ).lower()

        if gate == "APPROVE":
            counts["approve_count"] += 1
        if gate == "REVIEW":
            counts["review_count"] += 1
        if gate == "BLOCK":
            counts["block_count"] += 1
        if status in {"failed", "error", "not_found", "not_executed"}:
            counts["failed_commands"] += 1
        if "error" in payload_text:
            counts["errors"] += 1
        if "claim" in payload_text:
            counts["claims"] += 1
        if "evidence" in payload_text and "missing" not in payload_text:
            counts["evidence_backed_claims"] += 1
        if "ghostgate" in command and gate in {"REVIEW", "BLOCK"}:
            counts["plan_only_violations"] += 1
        if "rollback restore" in command and status == "ok":
            counts["rollback_success"] += 1
        if "rollback" in command and (status in {"failed", "error", "not_found"} or "not_found" in payload_text):
            counts["rollback_failure"] += 1
        if _safe_contains(command, PUBLICATION_MARKERS) or _safe_contains(payload_text, PUBLICATION_MARKERS):
            counts["publication_attempts"] += 1
        if _safe_contains(risk_text, SECRET_PRIVATE_MARKERS) or _safe_contains(risk_text, PRIVATE_PATH_MARKERS):
            counts["secret_private_path_findings"] += 1
        if _safe_contains(command, DESTRUCTIVE_MARKERS) or _safe_contains(payload_text, DESTRUCTIVE_MARKERS):
            counts["destructive_actions"] += 1
        if str(summary.get("decision") or "").upper() == "BLOCK":
            counts["block_count"] += 1
    return counts


def _count_fingerprint_signals(fingerprint: dict[str, Any] | None, test_report: str) -> dict[str, int]:
    counts = {
        "passed_tests": 0,
        "commands_recorded": 0,
        "fingerprint_approvals": 0,
        "fingerprint_reviews": 0,
        "fingerprint_blocks": 0,
    }
    if fingerprint:
        tests = fingerprint.get("tests") if isinstance(fingerprint.get("tests"), dict) else {}
        if tests.get("status") == "passed":
            counts["passed_tests"] += 1
        evidence = tests.get("evidence") if isinstance(tests.get("evidence"), list) else []
        counts["passed_tests"] += sum(1 for item in evidence if "passed" in str(item).lower())
        commands = fingerprint.get("commands_run")
        counts["commands_recorded"] += len(commands) if isinstance(commands, list) else 0
        gate = fingerprint.get("actiongate_summary") if isinstance(fingerprint.get("actiongate_summary"), dict) else {}
        counts["fingerprint_approvals"] += int(gate.get("approved") or 0)
        counts["fingerprint_reviews"] += int(gate.get("review_required") or 0)
        counts["fingerprint_blocks"] += int(gate.get("blocked") or 0)
    lowered = test_report.lower()
    if "passed" in lowered and "pytest" in lowered:
        counts["passed_tests"] += 1
    return counts


def _count_rollback_signals(manifests: list[dict[str, Any]], witness_counts: dict[str, int]) -> dict[str, int]:
    return {
        "rollback_count": len(manifests),
        "successful_rollbacks": witness_counts["rollback_success"],
        "rollback_failures": witness_counts["rollback_failure"],
    }


def _raw_counts(root: Path, source_files: list[str]) -> dict[str, int]:
    tasks = _load_tasks(root, source_files)
    memory = _load_memory(root, source_files)
    witness = _load_witness(root, source_files)
    manifests = _rollback_manifests(root, source_files)
    fingerprint = _load_fingerprint(root, source_files)
    test_report = _load_test_report(root, source_files)

    counts: dict[str, int] = {}
    for group in (
        _count_task_signals(tasks),
        _count_memory_signals(memory),
        _count_witness_signals(witness),
        _count_fingerprint_signals(fingerprint, test_report),
    ):
        counts.update(group)
    counts.update(_count_rollback_signals(manifests, counts))
    counts["reviews"] = counts["review_count"] + counts["tasks_reviewed"] + counts["fingerprint_reviews"]
    counts["blocks"] = counts["block_count"] + counts["tasks_blocked"] + counts["fingerprint_blocks"]
    counts["failures"] = counts["failed_commands"] + counts["tasks_failed"]
    counts["missing_evidence_total"] = (
        counts["missing_evidence"] + counts["task_missing_evidence"] + counts["handoff_missing"]
    )
    counts["unresolved_total"] = counts["unresolved_items"] + max(counts["tasks_created"] - counts["tasks_completed"], 0)
    counts["approved_total"] = counts["approve_count"] + counts["fingerprint_approvals"]
    return counts


def _components(counts: dict[str, int]) -> dict[str, float]:
    review_block_total = counts["reviews"] + counts["blocks"]
    irreversible_risk = (
        counts["destructive_actions"]
        + counts["publication_attempts"]
        + counts["rollback_failures"]
        + counts["secret_private_path_findings"]
    )
    return {
        "uncertainty_component": _component(counts["unresolved_total"], 8),
        "contradiction_component": _component(counts["contradictions"], 3),
        "missing_evidence_component": _component(counts["missing_evidence_total"], 6),
        "ambiguity_component": _component(counts["ambiguity"] + counts["plan_only_violations"], 4),
        "stale_state_component": _component(counts["stale_state"], 4),
        "irreversible_risk_component": _component(irreversible_risk, 4),
        "coordination_overhead_component": _component(
            counts["reviews"] + counts["blocks"] + counts["commands_recorded"], 30
        ),
        "rollback_component": _component(counts["rollback_count"] + counts["rollback_failures"], 6),
        "failure_component": _component(counts["failures"] + counts["errors"], 5),
        "review_block_component": _component(review_block_total, 10),
    }


def _r_total(components: dict[str, float]) -> float:
    return _clamp(sum(WEIGHTS[name] * components[name] for name in WEIGHTS))


def _phi_eff(counts: dict[str, int]) -> float:
    verified_output = (
        counts["tasks_completed"]
        + counts["passed_tests"]
        + counts["handoff_created"]
        + counts["evidence_backed_claims"]
        + counts["successful_rollbacks"]
        + counts["approved_total"]
    )
    coordination_cost = (
        counts["total_actions"]
        + counts["reviews"]
        + counts["blocks"]
        + counts["failed_commands"]
        + counts["missing_evidence_total"]
        + counts["rollback_count"]
        + counts["stale_state"]
        + counts["unresolved_total"]
    )
    return _clamp(verified_output / max(verified_output + coordination_cost, 1))


def _actiongate_suggestion(r_total: float, phi_eff: float, components: dict[str, float], counts: dict[str, int]) -> str:
    if (
        counts["secret_private_path_findings"] > 0
        or counts["publication_attempts"] > 0
        or counts["destructive_actions"] > 0
        or r_total >= 0.90
        or counts["rollback_failures"] > 0
    ):
        return "BLOCK"
    if (
        r_total <= 0.25
        and phi_eff >= 0.75
        and counts["blocks"] == 0
        and components["irreversible_risk_component"] < 0.25
    ):
        return "APPROVE"
    if r_total <= 0.60 and phi_eff >= 0.45:
        return "REVIEW"
    return "BLOCK" if r_total >= 0.90 else "REVIEW"


def _recommendations(suggestion: str, counts: dict[str, int], components: dict[str, float]) -> list[str]:
    recs: list[str] = []
    if suggestion == "APPROVE":
        recs.append("Continue local reversible work and keep WitnessLog evidence current.")
    if suggestion == "REVIEW":
        recs.append("Close bounded missing evidence, review events, or unresolved tasks before widening scope.")
    if suggestion == "BLOCK":
        recs.append("Stop execution and resolve blocked risk before further writes.")
    if counts["missing_evidence_total"]:
        recs.append("Add evidence references or Source Cards for items without evidence.")
    if counts["rollback_failures"]:
        recs.append("Repair rollback restore before allowing destructive or irreversible writes.")
    if components["coordination_overhead_component"] >= 0.5:
        recs.append("Reduce coordination overhead by closing or archiving stale work episodes.")
    if not recs:
        recs.append("Maintain current local-only operating boundary.")
    return recs


def calculate_rphi_budget(root: str | Path = ".") -> dict[str, Any]:
    state_root = Path(root)
    source_files: list[str] = []
    counts = _raw_counts(state_root, source_files)
    components = _components(counts)
    r_total = _r_total(components)
    phi_eff = _phi_eff(counts)
    suggestion = _actiongate_suggestion(r_total, phi_eff, components, counts)
    return {
        "schema_version": "claudio.rphi_budget.v0.1",
        "generated_at": _utc_now(),
        "r_total": r_total,
        "phi_eff": phi_eff,
        "regime": classify_regime(r_total),
        "actiongate_suggestion": suggestion,
        "components": components,
        "raw_counts": dict(sorted(counts.items())),
        "recommendations": _recommendations(suggestion, counts, components),
        "source_files_used": sorted(dict.fromkeys(source_files)),
    }


def render_rphi_report(budget: dict[str, Any]) -> str:
    counts = budget["raw_counts"]
    files = budget["source_files_used"]
    lines = [
        "# RPHI Budget Report",
        "",
        "Status: `LOCAL_ONLY`",
        "",
        "ESTADO",
        f"R_est: {budget['r_total']:.4f}",
        f"Phi_eff_est: {budget['phi_eff']:.4f}",
        f"Regimen: {budget['regime']}",
        f"ActionGate: {budget['actiongate_suggestion']}",
        "",
        "CERTEZA",
        "- observed local signals:",
        f"  - tasks_created: {counts['tasks_created']}",
        f"  - tasks_completed: {counts['tasks_completed']}",
        f"  - passed_tests: {counts['passed_tests']}",
        f"  - witness_events: {counts['total_actions']}",
        f"  - memory_records: {counts['memory_records']}",
        f"  - reviews: {counts['reviews']}",
        f"  - blocks: {counts['blocks']}",
        f"  - rollback_count: {counts['rollback_count']}",
        f"- files read: {', '.join(files) if files else 'none'}",
        "",
        "INFERENCIA",
        f"- The current local budget suggests `{budget['actiongate_suggestion']}` for the next bounded action.",
        f"- Regime is `{budget['regime']}` from deterministic local residue components.",
        "",
        "INCOGNITA",
        "- Missing source files are treated as unavailable signals, not as fatal errors.",
        "",
        "ACCION",
        f"- Next recommended local action: {budget['recommendations'][0]}",
        "",
        "ARTEFACTO",
        "- JSON budget path: `qa_artifacts/rphi-budget-latest.json`",
        "- Markdown report path: `qa_artifacts/rphi-budget-report-latest.md`",
        "",
        "HANDOFF",
        "Fingerprint: RPHI-BUDGET-v0.1",
        "Brief: Deterministic local R/Phi budget generated from available runtime artifacts.",
        "Next: Keep closing local work with evidence before opening external or irreversible scope.",
    ]
    return "\n".join(lines) + "\n"


def write_rphi_artifacts(root: str | Path = ".", output_root: str | Path | None = None) -> dict[str, Any]:
    state_root = Path(root)
    artifact_root = Path(output_root) if output_root is not None else state_root / "qa_artifacts"
    budget = calculate_rphi_budget(state_root)
    json_path = artifact_root / "rphi-budget-latest.json"
    report_path = artifact_root / "rphi-budget-report-latest.md"
    write_json(json_path, budget)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_rphi_report(budget), encoding="utf-8")
    return {
        "budget": budget,
        "json_path": str(json_path),
        "markdown_report_path": str(report_path),
    }
