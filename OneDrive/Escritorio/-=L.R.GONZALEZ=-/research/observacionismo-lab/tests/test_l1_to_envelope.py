from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from l1_to_envelope import compile_l1_to_observation_packet, observation_envelope_to_action_gate


EXAMPLES = ROOT / "examples"


def read_example(name: str) -> str:
    return (EXAMPLES / name).read_text(encoding="utf-8")


def test_valid_program_compiles_to_observation_envelope():
    packet = compile_l1_to_observation_packet(read_example("document_task.obs"), source_path="document_task.obs")
    envelope = packet["observation_envelope"]

    assert packet["schema"] == "observacionismo.l1_observation_packet.v0_1"
    assert envelope["envelope_version"] == "seto-observation-v1"
    assert envelope["source_kind"] == "generated_artifact"
    assert envelope["psi_state"] == "CERTEZA"
    assert envelope["action_gate"] == "APPROVE"
    assert packet["action_gate"]["decision"] == "APPROVE"
    assert packet["contract"]["claim"].startswith("Documentar una tarea local")
    assert packet["contract"]["handoff"]["required"] is False
    assert packet["l1"]["assembly"][-1] == "HALT 0 0"


def test_missing_evidence_goes_to_review():
    packet = compile_l1_to_observation_packet(read_example("missing_evidence.obs"), source_path="missing_evidence.obs")

    assert "missing_evidence" in packet["observation_envelope"]["risk_flags"]
    assert packet["observation_envelope"]["action_gate"] == "REVIEW"
    assert packet["action_gate"]["decision"] == "REVIEW"
    assert "claim evidence artifact" in packet["action_gate"]["required_evidence"]


def test_gate_block_for_external_action():
    packet = compile_l1_to_observation_packet(read_example("blocked_external_action.obs"), source_path="blocked_external_action.obs")

    assert "blocked_external_action" in packet["observation_envelope"]["risk_flags"]
    assert packet["observation_envelope"]["action_gate"] == "BLOCK"
    assert packet["action_gate"]["decision"] == "BLOCK"
    assert packet["action_gate"]["no_external_action"] is True


def test_write_intent_patch_requires_review_not_write():
    packet = compile_l1_to_observation_packet(read_example("gated_patch.obs"), source_path="gated_patch.obs")

    assert "write_requires_action_gate" in packet["observation_envelope"]["risk_flags"]
    assert packet["observation_envelope"]["action_gate"] == "REVIEW"
    assert packet["action_gate"]["decision"] == "REVIEW"
    assert packet["contract"]["gate_required"] is True


def test_handoff_snapshot_requires_review_and_preserves_target():
    packet = compile_l1_to_observation_packet(read_example("handoff.obs"), source_path="handoff.obs")

    assert packet["contract"]["handoff"]["required"] is True
    assert packet["contract"]["handoff"]["target"] == "wabi-sabi-sentido-comun"
    assert packet["observation_envelope"]["action_gate"] == "REVIEW"
    assert packet["action_gate"]["decision"] == "REVIEW"


def test_observation_envelope_to_action_gate_blocks_tampered_external_risk():
    packet = compile_l1_to_observation_packet(read_example("document_task.obs"), source_path="document_task.obs")
    envelope = dict(packet["observation_envelope"])
    envelope["risk_flags"] = ["blocked_external_action"]
    envelope["action_gate"] = "APPROVE"

    gate = observation_envelope_to_action_gate(envelope)

    assert gate["decision"] == "BLOCK"
    assert "target-specific external ActionGate" in gate["required_evidence"]
