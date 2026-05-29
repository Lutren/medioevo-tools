import sqlite3

from wabi_sabi.core.bridge import (
    DEGRADED_MODEL_ID,
    BridgeExecutor,
    MockRuntimeAdapter,
    WitnessLog,
    phi_eff_for_residue,
    regime_for_residue,
)


def test_deterministic_status_uses_no_llm(tmp_path):
    bridge = BridgeExecutor(tmp_path / "witness.sqlite")

    result = bridge.execute(
        "status local y validar json",
        evidence_refs=["test_status"],
        source="test",
    )

    assert result.decision.gate == "APPROVE"
    assert result.decision.route == "deterministic"
    assert result.decision.model_id is None
    assert result.output["mode"] == "deterministic_no_llm"
    assert bridge.witness.verify_chain() == (True, "ok")


def test_external_model_mutation_is_blocked_and_runtime_not_called(tmp_path):
    runtime = MockRuntimeAdapter()
    bridge = BridgeExecutor(tmp_path / "witness.sqlite", runtime_adapter=runtime)

    result = bridge.execute(
        "crea alias Ollama y publica el modelo",
        evidence_refs=["test_block"],
        source="test",
    )

    assert result.decision.gate == "BLOCK"
    assert "external_or_model_mutation" in result.decision.blocked_actions
    assert runtime.calls == []
    assert result.output["mode"] == "blocked"


def test_coder_task_routes_to_qwen_coder_under_review(tmp_path):
    bridge = BridgeExecutor(tmp_path / "witness.sqlite")

    result = bridge.execute(
        "implementa un adapter python con tests",
        evidence_refs=["test_coder"],
        source="test",
    )

    assert result.decision.gate == "REVIEW"
    assert result.decision.route == "technical_coder"
    assert result.decision.runtime == "ollama_optional"
    assert result.decision.model_id == "qwen2.5-coder:3b"


def test_triage_task_routes_to_small_qwen(tmp_path):
    bridge = BridgeExecutor(tmp_path / "witness.sqlite")

    result = bridge.execute(
        "clasifica pendientes y genera resumen",
        evidence_refs=["test_triage"],
        source="test",
    )

    assert result.decision.gate == "APPROVE"
    assert result.decision.route == "triage"
    assert result.decision.model_id == "qwen2.5:0.5b"


def test_missing_evidence_adds_required_evidence(tmp_path):
    bridge = BridgeExecutor(tmp_path / "witness.sqlite")

    result = bridge.execute("clasifica pendientes", source="test")

    assert result.decision.required_evidence == ["source_hash_or_test_or_local_file_reference"]
    assert result.decision.r_estimate > 0.2


def test_low_residue_keeps_optimo_or_functional_regime(tmp_path):
    bridge = BridgeExecutor(tmp_path / "witness.sqlite")

    result = bridge.execute(
        "status local y validar json",
        evidence_refs=["test_status"],
        source="test",
    )

    assert result.decision.gate == "APPROVE"
    assert result.decision.regime in {"OPTIMO", "FUNCIONAL"}


def test_decision_regime_and_phi_eff_match_canonical_helpers(tmp_path):
    bridge = BridgeExecutor(tmp_path / "witness.sqlite")

    result = bridge.execute("clasifica pendientes", source="test")

    r = result.decision.r_estimate
    assert result.decision.regime == regime_for_residue(r)
    assert result.decision.phi_eff == phi_eff_for_residue(r)


def test_jamming_regime_forces_review_and_degrades_model(tmp_path):
    bridge = BridgeExecutor(tmp_path / "witness.sqlite")
    # Uncertain + coder language, no evidence, long text -> residue lands in the jamming band
    # WITHOUT any hard-boundary block word, so the regime (not a block word) must force REVIEW.
    filler = "detalle " * 130  # >800 chars
    result = bridge.execute(
        "quizas refactor el modulo python " + filler,
        source="test",
    )

    assert result.decision.regime in {"JAMMING_TEMPRANO", "JAMMING"}
    assert result.decision.r_estimate >= 0.45
    assert result.decision.gate == "REVIEW"
    assert result.decision.model_id == DEGRADED_MODEL_ID
    assert any(reason.startswith("regime_jamming") for reason in result.decision.reasons)


def test_witness_log_detects_payload_tampering(tmp_path):
    log_path = tmp_path / "witness.sqlite"
    witness = WitnessLog(log_path)
    witness.append("test", {"value": 1})
    assert witness.verify_chain() == (True, "ok")

    with sqlite3.connect(log_path) as conn:
        conn.execute("UPDATE witness_events SET payload_json = ? WHERE id = 1", ('{"value":2}',))
        conn.commit()

    ok, reason = witness.verify_chain()
    assert not ok
    assert reason == "event_hash_mismatch_at:1"
