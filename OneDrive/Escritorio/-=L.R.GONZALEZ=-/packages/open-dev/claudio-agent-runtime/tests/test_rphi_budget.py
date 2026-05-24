from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from claudio_agent_runtime.rphi_budget import calculate_rphi_budget, classify_regime, write_rphi_artifacts


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(data, ensure_ascii=True, sort_keys=True) + "\n")


def test_empty_inputs_return_safe_defaults(tmp_path: Path) -> None:
    budget = calculate_rphi_budget(tmp_path)
    assert budget["r_total"] == 0.0
    assert budget["phi_eff"] == 0.0
    assert budget["regime"] == "OPTIMO"
    assert budget["actiongate_suggestion"] == "REVIEW"
    assert budget["source_files_used"] == []


def test_missing_files_do_not_crash(tmp_path: Path) -> None:
    state = tmp_path / "missing-state"
    budget = calculate_rphi_budget(state)
    assert budget["raw_counts"]["tasks_created"] == 0
    assert budget["raw_counts"]["memory_records"] == 0
    assert budget["raw_counts"]["total_actions"] == 0


def test_high_missing_evidence_raises_r(tmp_path: Path) -> None:
    clean = calculate_rphi_budget(tmp_path)
    memory = tmp_path / "memory" / "memory_lite.jsonl"
    for index in range(6):
        _append_jsonl(
            memory,
            {
                "schema_version": "claudio.memory_lite.v0.1",
                "type": "claim",
                "summary": f"missing evidence item {index}",
                "evidence_status": "missing_evidence",
            },
        )
    budget = calculate_rphi_budget(tmp_path)
    assert budget["components"]["missing_evidence_component"] == 1.0
    assert budget["r_total"] > clean["r_total"]


def test_failed_rollback_triggers_block(tmp_path: Path) -> None:
    _append_jsonl(
        tmp_path / "witness" / "witness_log.jsonl",
        {
            "schema_version": "claudio.witness_log.v0.1",
            "event_id": "evt-rollback-failed",
            "command": "rollback restore",
            "status": "not_found",
            "actiongate": "APPROVE",
            "result_summary": {"kind": "dict", "redacted": True},
        },
    )
    budget = calculate_rphi_budget(tmp_path)
    assert budget["raw_counts"]["rollback_failures"] == 1
    assert budget["actiongate_suggestion"] == "BLOCK"


def test_presence_only_secret_reporting_does_not_trigger_private_path_block(tmp_path: Path) -> None:
    _append_jsonl(
        tmp_path / "witness" / "witness_log.jsonl",
        {
            "schema_version": "claudio.witness_log.v0.1",
            "event_id": "evt-doctor",
            "command": "doctor",
            "status": "ok",
            "actiongate": "APPROVE",
            "result_summary": {
                "kind": "dict",
                "redacted": True,
                "secret_presence_only": True,
                "secret_values_printed": False,
            },
        },
    )
    budget = calculate_rphi_budget(tmp_path)
    assert budget["raw_counts"]["secret_private_path_findings"] == 0
    assert budget["actiongate_suggestion"] == "REVIEW"


def test_clean_signals_produce_optimo_or_funcional(tmp_path: Path) -> None:
    _write_json(
        tmp_path / "tasks" / "task_board.json",
        {
            "schema_version": "claudio.task_board.v0.1",
            "tasks": [
                {
                    "id": "task-clean",
                    "title": "Clean local close",
                    "status": "completed",
                    "evidence": ["test passed"],
                    "handoff_created": True,
                }
            ],
        },
    )
    _append_jsonl(
        tmp_path / "memory" / "memory_lite.jsonl",
        {
            "schema_version": "claudio.memory_lite.v0.1",
            "type": "claim",
            "summary": "Evidence-backed local claim.",
            "source": "TEST_REPORT.md",
            "confidence": 0.95,
        },
    )
    _append_jsonl(
        tmp_path / "witness" / "witness_log.jsonl",
        {
            "schema_version": "claudio.witness_log.v0.1",
            "event_id": "evt-clean",
            "command": "budget status",
            "status": "ok",
            "actiongate": "APPROVE",
            "result_summary": {"kind": "dict", "redacted": True, "evidence": "present"},
        },
    )
    budget = calculate_rphi_budget(tmp_path)
    assert budget["regime"] in {"OPTIMO", "FUNCIONAL"}
    assert budget["actiongate_suggestion"] == "APPROVE"


def test_phi_eff_decreases_when_review_block_failure_cost_rises(tmp_path: Path) -> None:
    clean_state = tmp_path / "clean"
    noisy_state = tmp_path / "noisy"
    _write_json(
        clean_state / "tasks" / "task_board.json",
        {"schema_version": "claudio.task_board.v0.1", "tasks": [{"id": "done", "status": "completed", "evidence": ["ok"]}]},
    )
    _write_json(
        noisy_state / "tasks" / "task_board.json",
        {"schema_version": "claudio.task_board.v0.1", "tasks": [{"id": "done", "status": "completed", "evidence": ["ok"]}]},
    )
    for index, gate in enumerate(["REVIEW", "BLOCK", "REVIEW", "BLOCK"]):
        _append_jsonl(
            noisy_state / "witness" / "witness_log.jsonl",
            {
                "schema_version": "claudio.witness_log.v0.1",
                "event_id": f"evt-noisy-{index}",
                "command": "permissions check",
                "status": "failed" if gate == "BLOCK" else "ok",
                "actiongate": gate,
                "result_summary": {"kind": "dict", "redacted": True},
            },
        )
    assert calculate_rphi_budget(noisy_state)["phi_eff"] < calculate_rphi_budget(clean_state)["phi_eff"]


def test_regime_boundaries_are_correct() -> None:
    assert classify_regime(0.1499) == "OPTIMO"
    assert classify_regime(0.15) == "FUNCIONAL"
    assert classify_regime(0.3999) == "FUNCIONAL"
    assert classify_regime(0.40) == "CARGADO"
    assert classify_regime(0.6999) == "CARGADO"
    assert classify_regime(0.70) == "SATURADO"
    assert classify_regime(0.8999) == "SATURADO"
    assert classify_regime(0.90) == "JAMMING"


def test_json_output_schema_is_stable(tmp_path: Path) -> None:
    result = write_rphi_artifacts(tmp_path, output_root=tmp_path / "qa_artifacts")
    budget = result["budget"]
    assert set(budget) == {
        "schema_version",
        "generated_at",
        "r_total",
        "phi_eff",
        "regime",
        "actiongate_suggestion",
        "components",
        "raw_counts",
        "recommendations",
        "source_files_used",
    }
    assert Path(result["json_path"]).exists()
    assert Path(result["markdown_report_path"]).exists()
