from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.json"
MODULES_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_PROGRAMMING_LEARNING_MODULES_2026-05-18.json"
MODULES_MD = ROOT / "docs" / "intake" / "BRAIN_OS_POST_PROGRAMMING_LEARNING_MODULES_2026-05-18.md"


def load_matrix() -> dict:
    return json.loads(MATRIX_JSON.read_text(encoding="utf-8"))


def load_modules() -> dict:
    return json.loads(MODULES_JSON.read_text(encoding="utf-8"))


def test_learning_modules_cover_all_matrix_deltas() -> None:
    matrix = load_matrix()
    modules = load_modules()
    all_delta_ids = {delta["id"] for delta in matrix["deltas"]}
    covered_delta_ids = {
        delta_id
        for card in modules["module_cards"]
        for delta_id in card["source_delta_ids"]
    }

    assert modules["coverage"]["uncovered_delta_ids"] == []
    assert covered_delta_ids == all_delta_ids


def test_module_cards_are_programmable_but_do_not_import_runtime_or_train_models() -> None:
    modules = load_modules()
    gates = modules["gate_summary"]

    assert gates["RuntimeImport"] == "BLOCK"
    assert gates["PublicationGate"] == "BLOCK"
    assert gates["RawAdoption"] == "BLOCK"
    assert gates["ModelTraining"] == "BLOCK"
    assert modules["learning_boundary"]["ai_learning_mode"] == "symbolic_curriculum_and_test_first_programming"
    assert modules["learning_boundary"]["model_training"] == "BLOCK"
    assert modules["learning_boundary"]["zip_extraction"] == "BLOCK"

    for card in modules["module_cards"]:
        assert card["status"] == "PROGRAMMING_LEARNING_SPEC"
        assert card["training_data_status"] == "CURATED_METADATA_AND_REQUIREMENTS_ONLY"
        assert card["model_training"] == "BLOCK"
        assert card["runtime_import"] == "BLOCK"
        assert card["publication_gate"] == "BLOCK"
        assert card["raw_adoption"] == "BLOCK"
        assert "learning_objective" in card and card["learning_objective"]
        assert "programming_objective" in card and card["programming_objective"]
        assert card["input_contract"]
        assert card["output_contract"]
        assert card["required_tests"]


def test_source_refs_preserve_provenance_hashes_and_evidence_anchors() -> None:
    matrix = load_matrix()
    modules = load_modules()
    deltas = {delta["id"]: delta for delta in matrix["deltas"]}

    for card in modules["module_cards"]:
        for ref in card["source_refs"]:
            delta = deltas[ref["delta_id"]]
            assert ref["source_path"] == delta["source_path"]
            assert ref["source_sha256"] == delta["source_sha256"]
            assert ref["evidence"] == delta["line_or_member_evidence"]
            assert ref["claim_boundary"] == delta["claim_boundary"]


def test_strong_claim_and_secret_terms_are_never_approved_in_learning_packets() -> None:
    modules = load_modules()
    serialized = json.dumps(modules, ensure_ascii=False)

    assert "ModelTraining=APPROVE" not in MODULES_MD.read_text(encoding="utf-8")
    assert "RuntimeImport=APPROVE" not in serialized
    assert "PublicationGate=APPROVE" not in serialized
    assert "RawAdoption=APPROVE" not in serialized

    packets = modules["codex_task_packets"]
    assert packets
    for packet in packets:
        assert packet["application_gate"] == "REVIEW"
        blocked = " ".join(packet["blocked_now"])
        assert "RuntimeImport" in blocked
        assert "PublicationGate approval" in blocked
        assert "RawAdoption" in blocked
        assert "cloud/model training" in blocked
        assert "secret/token exposure" in blocked


def test_zip_learning_module_is_metadata_only_and_blocks_extraction() -> None:
    modules = load_modules()
    cards = {card["module_id"]: card for card in modules["module_cards"]}
    zip_card = cards["post_zip_evidence_adapter"]

    assert zip_card["module_gate"] in {"REVIEW", "BLOCK"}
    assert any("zip_path::member" in action for action in zip_card["allowed_actions"])
    assert "extracting ZIP members into workspace" in zip_card["blocked_actions"]
    assert "runtime import from ZIP" in zip_card["blocked_actions"]


def test_security_workbench_module_is_fixture_only_and_blocks_tool_execution() -> None:
    modules = load_modules()
    cards = {card["module_id"]: card for card in modules["module_cards"]}
    security_card = cards["post_security_workbench_contract"]

    assert security_card["family"] == "Security"
    assert security_card["module_gate"] in {"REVIEW", "BLOCK"}
    assert security_card["runtime_import"] == "BLOCK"
    assert security_card["publication_gate"] == "BLOCK"
    assert security_card["raw_adoption"] == "BLOCK"
    assert security_card["source_delta_ids"] == [
        "security.scope_registry_authorization_required",
        "security.action_gate_dual_use_tools",
        "security.tool_catalog_default_gates",
        "security.dry_run_adapter_contract",
        "security.output_sanitizer_redaction",
        "security.risk_mapper_business_remediation",
        "security.witnesslog_handoff_security",
        "falsifiers.security_offensive_execution_blocked",
    ]
    blocked = " ".join(security_card["blocked_actions"])
    assert "executing nmap nikto sqlmap metasploit john hashcat maltego or recon-ng" in blocked
    assert "external target scanning" in blocked
    assert "password cracking" in blocked
    assert "Wabi CLI integration before obs-safe contract stability" in blocked
