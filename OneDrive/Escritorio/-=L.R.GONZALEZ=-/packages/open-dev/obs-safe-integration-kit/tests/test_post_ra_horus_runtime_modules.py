from obs_safe_integration_kit import (
    AgencyLevel,
    EstadoPSI,
    GateStatus,
    GenerationProposal,
    KnowledgeGraph,
    KnowledgeNode,
    NodeState,
    can_generate,
    classify_agency,
    classify_r_trend,
    compute_r_velocity,
    compute_temperature,
    evaluate_generation,
)


def test_agency_blocks_autonomous_generation_for_reality_checked_work():
    level = classify_agency(phi_eff=0.80, r=0.10, evidence_count=0, requires_reality_check=True)

    assert level == AgencyLevel.OBSERVER
    assert can_generate(level, task_risk="high") is False


def test_agency_allows_deliberative_only_with_evidence_control_and_low_r():
    level = classify_agency(phi_eff=0.80, r=0.10, evidence_count=2, requires_reality_check=True)

    assert level == AgencyLevel.DELIBERATIVE
    assert can_generate(level, task_risk="high") is True


def test_generation_gate_blocks_factual_code_or_plan_without_deliberative_evidence():
    psi = EstadoPSI(topic="post-ra-horus", R=0.10, Phi_eff=0.80)
    decision = evaluate_generation(
        GenerationProposal(content_type="factual", requires_sources=True, confidence_claimed=0.95),
        psi,
        evidence_count=0,
    )

    assert decision.status == GateStatus.BLOCK
    assert decision.agency_level == AgencyLevel.OBSERVER
    assert "sources_required_without_evidence" in decision.reasons


def test_generation_gate_passes_as_dry_run_when_deliberative_and_evidenced():
    psi = EstadoPSI(topic="post-ra-horus", R=0.10, Phi_eff=0.82)
    decision = evaluate_generation(
        GenerationProposal(content_type="code", requires_sources=False, confidence_claimed=0.55),
        psi,
        evidence_count=3,
    )

    assert decision.status == GateStatus.DRY_RUN
    assert decision.approved is True
    assert decision.agency_level == AgencyLevel.DELIBERATIVE


def test_knowledge_graph_does_not_return_locked_content_without_prerequisites():
    graph = KnowledgeGraph()
    graph.add_node(KnowledgeNode("math", "Math", "math content", unlock_phi_threshold=0.50))
    graph.add_node(KnowledgeNode("ghost", "GhostGate", "ghost content", prerequisites=["math"]))

    result = graph.attempt_access("ghost", phi_eff=0.90, r=0.10)

    assert result["status"] == NodeState.LOCKED.value
    assert result["content"] is None
    assert result["reason"] == "missing_prerequisites:math"


def test_knowledge_graph_unlocks_after_prerequisite_integration_and_phi_gate():
    graph = KnowledgeGraph()
    graph.add_node(KnowledgeNode("math", "Math", "math content", unlock_phi_threshold=0.50))
    graph.add_node(KnowledgeNode("ghost", "GhostGate", "ghost content", prerequisites=["math"]))

    math = graph.attempt_access("math", phi_eff=0.60, r=0.10)
    assert math["status"] == NodeState.ACCESSIBLE.value
    graph.integrate("math", ["local test evidence"])
    ghost = graph.attempt_access("ghost", phi_eff=0.70, r=0.10)

    assert ghost["status"] == NodeState.ACCESSIBLE.value
    assert ghost["content"] == "ghost content"
    assert graph.progress()["integrated"] == 1


def test_dynamic_temperature_decreases_with_r_and_caps_factual_tasks():
    low_r = compute_temperature(r=0.10, phi_eff=0.90, task_type="general")
    high_r = compute_temperature(r=0.45, phi_eff=0.90, task_type="general")
    factual = compute_temperature(r=0.10, phi_eff=0.90, task_type="factual")

    assert low_r.temperature > high_r.temperature
    assert factual.temperature < low_r.temperature
    assert high_r.profile.value in {"FOCUSED", "BALANCED", "CONSTRAINED"}


def test_r_velocity_distinguishes_stable_from_rising_residue():
    assert compute_r_velocity([0.30, 0.30, 0.30]) == 0.0
    assert compute_r_velocity([0.20, 0.30, 0.44]) > 0.0
    assert classify_r_trend([0.20, 0.30, 0.44]) == "RISING"
    assert classify_r_trend([0.30, 0.30, 0.30]) == "STABLE"

