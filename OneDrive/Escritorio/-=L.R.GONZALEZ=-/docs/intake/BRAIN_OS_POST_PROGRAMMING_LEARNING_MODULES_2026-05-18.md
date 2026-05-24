# BRAIN_OS POST Programming and AI Learning Modules 2026-05-18

Status: `LOCAL_PROGRAMMING_LEARNING_WORKPACK`

RuntimeImport=BLOCK

PublicationGate=BLOCK

RawAdoption=BLOCK

ModelTraining=BLOCK

This artifact converts the curated POST insights into programming module cards and an AI-learning curriculum for local agents. It does not train a model, extract ZIPs, publish content or import raw runtime code. Multiple runtime modules may be rebuilt clean-room only as isolated gated slices with target-lane tests.

## Module Cards

| module | family | gate | evidence | target |
|---|---|---|---|---|
| `post_boundary_guardrail_compiler` | `Boundary` | `BLOCK` | `REQUIRES_EVIDENCE` | tools/release validators, docs/intake, future ActionGate tests |
| `post_gate_simulation_contract` | `Gate` | `BLOCK` | `REQUIRES_EVIDENCE` | ActionGate contracts, Wabi/Claudio gate fixtures |
| `post_security_workbench_contract` | `Security` | `BLOCK` | `FALSIFIER_OR_DEFECT` | packages/open-dev/obs-safe-integration-kit; tests; docs/developer Wabi integration packet |
| `post_math_state_learning_lab` | `Math-State` | `REVIEW` | `REQUIRES_EVIDENCE` | Wabi geodia math tests, Claudio R/Phi backlog, docs/intake |
| `post_continuity_handoff_validator` | `Continuity` | `REVIEW` | `REQUIRES_EVIDENCE` | NEXT_SESSION_BRIEF, SESSION_FINGERPRINT, QA reports, bulletin board |
| `post_falsifier_fixture_suite` | `Falsifiers` | `BLOCK` | `REQUIRES_EVIDENCE` | tests/release, Wabi formal contract intake, Claudio R/Phi tests |
| `post_zip_evidence_adapter` | `Boundary` | `BLOCK` | `REQUIRES_EVIDENCE` | tools/release, docs/intake, future source-card compiler |

## Learning Path

### Phase 1 - boundary_before_runtime

Modules:
- `post_boundary_guardrail_compiler`
- `post_zip_evidence_adapter`

Exit criteria:
- aliases normalized
- ZIPs referenced without extraction
- publication/runtime/raw adoption gates blocked

### Phase 2 - gates_and_falsifiers

Modules:
- `post_gate_simulation_contract`
- `post_security_workbench_contract`
- `post_falsifier_fixture_suite`

Exit criteria:
- negative fixtures exist
- strong terms are not approved
- simulation is separate from execution permission
- security tools remain dry-run/fixture-only with no external target touched

### Phase 3 - bounded_programming

Modules:
- `post_math_state_learning_lab`
- `post_continuity_handoff_validator`

Exit criteria:
- target-lane failing test exists before implementation
- closure derives from real test output

## Gates

- Use only curated metadata, requirements, anchors and tests.
- Rebuild future code from reviewed requirements; do not copy source text or ZIP members.
- Every runtime step starts with a failing target-lane test.

## Next Action

Implement multiple runtime modules only as isolated gated slices: one module, one test file, one rollback-safe change set at a time.
