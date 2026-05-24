from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX_JSON = (
    ROOT
    / "docs"
    / "intake"
    / "BRAIN_OS_POST_UNIFIED_FRAMEWORK_MATRIX_2026-05-18.json"
)
MATRIX_MD = (
    ROOT
    / "docs"
    / "intake"
    / "BRAIN_OS_POST_UNIFIED_FRAMEWORK_MATRIX_2026-05-18.md"
)

PORTFOLIO_PATH = (
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST"
    r"\# 00 — LEER PRIMERO Portafolio MEDI.txt"
)
UNTITLED_PATH = (
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Untitled.txt"
)
EXPECTED_HASHES = {
    PORTFOLIO_PATH: "C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD",
    UNTITLED_PATH: "F5C992E17FAE57AB6B3F43488F0017BC635C0FE84A97EF1BBD34B5A90B84DF4B",
}


def load_matrix() -> dict:
    return json.loads(MATRIX_JSON.read_text(encoding="utf-8"))


def test_matrix_records_both_exact_post_sources_and_hashes() -> None:
    matrix = load_matrix()
    sources = {source["path"]: source["sha256"] for source in matrix["sources"]}

    assert sources == EXPECTED_HASHES
    assert {source["intake_action"] for source in matrix["sources"]} == {
        "SELECTIVE_CLAIM_EXTRACTION_ONLY",
        "CODE_INSIGHT_ONLY",
    }


def test_every_delta_has_provenance_target_boundary_evidence_and_gate() -> None:
    matrix = load_matrix()
    required = {
        "target_lane",
        "claim_boundary",
        "evidence_state",
        "action_gate",
        "source_path",
        "source_sha256",
        "line_evidence",
    }
    allowed_statuses = {
        "OVERLAP_REINFORCES_EXISTING",
        "REQUIRES_EVIDENCE",
        "FALSIFIER_OR_DEFECT",
    }

    assert matrix["deltas"]
    for delta in matrix["deltas"]:
        missing = [field for field in required if not delta.get(field)]
        assert missing == [], f"{delta['id']} missing {missing}"
        assert delta["source_path"] in EXPECTED_HASHES
        assert delta["source_sha256"] == EXPECTED_HASHES[delta["source_path"]]
        assert delta["integration_status"] in allowed_statuses
        assert all(isinstance(item, str) and item for item in delta["line_evidence"])


def test_runtime_publication_and_raw_adoption_stay_blocked() -> None:
    matrix = load_matrix()
    gates = matrix["gate_summary"]

    assert gates["RuntimeImport"] == "BLOCK"
    assert gates["PublicationGate"] == "BLOCK"
    assert gates["RawAdoption"] == "BLOCK"

    md_text = MATRIX_MD.read_text(encoding="utf-8")
    serialized = json.dumps(matrix, ensure_ascii=False)
    combined = md_text + "\n" + serialized

    assert "RuntimeImport=APPROVE" not in combined
    assert "PublicationGate=APPROVE" not in combined
    assert "RawAdoption=APPROVE" not in combined


def test_self_reported_success_terms_are_not_elevated_without_evidence() -> None:
    matrix = load_matrix()
    guardrails = matrix["claim_guardrails"] + matrix["falsifiers"]
    required_terms = ["Benchmark 5/5 OK", "PASS", "PROBADO", "derivada no conjetura"]

    for term in required_terms:
        matches = [
            item
            for item in guardrails
            if term in item.get("term", "") or term in item.get("raw_claim", "")
        ]
        assert matches, f"missing guardrail for {term}"
        for item in matches:
            combined_status = " ".join(
                [
                    item["claim_boundary"],
                    item["evidence_state"],
                    item["action_gate"],
                ]
            )
            assert "REQUIRES_EVIDENCE" in combined_status
            assert item["action_gate"] != "APPROVE"


def test_falsifiers_keep_partial_benchmark_regime_failure_and_lyapunov_bug() -> None:
    matrix = load_matrix()
    falsifier_claims = {item["raw_claim"] for item in matrix["falsifiers"]}

    assert "SCORE: 5/6" in falsifier_claims
    assert "F1_regime_prediction" in falsifier_claims
    assert "lambda=0.0000 -> INESTABLE" in falsifier_claims
    assert all(item["integration_status"] == "FALSIFIER_OR_DEFECT" for item in matrix["deltas"] if item["layer"] == "Falsifiers")
