from __future__ import annotations

from dataclasses import dataclass
from typing import Any


BLOCKED_GATES = {
    "RuntimeImport": "runtime import",
    "PublicationGate": "publication",
    "RawAdoption": "raw adoption",
    "ModelTraining": "model training",
    "CloudTraining": "cloud training",
    "ZipExtraction": "zip extraction",
}

ACTION_BLOCK_TERMS = {
    "publish": "PublicationGate",
    "publicar": "PublicationGate",
    "publication": "PublicationGate",
    "runtime import": "RuntimeImport",
    "import runtime": "RuntimeImport",
    "raw adoption": "RawAdoption",
    "adopcion cruda": "RawAdoption",
    "adopción cruda": "RawAdoption",
    "model training": "ModelTraining",
    "fine-tune": "ModelTraining",
    "finetune": "ModelTraining",
    "cloud training": "CloudTraining",
    "provider change": "CloudTraining",
    "extract zip": "ZipExtraction",
    "zip extraction": "ZipExtraction",
    "secret": "SecretBoundary",
    "token": "SecretBoundary",
    "credential": "SecretBoundary",
    "payload": "OffensiveSecurityBoundary",
    "shell": "OffensiveSecurityBoundary",
    "database dump": "OffensiveSecurityBoundary",
    "db dump": "OffensiveSecurityBoundary",
    "dump": "OffensiveSecurityBoundary",
    "bypass": "OffensiveSecurityBoundary",
    "exfiltration": "OffensiveSecurityBoundary",
    "exfiltracion": "OffensiveSecurityBoundary",
    "exfiltración": "OffensiveSecurityBoundary",
    "cookie": "SecretBoundary",
    "password": "SecretBoundary",
}

ACTION_REVIEW_TERMS = {
    "nmap": "DUAL_USE_SECURITY_TOOL_REQUIRES_SCOPE",
    "nikto": "DUAL_USE_SECURITY_TOOL_REQUIRES_SCOPE",
    "maltego": "OSINT_TOOL_REQUIRES_SCOPE",
    "recon ng": "OSINT_TOOL_REQUIRES_SCOPE",
    "recon-ng": "OSINT_TOOL_REQUIRES_SCOPE",
    "metasploit": "OFFENSIVE_VALIDATOR_REQUIRES_LAB_REVIEW",
    "sqlmap": "OFFENSIVE_VALIDATOR_REQUIRES_LAB_REVIEW",
    "john": "PASSWORD_AUDIT_REQUIRES_SYNTHETIC_OR_OWNED_HASH_REVIEW",
    "hashcat": "PASSWORD_AUDIT_REQUIRES_SYNTHETIC_OR_OWNED_HASH_REVIEW",
}

REQUIRES_EVIDENCE_TERMS = {
    "pass": "SELF_REPORTED_SUCCESS",
    "probado": "SELF_REPORTED_SUCCESS",
    "benchmark": "BENCHMARK_REQUIRES_CURRENT_OUTPUT",
    "derivada": "FORMAL_DERIVATION_REQUIRES_LOCAL_PROOF",
    "proof": "FORMAL_DERIVATION_REQUIRES_LOCAL_PROOF",
    "phisica": "SCIENCE_CLAIM_REQUIRES_EVIDENCE",
    "fisica": "SCIENCE_CLAIM_REQUIRES_EVIDENCE",
    "física": "SCIENCE_CLAIM_REQUIRES_EVIDENCE",
    "sueño": "DREAM_INTERPRETATION_REQUIRES_EVIDENCE",
    "dream": "DREAM_INTERPRETATION_REQUIRES_EVIDENCE",
    "jung": "ARCHETYPE_LANGUAGE_REQUIRES_REVIEW",
    "neurobiología": "NEUROBIOLOGY_CLAIM_REQUIRES_PRIMARY_REVIEW",
    "hipnagogia": "HYPNAGOGIA_ANALOGY_REQUIRES_BOUNDARY",
    "prefrontal": "PREFRONTAL_ANALOGY_REQUIRES_BOUNDARY",
    "metacognicion": "METACOGNITION_RUNTIME_CLAIM_REQUIRES_TESTS",
    "metacognición": "METACOGNITION_RUNTIME_CLAIM_REQUIRES_TESTS",
}

CLAIM_BLOCK_TERMS = {
    "consciencia": "CONSCIOUSNESS_CLAIM_BLOCK",
    "conciencia": "CONSCIOUSNESS_CLAIM_BLOCK",
    "agi": "AGI_CLAIM_BLOCK",
    "medicina": "MEDICAL_CLAIM_BLOCK",
    "medical": "MEDICAL_CLAIM_BLOCK",
    "secret": "SECRET_OR_TOKEN_BOUNDARY",
    "token": "SECRET_OR_TOKEN_BOUNDARY",
    "credential": "SECRET_OR_TOKEN_BOUNDARY",
    "cósmica": "COSMIC_OR_SPIRITUAL_CLAIM_BLOCK",
    "cosmica": "COSMIC_OR_SPIRITUAL_CLAIM_BLOCK",
    "ai generated": "AI_GENERATED_IMAGE_NOT_SOURCE_EVIDENCE",
    "raw code": "RAW_CODE_IMPORT_BLOCK",
    "payload": "OFFENSIVE_SECURITY_CLAIM_BLOCK",
    "shell": "OFFENSIVE_SECURITY_CLAIM_BLOCK",
    "dump": "OFFENSIVE_SECURITY_CLAIM_BLOCK",
    "bypass": "OFFENSIVE_SECURITY_CLAIM_BLOCK",
    "exfiltration": "OFFENSIVE_SECURITY_CLAIM_BLOCK",
    "cookie": "SECRET_OR_TOKEN_BOUNDARY",
    "password": "SECRET_OR_TOKEN_BOUNDARY",
}


@dataclass(frozen=True)
class GateDecision:
    decision: str
    reasons: tuple[str, ...]
    blocked_by: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "reasons": list(self.reasons),
            "blocked_by": list(self.blocked_by),
        }


def normalize_text(value: str) -> str:
    return " ".join(value.casefold().replace("_", " ").replace("-", " ").split())


def evaluate_action(
    requested_action: str,
    *,
    action_tags: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    normalized = normalize_text(requested_action)
    tags = {tag for tag in (action_tags or [])}
    blocked_by: list[str] = []
    reasons: list[str] = []

    for gate in BLOCKED_GATES:
        if gate in tags:
            blocked_by.append(gate)
            reasons.append(f"{gate}=BLOCK")

    for term, gate in ACTION_BLOCK_TERMS.items():
        if term in normalized and gate not in blocked_by:
            blocked_by.append(gate)
            reasons.append(f"{gate}=BLOCK_BY_TERM:{term}")

    if blocked_by:
        return GateDecision("BLOCK", tuple(reasons), tuple(blocked_by)).as_dict()

    review_reasons = []
    for term, reason in ACTION_REVIEW_TERMS.items():
        if term in normalized:
            review_reasons.append(f"{reason}: {term}")

    if review_reasons:
        return GateDecision(
            "REVIEW",
            tuple(review_reasons),
            tuple(),
        ).as_dict()

    if {"REVIEW", "ScienceClaimGate", "ExternalAction"} & tags:
        return GateDecision(
            "REVIEW",
            ("human or evidence review required",),
            tuple(),
        ).as_dict()

    return GateDecision(
        "APPROVE_LOCAL_DOCS_ONLY",
        ("local curated metadata and tests only",),
        tuple(),
    ).as_dict()


def evaluate_claim_text(claim_text: str) -> dict[str, Any]:
    normalized = normalize_text(claim_text)
    matched: list[dict[str, str]] = []

    for term, reason in CLAIM_BLOCK_TERMS.items():
        if term in normalized:
            matched.append({"term": term, "reason": reason})

    if matched:
        return {
            "decision": "BLOCK",
            "claim_boundary": "STRONG_OR_SENSITIVE_CLAIM_BLOCK",
            "matched_terms": matched,
        }

    for term, reason in REQUIRES_EVIDENCE_TERMS.items():
        if term in normalized:
            matched.append({"term": term, "reason": reason})

    if matched:
        return {
            "decision": "REQUIRES_EVIDENCE",
            "claim_boundary": "CURRENT_LOCAL_EVIDENCE_REQUIRED",
            "matched_terms": matched,
        }

    return {
        "decision": "APPROVE_LOCAL_DOCS_ONLY",
        "claim_boundary": "LOW_CLAIM_LOCAL_DOCS",
        "matched_terms": [],
    }


def _delta_index(matrix: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {delta["id"]: delta for delta in matrix["deltas"]}


def _source_refs_ok(card: dict[str, Any]) -> bool:
    for ref in card["source_refs"]:
        if not ref.get("source_path"):
            return False
        if not ref.get("source_sha256"):
            return False
        if not ref.get("evidence"):
            return False
        if not ref.get("claim_boundary"):
            return False
    return True


def compile_zip_evidence(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    compiled: list[dict[str, Any]] = []
    for item in matrix["zip_inventory"]:
        compiled.append(
            {
                "path": item["path"],
                "sha256": item["sha256"],
                "testzip": item["testzip"],
                "entry_count": item["entry_count"],
                "member_anchors": [
                    f"{item['path']}::{entry}" for entry in item["entries"]
                ],
                "suspicious_name_entries": item["suspicious_name_entries"],
                "extraction_gate": "BLOCK",
                "runtime_import_gate": "BLOCK",
                "content_policy": "METADATA_AND_MEMBER_NAMES_ONLY",
            }
        )
    return compiled


def _module_negative_fixtures(card: dict[str, Any]) -> list[dict[str, Any]]:
    samples = [
        "Benchmark PASS PROBADO without current pytest evidence",
        "AGI/consciencia as fact",
        "medicina claim",
        "secret token exposure",
    ]
    if "zip" in card["module_id"]:
        samples.append("extract ZIP members into runtime")
    if "gate" in card["module_id"]:
        samples.append("simulate cloud provider change as approved execution")
    if "continuity" in card["module_id"]:
        samples.append("mark closure done without test output")
    return [
        {
            "sample": sample,
            "claim_decision": evaluate_claim_text(sample),
            "action_decision": evaluate_action(sample),
        }
        for sample in samples
    ]


def compile_module(card: dict[str, Any], deltas_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    missing_delta_ids = [
        delta_id for delta_id in card["source_delta_ids"] if delta_id not in deltas_by_id
    ]
    source_delta_gates = [
        deltas_by_id[delta_id]["action_gate"]
        for delta_id in card["source_delta_ids"]
        if delta_id in deltas_by_id
    ]
    return {
        "module_id": card["module_id"],
        "family": card["family"],
        "status": "COMPILED_LOCAL_PROGRAMMING_CONTRACT",
        "target_lane": card["target_lane"],
        "source_delta_ids": list(card["source_delta_ids"]),
        "missing_delta_ids": missing_delta_ids,
        "source_refs": list(card["source_refs"]),
        "source_refs_valid": _source_refs_ok(card),
        "source_delta_gates": source_delta_gates,
        "gate": card["module_gate"],
        "evidence_state": card["evidence_state"],
        "programming_objective": card["programming_objective"],
        "learning_objective": card["learning_objective"],
        "input_contract": list(card["input_contract"]),
        "output_contract": [
            "compiled local validator contract",
            "negative fixtures",
            "gate simulation cases",
            "benchmark evidence requirements",
        ],
        "allowed_write_scope": [
            "tools/release",
            "tests/release",
            "docs/intake",
            "root closure docs",
        ],
        "blocked_actions": sorted(set(card["blocked_actions"]) | set(BLOCKED_GATES)),
        "negative_fixtures": _module_negative_fixtures(card),
        "simulation_cases": [
            evaluate_action("write local docs from curated metadata"),
            evaluate_action("runtime import POST source", action_tags=["RuntimeImport"]),
            evaluate_action("publish POST workpack", action_tags=["PublicationGate"]),
            evaluate_action("train model from POST corpus", action_tags=["ModelTraining"]),
            evaluate_action("extract ZIP members into workspace", action_tags=["ZipExtraction"]),
        ],
        "required_tests": list(card["required_tests"])
        + [
            "compiled module has no missing source deltas",
            "blocked actions stay BLOCK",
            "negative fixtures do not approve strong claims",
        ],
    }


def compile_learning_program(
    matrix: dict[str, Any],
    workpack: dict[str, Any],
) -> dict[str, Any]:
    deltas_by_id = _delta_index(matrix)
    compiled_modules = [
        compile_module(card, deltas_by_id) for card in workpack["module_cards"]
    ]
    covered_delta_ids = sorted(
        {
            delta_id
            for module in compiled_modules
            for delta_id in module["source_delta_ids"]
        }
    )
    all_delta_ids = sorted(deltas_by_id)
    return {
        "schema_version": "brain_os.post_compiled_learning_program.v1",
        "created_date": "2026-05-18",
        "status": "LOCAL_PROGRAMMING_CONTRACTS_COMPILED",
        "source_matrix": workpack["source_matrix"],
        "source_workpack": "docs/intake/BRAIN_OS_POST_PROGRAMMING_LEARNING_MODULES_2026-05-18.json",
        "learning_boundary": {
            "mode": "symbolic_curriculum_test_first_programming",
            "training_data_status": "CURATED_METADATA_REQUIREMENTS_AND_FIXTURES_ONLY",
            "model_training": "BLOCK",
            "cloud_training": "BLOCK",
            "raw_source_import": "BLOCK",
            "zip_extraction": "BLOCK",
        },
        "gate_summary": {
            "RuntimeImport": "BLOCK",
            "PublicationGate": "BLOCK",
            "RawAdoption": "BLOCK",
            "ModelTraining": "BLOCK",
            "CloudTraining": "BLOCK",
            "ZipExtraction": "BLOCK",
        },
        "coverage": {
            "module_count": len(compiled_modules),
            "all_delta_ids": all_delta_ids,
            "covered_delta_ids": covered_delta_ids,
            "uncovered_delta_ids": [
                delta_id for delta_id in all_delta_ids if delta_id not in covered_delta_ids
            ],
            "modules_with_missing_delta_ids": [
                module["module_id"]
                for module in compiled_modules
                if module["missing_delta_ids"]
            ],
        },
        "compiled_modules": compiled_modules,
        "zip_evidence": compile_zip_evidence(matrix),
        "benchmarks": [
            "python -m json.tool docs/intake/BRAIN_OS_POST_COMPILED_LEARNING_PROGRAM_2026-05-18.json",
            "python -m pytest tests/release/test_curador_preflight_selective_extraction.py tests/release/test_brain_os_post_unified_framework.py tests/release/test_brain_os_post_batch_insights.py tests/release/test_brain_os_post_learning_modules.py tests/release/test_brain_os_post_learning_program.py -q",
            "python -m pytest apps/local/wabi-sabi/tests/test_formal_contract_intake.py -q",
            "python -m pytest tests -q",
            "cd apps/local/wabi-sabi; python -m pytest -q",
        ],
        "blocked_actions": sorted(BLOCKED_GATES),
        "next_action": "If runtime is opened later, select one compiled module and create the target-lane failing test first.",
    }
