from __future__ import annotations

from obsai_core import CANONICAL_CLAIM_GATES, build_claim_gate_contract
from obsai_core.claim_classifier import ClaimClassifier


def _gate_status(contract: dict, name: str) -> str:
    for gate in contract["gates"]:
        if gate["name"] == name:
            return gate["status"]
    raise AssertionError(f"missing gate: {name}")


def test_claim_gate_contract_names_are_canonical() -> None:
    assert CANONICAL_CLAIM_GATES == (
        "TruthGate",
        "C-GATE",
        "PhysicsHonestyGate",
        "ScienceClaimGate",
    )


def test_claim_gate_contract_is_embedded_in_claim_result_dict() -> None:
    result = ClaimClassifier().classify_atom(
        "El observador no observa desde cero; observa desde estado."
    )
    payload = result.to_dict()

    assert payload["gate_contract"]["schemaVersion"] == "obsai.claim_gate_contract.v1"
    assert payload["gate_contract"]["final_decision"] == "APPROVE"
    assert [gate["name"] for gate in payload["gate_contract"]["gates"]] == list(CANONICAL_CLAIM_GATES)


def test_science_claim_gate_blocks_strong_external_claim() -> None:
    result = ClaimClassifier().classify_atom("Causal Rendering prueba una nueva fisica.")
    contract = build_claim_gate_contract(result)

    assert contract["final_decision"] == "BLOCK"
    assert _gate_status(contract, "TruthGate") == "BLOCK"
    assert _gate_status(contract, "PhysicsHonestyGate") == "BLOCK"
    assert _gate_status(contract, "ScienceClaimGate") == "BLOCK"


def test_c_gate_reviews_low_clarity_claim() -> None:
    result = ClaimClassifier().classify_atom("Esto.")
    contract = build_claim_gate_contract(result)

    assert _gate_status(contract, "C-GATE") == "REVIEW"
    assert contract["final_decision"] in {"REVIEW", "BLOCK"}
