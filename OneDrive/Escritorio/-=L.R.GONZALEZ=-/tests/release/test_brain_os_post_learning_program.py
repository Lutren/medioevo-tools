from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS_RELEASE = ROOT / "tools" / "release"
sys.path.insert(0, str(TOOLS_RELEASE))

from brain_os_post_learning_program import (  # noqa: E402
    compile_learning_program,
    evaluate_action,
    evaluate_claim_text,
)


MATRIX_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.json"
WORKPACK_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_PROGRAMMING_LEARNING_MODULES_2026-05-18.json"
PROGRAM_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_COMPILED_LEARNING_PROGRAM_2026-05-18.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_program() -> dict:
    return compile_learning_program(load_json(MATRIX_JSON), load_json(WORKPACK_JSON))


def test_compiled_program_covers_all_post_modules_and_deltas() -> None:
    program = build_program()
    workpack = load_json(WORKPACK_JSON)

    assert program["schema_version"] == "brain_os.post_compiled_learning_program.v1"
    assert program["coverage"]["module_count"] == 7
    assert len(program["compiled_modules"]) == len(workpack["module_cards"])
    assert program["coverage"]["uncovered_delta_ids"] == []
    assert program["coverage"]["modules_with_missing_delta_ids"] == []


def test_compiled_program_keeps_all_global_gates_blocked() -> None:
    program = build_program()
    gates = program["gate_summary"]

    assert gates["RuntimeImport"] == "BLOCK"
    assert gates["PublicationGate"] == "BLOCK"
    assert gates["RawAdoption"] == "BLOCK"
    assert gates["ModelTraining"] == "BLOCK"
    assert gates["CloudTraining"] == "BLOCK"
    assert gates["ZipExtraction"] == "BLOCK"
    assert program["learning_boundary"]["training_data_status"] == "CURATED_METADATA_REQUIREMENTS_AND_FIXTURES_ONLY"

    serialized = json.dumps(program, ensure_ascii=False)
    assert "RuntimeImport=APPROVE" not in serialized
    assert "PublicationGate=APPROVE" not in serialized
    assert "RawAdoption=APPROVE" not in serialized
    assert "ModelTraining=APPROVE" not in serialized


def test_compiled_modules_preserve_provenance_hashes_and_required_contracts() -> None:
    program = build_program()
    workpack = load_json(WORKPACK_JSON)
    cards = {card["module_id"]: card for card in workpack["module_cards"]}

    for module in program["compiled_modules"]:
        card = cards[module["module_id"]]
        assert module["status"] == "COMPILED_LOCAL_PROGRAMMING_CONTRACT"
        assert module["source_refs_valid"] is True
        assert module["missing_delta_ids"] == []
        assert module["source_refs"] == card["source_refs"]
        assert "compiled module has no missing source deltas" in module["required_tests"]
        assert "blocked actions stay BLOCK" in module["required_tests"]
        assert "tools/release" in module["allowed_write_scope"]
        assert "tests/release" in module["allowed_write_scope"]


def test_gate_simulation_blocks_runtime_publication_training_zip_and_secret_actions() -> None:
    blocked_cases = [
        ("runtime import POST source", ["RuntimeImport"]),
        ("publish POST workpack", ["PublicationGate"]),
        ("raw adoption of POST code", ["RawAdoption"]),
        ("train model from POST corpus", ["ModelTraining"]),
        ("cloud training provider change", ["CloudTraining"]),
        ("extract ZIP members into workspace", ["ZipExtraction"]),
        ("read secret token from source", []),
    ]

    for text, tags in blocked_cases:
        decision = evaluate_action(text, action_tags=tags)
        assert decision["decision"] == "BLOCK"
        assert decision["blocked_by"]

    local_decision = evaluate_action("write local docs from curated metadata")
    assert local_decision["decision"] == "APPROVE_LOCAL_DOCS_ONLY"

    for text in ["nmap dry-run plan", "nikto fixture parse", "sqlmap lab validator", "hashcat synthetic audit"]:
        decision = evaluate_action(text)
        assert decision["decision"] == "REVIEW"


def test_claim_evaluator_never_approves_strong_success_science_or_secret_terms() -> None:
    blocked_claims = [
        "AGI as fact",
        "consciencia proven as physics",
        "medicina recommendation",
        "secret token available",
        "alineación cósmica as fact",
        "AI generated image as evidence",
        "raw code import from dream modules",
    ]
    requires_evidence_claims = [
        "Benchmark PASS",
        "PROBADO without current output",
        "derivada no conjetura",
        "fisica claim",
        "Jung archetype claim",
        "neurobiología dream claim",
        "hipnagogia prefrontal analogy",
    ]

    for claim in blocked_claims:
        decision = evaluate_claim_text(claim)
        assert decision["decision"] == "BLOCK"

    for claim in requires_evidence_claims:
        decision = evaluate_claim_text(claim)
        assert decision["decision"] == "REQUIRES_EVIDENCE"


def test_zip_evidence_is_metadata_only_and_blocks_extraction() -> None:
    program = build_program()
    zip_evidence = program["zip_evidence"]

    assert len(zip_evidence) == 4
    for item in zip_evidence:
        assert item["testzip"] is None
        assert item["entry_count"] == len(item["member_anchors"])
        assert all("::" in anchor for anchor in item["member_anchors"])
        assert item["suspicious_name_entries"] == []
        assert item["extraction_gate"] == "BLOCK"
        assert item["runtime_import_gate"] == "BLOCK"
        assert item["content_policy"] == "METADATA_AND_MEMBER_NAMES_ONLY"
        assert "member_contents" not in item
        assert "extracted_path" not in item


def test_generated_program_json_matches_compiler_contract_after_builder_runs() -> None:
    generated = load_json(PROGRAM_JSON)
    compiled = build_program()

    assert generated["schema_version"] == compiled["schema_version"]
    assert generated["coverage"] == compiled["coverage"]
    assert generated["gate_summary"] == compiled["gate_summary"]
    assert generated["compiled_modules"] == compiled["compiled_modules"]
