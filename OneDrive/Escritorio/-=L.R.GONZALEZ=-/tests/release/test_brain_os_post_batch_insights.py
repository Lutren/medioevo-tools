from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.json"
MATRIX_MD = ROOT / "docs" / "intake" / "BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.md"

EXPECTED_EXISTING_HASHES = {
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# 00 — LEER PRIMERO Portafolio MEDI.txt": "C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# OSIT Epistemic Engine A Formal Fr.txt": "94BE9A64DF6AD002F0F6B7DB4B2C2FA052314C31AABE2FE5E55ADFCFD40348D2",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\El Ojo de Ra y el Ojo de Horus (a m.txt": "F397D144BEA1471761838E7B9D7F209ED31CEC1F3D805B30548D6E0AF0BA6C30",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\deep-research-report.md": "26B51C23C6B2CA503CFE62B947835D0AFA88A05E0F059F6817E7A7B76FD44A18",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Del Cálculo al Gate_ Cómo OSIT Transforma la Planificación en la Nube en Acciones Locales Seguras y Auditables.pdf": "F294EF4A73202F8BE5B2C58FBD38053F299423DFDE03654F8FBAEAF2F2143578",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\El Noúmeno Informacional Unificació.txt": "F9D5B122A9B82C568C9CAEBBBFC0869DD5165CF7B4D2684C6C222FF030AEFCAD",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\ESTADO ANÁLISIS_ARQUITECTÓNICO  REV.txt": "F3805545DB1163971149DC25892467D5F958955A2494740ECCA6D2A70B35180D",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\ESTADO.txt": "9B9EC7C6723FB037CA0370B40E31EBD5FD4A79D830DE80B947CA576268AD2D60",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\ESTADO222222222.txt": "2E118556099DEAE74E07A8CCDC2B6F7D97C9BBBF5828EB2C41BDF244EC1137FE",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\ESTADOqqqqq.txt": "4744D5E3947591D8B5D7D53A9B284D4B0EFC13ECE0B3239C07F40FE53982E473",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Ingeniería Observacionista Inversa_ Un Modelo Operativo para Elevar la Eficiencia de la Investigación desde un Estado Óptimo.md": "5BE0BF57AB98AE8AC8F21C53DCDB0864DA943BFDF703B928B337008319BEE5BB",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\MEDIOEVO_OSIT_DOCUMENTOS_ACTUALIZADOS_TRUTHGATE_EIC_v0_3_2026-05-17.zip": "1FFC289E526E2BA81987B074DF1BDE6805C3E4A3C551E9BB7816BF29699FBE0C",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\MEDIOEVO_OSIT_DOCUMENTOS_FORMALIZADOS_v2_1_2026-05-17.zip": "44190A3DE0CC6EEB6E3DC7BA37D361DE50653965BCBDFD9B82BD050C9F698937",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\MEDIOEVO_OSIT_TEORIAS_COMUNICACION_CONSCIENCIA_v0_1_2026-05-17.zip": "6D1A0E1A686A44599BDB61C66DDC4E8B5212D56FE71ECBD79F8B514CAAFA438C",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\MEDIOEVO_OSIT_TRABAJO_MEJORADO_v0_2_2026-05-17.zip": "9871A6010E6E5BEF410C78314D6F60C790DC9E1BE591D6A86F93C7351EFA3523",
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Untitled.txt": "F5C992E17FAE57AB6B3F43488F0017BC635C0FE84A97EF1BBD34B5A90B84DF4B",
}

ZIP_PATHS = {
    path for path in EXPECTED_EXISTING_HASHES if path.endswith(".zip")
}


def load_matrix() -> dict:
    return json.loads(MATRIX_JSON.read_text(encoding="utf-8"))


def test_matrix_records_all_exact_existing_paths_and_hashes() -> None:
    matrix = load_matrix()
    sources = {source["path"]: source["sha256"] for source in matrix["sources"]}

    assert sources == EXPECTED_EXISTING_HASHES
    assert len(matrix["sources"]) == 16
    assert matrix["new_source_count"] == 14


def test_missing_alias_is_boundary_only_and_not_a_registered_source() -> None:
    matrix = load_matrix()
    aliases = matrix["not_found_aliases"]

    assert aliases == [
        {
            "path": r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# 00  LEER PRIMERO Portafolio MEDI.txt",
            "status": "NOT_FOUND_ALIAS_DO_NOT_REGISTER",
            "canonical_path": r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# 00 — LEER PRIMERO Portafolio MEDI.txt",
            "canonical_sha256": "C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD",
        }
    ]
    source_paths = {source["path"] for source in matrix["sources"]}
    assert aliases[0]["path"] not in source_paths


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


def test_every_delta_has_required_provenance_boundary_evidence_and_gate() -> None:
    matrix = load_matrix()
    sources = {source["path"]: source["sha256"] for source in matrix["sources"]}
    required = {
        "source_path",
        "source_sha256",
        "line_or_member_evidence",
        "target_lane",
        "claim_boundary",
        "evidence_state",
        "action_gate",
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
        assert delta["source_path"] in sources
        assert delta["source_sha256"] == sources[delta["source_path"]]
        assert delta["integration_status"] in allowed_statuses
        assert all(isinstance(item, str) and item for item in delta["line_or_member_evidence"])


def test_zip_containers_have_integrity_metadata_entries_and_no_suspicious_names() -> None:
    matrix = load_matrix()
    zip_inventory = {item["path"]: item for item in matrix["zip_inventory"]}

    assert set(zip_inventory) == ZIP_PATHS
    for path, item in zip_inventory.items():
        assert item["sha256"] == EXPECTED_EXISTING_HASHES[path]
        assert item["testzip"] is None
        assert item["entry_count"] == len(item["entries"])
        assert item["entry_count"] > 0
        assert item["suspicious_name_entries"] == []


def test_sensitive_success_and_strong_claim_terms_are_not_elevated() -> None:
    matrix = load_matrix()
    terms = {item["term"]: item for item in matrix["claim_guardrails"]}
    required_terms = {
        "PASS",
        "PROBADO",
        "Benchmark",
        "consciencia",
        "conciencia",
        "AGI",
        "medicina",
        "secret",
        "token",
        "arXiv",
        "quant-ph",
        "100%",
        "Shannon",
        "sueño",
        "Jung",
        "neurobiología",
        "AI generated",
        "cósmica",
        "nmap",
        "nikto",
        "maltego",
        "recon-ng",
        "metasploit",
        "sqlmap",
        "john",
        "hashcat",
        "payload",
        "shell",
        "dump",
        "bypass",
        "exfiltration",
        "cookie",
        "password",
    }

    assert required_terms <= set(terms)
    for term in required_terms:
        item = terms[term]
        combined_status = " ".join(
            [
                item["claim_boundary"],
                item["evidence_state"],
                item["action_gate"],
            ]
        )
        assert "REQUIRES_EVIDENCE" in combined_status or "BLOCK" in combined_status
        assert item["action_gate"] != "APPROVE"
        assert item["action_gate"] != "APPROVE_LOCAL_DOCS_ONLY"


def test_raw_runtime_code_in_zip_is_a_falsifier_not_an_import() -> None:
    matrix = load_matrix()
    falsifiers = {item["id"]: item for item in matrix["falsifiers"]}

    assert falsifiers["zip_runtime_code_member"]["claim_boundary"] == "RUNTIME_IMPORT_BLOCK"
    assert falsifiers["zip_runtime_code_member"]["action_gate"] == "REVIEW"
    assert "osit_epistemic_engine_v2_1.py" in falsifiers["zip_runtime_code_member"]["raw_claim"]


def test_formal_framework_source_is_insight_only_and_preprint_claims_are_not_approved() -> None:
    matrix = load_matrix()
    sources = {source["id"]: source for source in matrix["sources"]}
    source = sources["osit_epistemic_engine_formal_framework_post"]

    assert source["intake_action"] == "FORMAL_FRAMEWORK_INSIGHT_ONLY"
    assert source["runtime_import"] == "BLOCK"
    assert source["publication_gate"] == "BLOCK"
    assert source["raw_adoption"] == "BLOCK"
    assert source["ficha"].endswith("2026-05-18_batch_osit_epistemic_engine_formal_framework.md")

    deltas = {delta["id"]: delta for delta in matrix["deltas"]}
    for delta_id in {
        "math_state.formal_framework_shannon_bridge_requires_calibration",
        "gate.formal_framework_ghostgate_classical_simulation",
        "continuity.formal_framework_handoff_fingerprint_contract",
        "falsifiers.formal_framework_preprint_benchmark_claims_require_current_evidence",
    }:
        delta = deltas[delta_id]
        assert delta["source_path"] == source["path"]
        assert delta["source_sha256"] == source["sha256"]
        assert delta["action_gate"] != "APPROVE"

    falsifiers = {item["id"]: item for item in matrix["falsifiers"]}
    assert falsifiers["formal_framework_preprint_benchmark_claim"]["action_gate"] == "REVIEW"


def test_ra_horus_source_is_symbolic_agency_only_and_raw_code_claims_are_blocked() -> None:
    matrix = load_matrix()
    sources = {source["id"]: source for source in matrix["sources"]}
    source = sources["ra_horus_symbolic_agency_post"]

    assert source["intake_action"] == "SYMBOLIC_AGENCY_INSIGHT_ONLY"
    assert source["runtime_import"] == "BLOCK"
    assert source["publication_gate"] == "BLOCK"
    assert source["raw_adoption"] == "BLOCK"
    assert source["ficha"].endswith("2026-05-18_batch_ra_horus_symbolic_agency.md")

    deltas = {delta["id"]: delta for delta in matrix["deltas"]}
    for delta_id in {
        "gate.ra_horus_agency_state_machine_requires_runtime_tests",
        "gate.ra_horus_pre_action_generation_gate",
        "continuity.ra_horus_prerequisite_knowledge_graph",
        "math_state.ra_horus_dynamic_temperature_and_r_velocity",
        "falsifiers.ra_horus_dream_science_and_raw_code_claims_blocked",
    }:
        delta = deltas[delta_id]
        assert delta["source_path"] == source["path"]
        assert delta["source_sha256"] == source["sha256"]
        assert delta["action_gate"] != "APPROVE"

    falsifiers = {item["id"]: item for item in matrix["falsifiers"]}
    assert falsifiers["ra_horus_dream_modules_raw_code_claim"]["action_gate"] == "BLOCK"


def test_security_workbench_source_is_review_only_and_contributes_eight_deltas() -> None:
    matrix = load_matrix()
    sources = {source["id"]: source for source in matrix["sources"]}
    source = sources["estado_security_workbench_post"]

    assert source["classification"] == "POST_ETHICAL_SECURITY_WORKBENCH_SOURCE"
    assert source["intake_action"] == "DEFENSIVE_SECURITY_WORKBENCH_INSIGHT_ONLY"
    assert source["action_gate"] == "REVIEW"
    assert source["runtime_import"] == "BLOCK"
    assert source["publication_gate"] == "BLOCK"
    assert source["raw_adoption"] == "BLOCK"
    assert source["ficha"].endswith("2026-05-18_batch_estado_security_workbench.md")

    deltas = {delta["id"]: delta for delta in matrix["deltas"]}
    expected_delta_ids = {
        "security.scope_registry_authorization_required",
        "security.action_gate_dual_use_tools",
        "security.tool_catalog_default_gates",
        "security.dry_run_adapter_contract",
        "security.output_sanitizer_redaction",
        "security.risk_mapper_business_remediation",
        "security.witnesslog_handoff_security",
        "falsifiers.security_offensive_execution_blocked",
    }

    assert len(matrix["deltas"]) == 30
    assert expected_delta_ids <= set(deltas)
    for delta_id in expected_delta_ids:
        delta = deltas[delta_id]
        assert delta["source_path"] == source["path"]
        assert delta["source_sha256"] == source["sha256"]
        assert delta["action_gate"] != "APPROVE"
        assert delta["action_gate"] != "APPROVE_LOCAL_DOCS_ONLY"

    falsifiers = {item["id"]: item for item in matrix["falsifiers"]}
    assert falsifiers["security_offensive_execution_blocked"]["action_gate"] == "BLOCK"
