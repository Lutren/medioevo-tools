from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from claudio_agent_runtime.brief import render_brief
from claudio_agent_runtime.doctor import run_doctor
from claudio_agent_runtime.executor import execute_write_file, restore_rollback
from claudio_agent_runtime.ghostgate import evaluate_plan_request, plan_tools
from claudio_agent_runtime.jsonutil import read_json
from claudio_agent_runtime.memory_lite import memory_status, search_memory
from claudio_agent_runtime.permissions import evaluate_permission
from claudio_agent_runtime.skills_registry import discover_skills, inspect_skill
from claudio_agent_runtime.task_board import add_task, list_tasks
from claudio_agent_runtime.witness_log import append_witness_event, load_witness_events, witness_status


FIXTURES = ROOT / "fixtures"
STATE = FIXTURES / "state"


def test_permission_decisions_cover_approve_review_block() -> None:
    cases = {
        "permission_local_write.json": "APPROVE",
        "permission_external_publish.json": "REVIEW",
        "permission_sensitive_path.json": "BLOCK",
    }
    for filename, expected in cases.items():
        result = evaluate_permission(read_json(FIXTURES / filename))
        assert result["decision"] == expected


def test_ghostgate_plan_tools_are_read_only() -> None:
    tools = plan_tools()
    assert "read_file" in tools["allowed_tools"]
    assert "write_file" in tools["blocked_tools"]
    assert "run_command" in tools["blocked_tools"]
    assert tools["contract"] == "read_list_search_inspect_only"


def test_ghostgate_plan_request_blocks_write_shell_git_push() -> None:
    allowed = evaluate_plan_request(read_json(FIXTURES / "ghostgate_plan_allowed.json"))
    blocked = evaluate_plan_request(read_json(FIXTURES / "ghostgate_plan_blocked.json"))
    assert allowed["decision"] == "APPROVE"
    assert blocked["decision"] == "BLOCK"
    assert blocked["blocked"] == ["git_push", "run_command", "write_file"]


def test_execute_write_file_requires_actiongate_and_creates_rollback(tmp_path: Path) -> None:
    payload = read_json(FIXTURES / "execute_write_approved.json")
    result = execute_write_file(tmp_path, payload)
    assert result["status"] == "executed"
    target = tmp_path / "runtime" / "outputs" / "example.txt"
    assert target.read_text(encoding="utf-8") == "hello from claudio-agent-runtime\n"
    restored = restore_rollback(tmp_path, result["rollback_id"])
    assert restored["status"] == "restored"
    assert not target.exists()


def test_execute_write_file_does_not_execute_review_actions(tmp_path: Path) -> None:
    result = execute_write_file(tmp_path, read_json(FIXTURES / "execute_write_review.json"))
    assert result["status"] == "not_executed"
    assert result["actiongate"] == "REVIEW"
    assert not (tmp_path / "github:Lutren" / "example").exists()


def test_skills_list_progressive_disclosure_metadata_only() -> None:
    skills = discover_skills(FIXTURES / "skills")
    assert {skill["name"] for skill in skills} == {"curator", "release-guard"}
    assert all(skill["loaded"] is False for skill in skills)
    assert all("body" not in skill for skill in skills)


def test_skill_inspect_loads_body_on_demand() -> None:
    inspected = inspect_skill(FIXTURES / "skills" / "release-guard" / "SKILL.md")
    assert inspected["name"] == "release-guard"
    assert inspected["loaded"] is True
    assert "Release Guard" in inspected["body"]


def test_memory_status_counts_without_dumping_entries() -> None:
    status = memory_status(STATE)
    assert status["count"] == 2
    assert status["by_type"] == {"constraint": 1, "decision": 1}
    assert status["entries_redacted"] is True


def test_memory_search_returns_summaries_only() -> None:
    results = search_memory(STATE, "mercury")
    assert len(results) == 1
    assert results[0]["summary"] == "Mercury is reference only, not a runtime dependency."
    assert "boundary_tags" not in results[0]


def test_task_board_list_and_add(tmp_path: Path) -> None:
    state = tmp_path / "state"
    result = add_task(state, {"title": "Write tests", "priority": "P0"})
    assert result["count"] == 1
    listed = list_tasks(state)
    assert listed["tasks"][0]["title"] == "Write tests"
    assert listed["tasks"][0]["evidence_count"] == 0


def test_doctor_reports_secret_presence_only() -> None:
    doctor = run_doctor(STATE)
    assert doctor["secrets"]["presence_only"] is True
    assert doctor["secrets"]["values_printed"] is False
    assert "OPENAI_API_KEY" in doctor["secrets"]["env"]
    assert doctor["witness_log"]["entries_redacted"] is True


def test_brief_renders_next_action() -> None:
    brief = render_brief(STATE)
    assert "NEXT_SESSION_BRIEF CLAUDIO_AGENT_RUNTIME" in brief
    assert "Proxima accion verificable" in brief


def test_cli_json_smoke() -> None:
    from claudio_agent_runtime.cli import main

    assert main(["doctor", "--root", str(STATE), "--json"]) == 0


def test_witness_log_appends_redacted_events(tmp_path: Path) -> None:
    result = {"decision": "REVIEW", "reason": "publication requires review", "sensitive": "redacted"}
    event = append_witness_event(tmp_path, command="permissions check", status="ok", result=result, actiongate="REVIEW")
    assert event["event_id"].startswith("evt-")
    events = load_witness_events(tmp_path)
    assert len(events) == 1
    assert events[0]["actiongate"] == "REVIEW"
    assert events[0]["result_summary"]["decision"] == "REVIEW"
    assert "sensitive" not in events[0]["result_summary"]
    assert events[0]["result_summary"]["redacted"] is True


def test_cli_can_emit_witness_event_for_p0_commands(tmp_path: Path) -> None:
    from claudio_agent_runtime.cli import main

    assert main(["doctor", "--root", str(STATE), "--witness-root", str(tmp_path), "--json"]) == 0
    assert main(
        [
            "permissions",
            "check",
            str(FIXTURES / "permission_external_publish.json"),
            "--witness-root",
            str(tmp_path),
            "--json",
        ]
    ) == 0
    assert main(
        [
            "ghostgate",
            "check",
            str(FIXTURES / "ghostgate_plan_blocked.json"),
            "--witness-root",
            str(tmp_path),
            "--json",
        ]
    ) == 0
    status = witness_status(tmp_path)
    assert status["count"] == 3
    assert status["entries_redacted"] is True
