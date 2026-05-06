from pathlib import Path
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from l1_comms_diff_consumer import consume_inbox, is_within_path, validate_diff_plan
from l1_programmer_workpack import append_comms_message, build_comms_message, build_workpack_from_l1


EXAMPLES = ROOT / "examples"
SCRIPT = ROOT / "l1_comms_diff_consumer.py"


def read_example(name: str) -> str:
    return (EXAMPLES / name).read_text(encoding="utf-8")


def write_message(tmp_path: Path, example: str, *, repo_root: Path) -> Path:
    inbox = tmp_path / "COMMS" / "inbox" / "claudio-local-agent.jsonl"
    workpack = build_workpack_from_l1(read_example(example), source_path=example)
    message = build_comms_message(workpack)
    append_comms_message(inbox, message)
    return inbox


def test_consumer_builds_diff_plan_ready_without_applying(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "example.md").write_text("old\n", encoding="utf-8")
    inbox = write_message(tmp_path, "gated_patch.obs", repo_root=repo)

    result = consume_inbox(inbox, repo_root=repo)
    plan = result["plans"][0]

    assert result["plan_count"] == 1
    assert plan["status"] == "DIFF_PLAN_READY"
    assert plan["proposal_count"] == 1
    assert plan["application_gate"]["status"] == "REVIEW"
    assert plan["dry_run"] is True
    assert plan["applied"] is False
    assert plan["may_apply_patch"] is False
    assert (repo / "docs" / "example.md").read_text(encoding="utf-8") == "old\n"


def test_consumer_blocks_external_action_message(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    inbox = write_message(tmp_path, "blocked_external_action.obs", repo_root=repo)

    result = consume_inbox(inbox, repo_root=repo)
    plan = result["plans"][0]

    assert plan["status"] == "BLOCKED_BY_ACTION_GATE"
    assert "blocked_by_action_gate" in plan["blockers"]
    assert plan["proposal_count"] == 0
    assert plan["may_apply_patch"] is False


def test_consumer_reviews_missing_target(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    inbox = write_message(tmp_path, "gated_patch.obs", repo_root=repo)

    result = consume_inbox(inbox, repo_root=repo)
    plan = result["plans"][0]

    assert plan["status"] == "REVIEW_NOT_DIFFABLE"
    assert "target_missing" in plan["blockers"]
    assert plan["proposal_count"] == 0


def test_consumer_reviews_directory_target_instead_of_ready_plan(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs" / "example.md").mkdir(parents=True)
    inbox = write_message(tmp_path, "gated_patch.obs", repo_root=repo)

    result = consume_inbox(inbox, repo_root=repo)
    plan = result["plans"][0]

    assert plan["status"] == "REVIEW_NOT_DIFFABLE"
    assert "target_not_file" in plan["blockers"]
    assert plan["proposal_count"] == 0
    assert plan["validation"]["ok"] is True


def test_path_boundary_rejects_prefix_sibling(tmp_path):
    repo = tmp_path / "repo"
    sibling = tmp_path / "repo_evil" / "docs" / "example.md"
    repo.mkdir()
    sibling.parent.mkdir(parents=True)
    sibling.write_text("outside\n", encoding="utf-8")

    assert is_within_path(repo, sibling) is False


def test_consumer_returns_empty_result_for_no_messages(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    inbox = tmp_path / "COMMS" / "inbox" / "claudio-local-agent.jsonl"
    inbox.parent.mkdir(parents=True)
    inbox.write_text("", encoding="utf-8")

    result = consume_inbox(inbox, repo_root=repo)

    assert result["message_count"] == 0
    assert result["plan_count"] == 0
    assert result["applied"] is False


def test_diff_plan_validator_rejects_apply_permission(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "example.md").write_text("old\n", encoding="utf-8")
    inbox = write_message(tmp_path, "gated_patch.obs", repo_root=repo)
    plan = consume_inbox(inbox, repo_root=repo)["plans"][0]
    plan["may_apply_patch"] = True

    validation = validate_diff_plan(plan)

    assert validation["ok"] is False
    assert "may_apply_patch must be false" in validation["errors"]


def test_cli_writes_diff_consumer_result(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "example.md").write_text("old\n", encoding="utf-8")
    inbox = write_message(tmp_path, "gated_patch.obs", repo_root=repo)
    out = tmp_path / "diff_consumer.json"

    subprocess.run(
        [sys.executable, str(SCRIPT), str(inbox), "--repo-root", str(repo), "--out", str(out), "--pretty"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))

    assert payload["schema"] == "observacionismo.l1_comms_diff_consumer_result.v0_1"
    assert payload["plans"][0]["status"] == "DIFF_PLAN_READY"
    assert payload["plans"][0]["applied"] is False


def test_diff_plan_schema_contract_file_is_present():
    schema = json.loads((ROOT / "schemas" / "l1_comms_diff_plan.schema.json").read_text(encoding="utf-8"))

    assert schema["properties"]["schema"]["const"] == "observacionismo.l1_comms_diff_plan.v0_1"
    assert schema["properties"]["application_gate"]["properties"]["status"]["const"] == "REVIEW"
    assert schema["properties"]["may_apply_patch"]["const"] is False
