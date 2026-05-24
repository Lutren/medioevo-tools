from __future__ import annotations

import json

from duat_genesis import (
    DUAT_MODULES,
    PUBLIC_PROMPTS,
    PUBLIC_SOURCE_CARDS,
    ActionGateInput,
    SourceCard,
    action_gate_v2,
    event_to_jsonl,
    get_public_modules,
    get_public_prompt_keys,
    get_public_source_cards,
    legacy_transfer_checklist,
    make_witness_event,
    validate_handoff_text,
    validate_module_card,
    validate_source_card,
)


def test_module_registry_cards_validate() -> None:
    assert DUAT_MODULES
    assert all(validate_module_card(card) == [] for card in DUAT_MODULES)
    assert {module.id for module in get_public_modules()} >= {
        "project_analyzer",
        "image_reactor",
        "company_observatory",
    }


def test_action_gate_blocks_secrets_and_reviews_unmanifested_delete() -> None:
    blocked = action_gate_v2(
        ActionGateInput(
            evidence=1.0,
            risk=0.1,
            reversibility=1.0,
            authorization=1.0,
            phi_eff=0.9,
            r_delta_expected=-0.1,
            touches_secrets=True,
            external_publish=False,
            destructive=False,
        )
    )
    assert blocked.decision == "BLOCK"

    review = action_gate_v2(
        ActionGateInput(
            evidence=0.9,
            risk=0.3,
            reversibility=0.0,
            authorization=1.0,
            phi_eff=0.8,
            r_delta_expected=-0.2,
            touches_secrets=False,
            external_publish=False,
            destructive=False,
            permanent_delete=True,
            value_absorbed=False,
            manifest_created=True,
        )
    )
    assert review.decision == "REVIEW"


def test_action_gate_approves_documented_low_risk_local_action() -> None:
    result = action_gate_v2(
        ActionGateInput(
            evidence=0.9,
            risk=0.1,
            reversibility=0.9,
            authorization=0.9,
            phi_eff=0.8,
            r_delta_expected=-0.2,
            touches_secrets=False,
            external_publish=False,
            destructive=False,
        )
    )
    assert result.decision == "APPROVE"
    assert result.score >= 0.72


def test_handoff_validator_and_public_prompts_shape() -> None:
    handoff = """
ESTADO
CERTEZA
INFERENCIA
INCOGNITA
ACCION
Proxima accion: run focused QA.
ARTEFACTO
HANDOFF
Fingerprint: abc123
"""
    assert validate_handoff_text(handoff).ok
    assert set(get_public_prompt_keys()) == {"max_token_savings", "full_handoff"}
    assert PUBLIC_PROMPTS["full_handoff"]["boundary"] == "public"


def test_source_card_legacy_and_witness_shapes() -> None:
    card = SourceCard(
        id="demo",
        title="Demo source",
        source_type="doc",
        boundary="public",
        claims=("synthetic-only",),
        evidence=("tests/test_run8_modules.py",),
        next_action="Keep as public fixture.",
    )
    assert validate_source_card(card) == []
    assert legacy_transfer_checklist()

    event = make_witness_event(
        actor="pytest",
        event="test_run",
        path="tests/test_run8_modules.py",
        reason="shape verification",
        gate="APPROVE",
        risk="low",
        hash="abc123",
    )
    payload = json.loads(event_to_jsonl(event))
    assert payload["event"] == "test_run"
    assert payload["gate"] == "APPROVE"


def test_public_dataset_source_cards_are_catalog_only() -> None:
    cards = get_public_source_cards()
    assert cards == PUBLIC_SOURCE_CARDS
    assert all(validate_source_card(card) == [] for card in cards)
    by_id = {card.id: card for card in cards}
    awesomedata = by_id["awesomedata_public_datasets"]
    assert awesomedata.source_type == "catalog_index"
    assert awesomedata.boundary == "public"
    assert "discovery index only" in awesomedata.next_action
    assert by_id["fred_api"].boundary == "unknown_review"
