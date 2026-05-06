from pathlib import Path
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from l1_programmer_workpack import build_workpack_from_l1, validate_programmer_workpack
from l1_programmer_workpack import append_comms_message, build_comms_message, validate_comms_message


EXAMPLES = ROOT / "examples"
SCRIPT = ROOT / "l1_programmer_workpack.py"


def read_example(name: str) -> str:
    return (EXAMPLES / name).read_text(encoding="utf-8")


def test_document_task_builds_read_only_workpack():
    workpack = build_workpack_from_l1(read_example("document_task.obs"), source_path="document_task.obs")

    assert workpack["status"] == "READY_READ_ONLY"
    assert workpack["patch_policy"]["may_prepare_patch_plan"] is False
    assert workpack["patch_policy"]["may_apply_patch"] is False
    assert workpack["validation"]["ok"] is True


def test_gated_patch_builds_patch_plan_only_workpack():
    workpack = build_workpack_from_l1(read_example("gated_patch.obs"), source_path="gated_patch.obs")

    assert workpack["status"] == "REVIEW_PATCH_PLAN_ONLY"
    assert workpack["proposed_scope"]["target_paths"] == ["docs/example.md"]
    assert workpack["patch_policy"]["may_prepare_patch_plan"] is True
    assert workpack["patch_policy"]["may_apply_patch"] is False
    assert workpack["patch_policy"]["requires_action_gate"] is True


def test_external_action_builds_blocked_workpack():
    workpack = build_workpack_from_l1(read_example("blocked_external_action.obs"), source_path="blocked_external_action.obs")

    assert workpack["status"] == "BLOCKED_BY_ACTION_GATE"
    assert workpack["proposed_scope"]["external_boundary_touched"] is True
    assert workpack["patch_policy"]["may_prepare_patch_plan"] is False
    assert workpack["validation"]["ok"] is True


def test_missing_evidence_builds_review_workpack():
    workpack = build_workpack_from_l1(read_example("missing_evidence.obs"), source_path="missing_evidence.obs")

    assert workpack["status"] == "REVIEW_MISSING_EVIDENCE"
    assert "missing_evidence" in workpack["risk_flags"]
    assert workpack["validation"]["ok"] is True


def test_handoff_builds_review_workpack():
    workpack = build_workpack_from_l1(read_example("handoff.obs"), source_path="handoff.obs")

    assert workpack["status"] == "HANDOFF_REVIEW"
    assert workpack["handoff"]["target"] == "wabi-sabi-sentido-comun"
    assert workpack["patch_policy"]["may_apply_patch"] is False


def test_validator_rejects_tampered_apply_permission():
    workpack = build_workpack_from_l1(read_example("document_task.obs"), source_path="document_task.obs")
    workpack["patch_policy"]["may_apply_patch"] = True

    validation = validate_programmer_workpack(workpack)

    assert validation["ok"] is False
    assert "may_apply_patch must be false" in validation["errors"]


def test_cli_writes_workpack(tmp_path):
    out = tmp_path / "workpack.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(EXAMPLES / "gated_patch.obs"), "--out", str(out), "--pretty"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))

    assert result.stdout == ""
    assert payload["schema"] == "observacionismo.l1_programmer_workpack.v0_1"
    assert payload["status"] == "REVIEW_PATCH_PLAN_ONLY"
    assert payload["validation"]["ok"] is True


def test_workpack_schema_contract_file_is_present():
    schema = json.loads((ROOT / "schemas" / "l1_programmer_workpack.schema.json").read_text(encoding="utf-8"))

    assert schema["properties"]["schema"]["const"] == "observacionismo.l1_programmer_workpack.v0_1"
    assert schema["properties"]["programmer_agent"]["properties"]["may_execute"]["const"] is False
    assert schema["properties"]["patch_policy"]["properties"]["may_apply_patch"]["const"] is False
    assert schema["properties"]["patch_policy"]["properties"]["no_auto_write"]["const"] is True


def test_comms_message_embeds_workpack_without_execution(tmp_path):
    workpack = build_workpack_from_l1(read_example("gated_patch.obs"), source_path="gated_patch.obs")
    message = build_comms_message(workpack)
    inbox = tmp_path / "COMMS" / "inbox" / "claudio-local-agent.jsonl"

    append_result = append_comms_message(inbox, message)
    validation = validate_comms_message(message)
    rows = [json.loads(line) for line in inbox.read_text(encoding="utf-8").splitlines() if line.strip()]

    assert validation["ok"] is True
    assert append_result["ok"] is True
    assert rows[0]["message_type"] == "L1_PROGRAMMER_WORKPACK_READY"
    assert rows[0]["observation_envelope"]["envelope_version"] == "seto-observation-v1"
    assert rows[0]["workpack"]["patch_policy"]["may_apply_patch"] is False
    assert rows[0]["routing"]["does_not_execute"] is True


def test_comms_message_passes_canonical_claudio_agent_comms_validator():
    claudio_root = ROOT.parents[1] / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio"
    assert (claudio_root / "core" / "agent_comms.py").exists()
    sys.path.insert(0, str(claudio_root))
    from core import agent_comms

    workpack = build_workpack_from_l1(read_example("gated_patch.obs"), source_path="gated_patch.obs")
    message = build_comms_message(workpack)

    assert agent_comms.validate_message(message, "l1-workpack") == []


def test_comms_validator_rejects_embedded_apply_permission():
    workpack = build_workpack_from_l1(read_example("gated_patch.obs"), source_path="gated_patch.obs")
    message = build_comms_message(workpack)
    message["workpack"]["patch_policy"]["may_apply_patch"] = True

    validation = validate_comms_message(message)

    assert validation["ok"] is False
    assert "embedded workpack may_apply_patch must be false" in validation["errors"]


def test_cli_appends_comms_message_only_when_requested(tmp_path):
    out = tmp_path / "workpack.json"
    inbox = tmp_path / "COMMS" / "inbox" / "claudio-local-agent.jsonl"
    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(EXAMPLES / "gated_patch.obs"),
            "--out",
            str(out),
            "--comms-inbox",
            str(inbox),
            "--pretty",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    row = json.loads(inbox.read_text(encoding="utf-8").splitlines()[0])

    assert payload["comms_append"]["ok"] is True
    assert row["recipient"] == "claudio-local-agent"
    assert row["routing"]["append_only"] is True
