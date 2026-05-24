from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MATRIX_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.json"
OUT_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_PROGRAMMING_LEARNING_MODULES_2026-05-18.json"
OUT_MD = ROOT / "docs" / "intake" / "BRAIN_OS_POST_PROGRAMMING_LEARNING_MODULES_2026-05-18.md"


MODULE_SPECS = [
    {
        "module_id": "post_boundary_guardrail_compiler",
        "family": "Boundary",
        "source_delta_ids": [
            "boundary.alias_normalization_and_no_register",
            "boundary.publication_runtime_raw_adoption_block",
            "boundary.cloud_plan_requires_local_gate",
            "zip.teorias_consciencia_claims_blocked",
            "falsifiers.formal_framework_preprint_benchmark_claims_require_current_evidence",
            "falsifiers.ra_horus_dream_science_and_raw_code_claims_blocked",
        ],
        "programming_objective": "Build validators that normalize source aliases, block raw adoption, and force explicit gates before publication, runtime or cloud actions.",
        "learning_objective": "Teach local agents to classify source material before using it, and to demote strong claims to REVIEW or BLOCK.",
        "target_lane": "tools/release validators, docs/intake, future ActionGate tests",
        "allowed_actions": [
            "generate validation tests",
            "write local-only docs",
            "create structured workpacks",
            "reference exact source paths and hashes",
        ],
        "blocked_actions": [
            "RuntimeImport",
            "PublicationGate approval",
            "RawAdoption",
            "external posting",
            "secret or token handling",
        ],
    },
    {
        "module_id": "post_gate_simulation_contract",
        "family": "Gate",
        "source_delta_ids": [
            "gate.ghostgate_actiongate_scienceclaimgate_split",
            "gate.formal_framework_ghostgate_classical_simulation",
            "gate.ra_horus_agency_state_machine_requires_runtime_tests",
            "gate.ra_horus_pre_action_generation_gate",
            "zip.truthgate_eic_member_anchors",
            "boundary.cloud_plan_requires_local_gate",
        ],
        "programming_objective": "Convert GhostGate/ActionGate/ScienceClaimGate insights into a testable pre-action contract and fixture set.",
        "learning_objective": "Teach the agent to simulate before executing and to separate planning evidence from execution permission.",
        "target_lane": "ActionGate contracts, Wabi/Claudio gate fixtures",
        "allowed_actions": [
            "add negative fixtures",
            "generate gate decision examples",
            "write REVIEW/BLOCK test cases",
        ],
        "blocked_actions": [
            "cloud execution",
            "provider changes",
            "credential reads",
            "unbounded process execution",
        ],
    },
    {
        "module_id": "post_security_workbench_contract",
        "family": "Security",
        "source_delta_ids": [
            "security.scope_registry_authorization_required",
            "security.action_gate_dual_use_tools",
            "security.tool_catalog_default_gates",
            "security.dry_run_adapter_contract",
            "security.output_sanitizer_redaction",
            "security.risk_mapper_business_remediation",
            "security.witnesslog_handoff_security",
            "falsifiers.security_offensive_execution_blocked",
        ],
        "programming_objective": "Rebuild the Ethical Security Workbench as a defensive dry-run and fixture-only contract in obs-safe before any Wabi wrapper exists.",
        "learning_objective": "Teach local agents to separate authorized defensive observation from raw dual-use tool execution, exploitation, cracking, dumps and secret handling.",
        "target_lane": "packages/open-dev/obs-safe-integration-kit; tests; docs/developer Wabi integration packet",
        "allowed_actions": [
            "define security scope records",
            "list default-gated security tools",
            "build dry-run plans without execution",
            "parse synthetic fixtures",
            "redact sensitive output",
            "generate remediation reports and witness handoff",
        ],
        "blocked_actions": [
            "executing nmap nikto sqlmap metasploit john hashcat maltego or recon-ng",
            "external target scanning",
            "exploitation",
            "payloads",
            "shells",
            "database dumps",
            "password cracking",
            "bypass or exfiltration",
            "secret or credential output",
            "Wabi CLI integration before obs-safe contract stability",
        ],
    },
    {
        "module_id": "post_math_state_learning_lab",
        "family": "Math-State",
        "source_delta_ids": [
            "math_state.phi_eff_as_method_not_proof",
            "math_state.formal_lab_demotes_physics_claims",
            "math_state.formal_framework_shannon_bridge_requires_calibration",
            "math_state.ra_horus_dynamic_temperature_and_r_velocity",
            "zip.formalizados_engine_runtime_import_block",
        ],
        "programming_objective": "Translate R/Phi_eff and formal-lab ideas into bounded tests and comparison helpers without copying prototype code.",
        "learning_objective": "Teach the system to treat math-state claims as hypotheses requiring fixtures, tolerances and measured evidence.",
        "target_lane": "Wabi geodia math tests, Claudio R/Phi backlog, docs/intake",
        "allowed_actions": [
            "write synthetic fixtures",
            "define tolerance tests",
            "create comparison adapters from requirements",
        ],
        "blocked_actions": [
            "copying osit_epistemic_engine code",
            "claiming scientific proof",
            "model training",
            "runtime replacement",
        ],
    },
    {
        "module_id": "post_continuity_handoff_validator",
        "family": "Continuity",
        "source_delta_ids": [
            "continuity.meta_review_prioritizes_direct_cleanup_dangerous",
            "continuity.formal_framework_handoff_fingerprint_contract",
            "continuity.ra_horus_prerequisite_knowledge_graph",
            "zip.trabajo_mejorado_public_safe_qa_handoff",
        ],
        "programming_objective": "Convert Handoff/QA/public-safe insights into validators for session fingerprints, next-session briefs and evidence closure.",
        "learning_objective": "Teach agents that closure text must be derived from actual test evidence, not self-reported completion.",
        "target_lane": "NEXT_SESSION_BRIEF, SESSION_FINGERPRINT, QA reports, bulletin board",
        "allowed_actions": [
            "validate closure JSON",
            "write handoff consistency checks",
            "generate next-action workpacks",
        ],
        "blocked_actions": [
            "marking unverified tasks done",
            "publication claims",
            "broad cleanup",
            "moving raw sources",
        ],
    },
    {
        "module_id": "post_falsifier_fixture_suite",
        "family": "Falsifiers",
        "source_delta_ids": [
            "falsifiers.benchmark_pass_terms_require_current_evidence",
            "falsifiers.formal_framework_preprint_benchmark_claims_require_current_evidence",
            "falsifiers.ra_horus_dream_science_and_raw_code_claims_blocked",
            "falsifiers.noumeno_consciousness_physics_claims_blocked",
            "zip.formalizados_engine_runtime_import_block",
        ],
        "programming_objective": "Convert PASS/PROBADO/Benchmark and strong-claim language into negative fixtures and regression tests.",
        "learning_objective": "Teach the agent to prefer falsifiers and current evidence over confident source wording.",
        "target_lane": "tests/release, Wabi formal contract intake, Claudio R/Phi tests",
        "allowed_actions": [
            "write failing tests first",
            "record negative fixtures",
            "gate self-reported success terms",
        ],
        "blocked_actions": [
            "approving benchmark terms without test output",
            "publishing consciousness or AGI claims",
            "medical claims",
            "secret or token exposure",
        ],
    },
    {
        "module_id": "post_zip_evidence_adapter",
        "family": "Boundary",
        "source_delta_ids": [
            "zip.truthgate_eic_member_anchors",
            "zip.formalizados_engine_runtime_import_block",
            "zip.teorias_consciencia_claims_blocked",
            "zip.trabajo_mejorado_public_safe_qa_handoff",
        ],
        "programming_objective": "Create a safe ZIP evidence adapter contract that reads metadata and member anchors without extraction to runtime.",
        "learning_objective": "Teach agents to use ZIPs as evidence containers, not source trees to adopt wholesale.",
        "target_lane": "tools/release, docs/intake, future source-card compiler",
        "allowed_actions": [
            "read ZIP metadata",
            "reference zip_path::member anchors",
            "hash containers",
            "test for suspicious member names",
        ],
        "blocked_actions": [
            "extracting ZIP members into workspace",
            "runtime import from ZIP",
            "public packaging",
            "copying internal prompts",
        ],
    },
]


def load_matrix() -> dict[str, Any]:
    return json.loads(MATRIX_JSON.read_text(encoding="utf-8"))


def _by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in items}


def _strictest_gate(deltas: list[dict[str, Any]]) -> str:
    gates = {delta["action_gate"] for delta in deltas}
    if "BLOCK" in gates:
        return "BLOCK"
    if "REVIEW" in gates:
        return "REVIEW"
    return "APPROVE_LOCAL_DOCS_ONLY"


def _evidence_state(deltas: list[dict[str, Any]]) -> str:
    states = {delta["evidence_state"] for delta in deltas}
    if any("FALSIFIER" in state for state in states):
        return "FALSIFIER_OR_DEFECT"
    if "REQUIRES_EVIDENCE" in states:
        return "REQUIRES_EVIDENCE"
    return "OVERLAP_REINFORCES_EXISTING"


def build_module_card(spec: dict[str, Any], deltas_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    deltas = [deltas_by_id[delta_id] for delta_id in spec["source_delta_ids"]]
    source_refs = []
    for delta in deltas:
        source_refs.append(
            {
                "delta_id": delta["id"],
                "source_path": delta["source_path"],
                "source_sha256": delta["source_sha256"],
                "evidence": delta["line_or_member_evidence"],
                "claim_boundary": delta["claim_boundary"],
            }
        )
    return {
        "module_id": spec["module_id"],
        "family": spec["family"],
        "status": "PROGRAMMING_LEARNING_SPEC",
        "module_gate": _strictest_gate(deltas),
        "evidence_state": _evidence_state(deltas),
        "training_data_status": "CURATED_METADATA_AND_REQUIREMENTS_ONLY",
        "model_training": "BLOCK",
        "runtime_import": "BLOCK",
        "publication_gate": "BLOCK",
        "raw_adoption": "BLOCK",
        "source_delta_ids": list(spec["source_delta_ids"]),
        "source_refs": source_refs,
        "target_lane": spec["target_lane"],
        "programming_objective": spec["programming_objective"],
        "learning_objective": spec["learning_objective"],
        "input_contract": [
            "curated matrix JSON",
            "exact source path and SHA256",
            "line_or_member_evidence anchors",
            "claim_boundary",
            "ActionGate decision",
        ],
        "output_contract": [
            "test-first implementation plan",
            "negative fixtures where needed",
            "local docs or validators",
            "updated handoff with evidence",
        ],
        "required_tests": [
            "source provenance and hash retained",
            "RuntimeImport remains BLOCK",
            "PublicationGate remains BLOCK",
            "RawAdoption remains BLOCK",
            "strong claims require REQUIRES_EVIDENCE or BLOCK",
        ],
        "allowed_actions": list(spec["allowed_actions"]),
        "blocked_actions": list(spec["blocked_actions"]),
    }


def build_learning_path(module_cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "phase": 1,
            "name": "boundary_before_runtime",
            "module_ids": [
                "post_boundary_guardrail_compiler",
                "post_zip_evidence_adapter",
            ],
            "exit_criteria": [
                "aliases normalized",
                "ZIPs referenced without extraction",
                "publication/runtime/raw adoption gates blocked",
            ],
        },
        {
            "phase": 2,
            "name": "gates_and_falsifiers",
            "module_ids": [
                "post_gate_simulation_contract",
                "post_security_workbench_contract",
                "post_falsifier_fixture_suite",
            ],
            "exit_criteria": [
                "negative fixtures exist",
                "strong terms are not approved",
                "simulation is separate from execution permission",
                "security tools remain dry-run/fixture-only with no external target touched",
            ],
        },
        {
            "phase": 3,
            "name": "bounded_programming",
            "module_ids": [
                "post_math_state_learning_lab",
                "post_continuity_handoff_validator",
            ],
            "exit_criteria": [
                "target-lane failing test exists before implementation",
                "closure derives from real test output",
            ],
        },
    ]


def build_task_packets(module_cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    packets = []
    for card in module_cards:
        packets.append(
            {
                "packet_id": f"codex_{card['module_id']}",
                "mode": "test_first_local_programming",
                "application_gate": "REVIEW",
                "module_id": card["module_id"],
                "prompt": (
                    f"Implement only the next safe test-first step for {card['module_id']} "
                    "from curated requirements. Do not import raw POST source or extract ZIP members."
                ),
                "write_scope": [
                    "tests/release or target-lane tests",
                    "docs/intake or local validator modules",
                ],
                "blocked_now": [
                    "RuntimeImport",
                    "PublicationGate approval",
                    "RawAdoption",
                    "cloud/model training",
                    "secret/token exposure",
                ],
                "evidence_required": card["required_tests"],
            }
        )
    return packets


def build_payload() -> dict[str, Any]:
    matrix = load_matrix()
    deltas_by_id = _by_id(matrix["deltas"])
    cards = [build_module_card(spec, deltas_by_id) for spec in MODULE_SPECS]
    covered = sorted({delta_id for card in cards for delta_id in card["source_delta_ids"]})
    all_delta_ids = sorted(deltas_by_id)
    return {
        "schema_version": "brain_os.post_programming_learning_modules.v1",
        "created_date": "2026-05-18",
        "source_matrix": str(MATRIX_JSON.relative_to(ROOT)),
        "status": "LOCAL_PROGRAMMING_LEARNING_WORKPACK",
        "learning_boundary": {
            "ai_learning_mode": "symbolic_curriculum_and_test_first_programming",
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
        },
        "coverage": {
            "all_delta_ids": all_delta_ids,
            "covered_delta_ids": covered,
            "uncovered_delta_ids": [delta_id for delta_id in all_delta_ids if delta_id not in covered],
        },
        "module_cards": cards,
        "learning_path": build_learning_path(cards),
        "codex_task_packets": build_task_packets(cards),
        "next_action": "Implement multiple runtime modules only as isolated gated slices: one module, one test file, one rollback-safe change set at a time.",
    }


def render_md(payload: dict[str, Any]) -> str:
    lines = [
        "# BRAIN_OS POST Programming and AI Learning Modules 2026-05-18",
        "",
        "Status: `LOCAL_PROGRAMMING_LEARNING_WORKPACK`",
        "",
        "RuntimeImport=BLOCK",
        "",
        "PublicationGate=BLOCK",
        "",
        "RawAdoption=BLOCK",
        "",
        "ModelTraining=BLOCK",
        "",
            "This artifact converts the curated POST insights into programming module cards and an AI-learning curriculum for local agents. It does not train a model, extract ZIPs, publish content or import raw runtime code. Multiple runtime modules may be rebuilt clean-room only as isolated gated slices with target-lane tests.",
        "",
        "## Module Cards",
        "",
        "| module | family | gate | evidence | target |",
        "|---|---|---|---|---|",
    ]
    for card in payload["module_cards"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{card['module_id']}`",
                    f"`{card['family']}`",
                    f"`{card['module_gate']}`",
                    f"`{card['evidence_state']}`",
                    card["target_lane"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Learning Path",
            "",
        ]
    )
    for phase in payload["learning_path"]:
        lines.append(f"### Phase {phase['phase']} - {phase['name']}")
        lines.append("")
        lines.append("Modules:")
        lines.extend(f"- `{module_id}`" for module_id in phase["module_ids"])
        lines.append("")
        lines.append("Exit criteria:")
        lines.extend(f"- {criterion}" for criterion in phase["exit_criteria"])
        lines.append("")
    lines.extend(
        [
            "## Gates",
            "",
            "- Use only curated metadata, requirements, anchors and tests.",
            "- Rebuild future code from reviewed requirements; do not copy source text or ZIP members.",
            "- Every runtime step starts with a failing target-lane test.",
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    payload = build_payload()
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "module_cards": len(payload["module_cards"]),
                "uncovered_delta_ids": payload["coverage"]["uncovered_delta_ids"],
                "output": str(OUT_JSON),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
