# BRAIN_OS POST Compiled Learning Program 2026-05-18

Status: `LOCAL_PROGRAMMING_CONTRACTS_COMPILED`

RuntimeImport=BLOCK
PublicationGate=BLOCK
RawAdoption=BLOCK
ModelTraining=BLOCK
CloudTraining=BLOCK
ZipExtraction=BLOCK

This program turns the curated POST workpack into deterministic local programming contracts, fixtures and benchmark requirements. It does not train a model, publish content, import raw source, extract ZIP members or approve runtime adoption.

## Coverage

- Modules: `7`
- Covered deltas: `30`
- Uncovered deltas: `0`
- Modules with missing deltas: `0`

## Compiled Modules

| module | family | gate | evidence | target |
|---|---|---|---|---|
| `post_boundary_guardrail_compiler` | `Boundary` | `BLOCK` | `REQUIRES_EVIDENCE` | tools/release validators, docs/intake, future ActionGate tests |
| `post_gate_simulation_contract` | `Gate` | `BLOCK` | `REQUIRES_EVIDENCE` | ActionGate contracts, Wabi/Claudio gate fixtures |
| `post_security_workbench_contract` | `Security` | `BLOCK` | `FALSIFIER_OR_DEFECT` | packages/open-dev/obs-safe-integration-kit; tests; docs/developer Wabi integration packet |
| `post_math_state_learning_lab` | `Math-State` | `REVIEW` | `REQUIRES_EVIDENCE` | Wabi geodia math tests, Claudio R/Phi backlog, docs/intake |
| `post_continuity_handoff_validator` | `Continuity` | `REVIEW` | `REQUIRES_EVIDENCE` | NEXT_SESSION_BRIEF, SESSION_FINGERPRINT, QA reports, bulletin board |
| `post_falsifier_fixture_suite` | `Falsifiers` | `BLOCK` | `REQUIRES_EVIDENCE` | tests/release, Wabi formal contract intake, Claudio R/Phi tests |
| `post_zip_evidence_adapter` | `Boundary` | `BLOCK` | `REQUIRES_EVIDENCE` | tools/release, docs/intake, future source-card compiler |

## ZIP Evidence

| zip | entries | testzip | extraction | runtime import |
|---|---:|---|---|---|
| `MEDIOEVO_OSIT_DOCUMENTOS_ACTUALIZADOS_TRUTHGATE_EIC_v0_3_2026-05-17.zip` | `23` | `None` | `BLOCK` | `BLOCK` |
| `MEDIOEVO_OSIT_DOCUMENTOS_FORMALIZADOS_v2_1_2026-05-17.zip` | `25` | `None` | `BLOCK` | `BLOCK` |
| `MEDIOEVO_OSIT_TEORIAS_COMUNICACION_CONSCIENCIA_v0_1_2026-05-17.zip` | `20` | `None` | `BLOCK` | `BLOCK` |
| `MEDIOEVO_OSIT_TRABAJO_MEJORADO_v0_2_2026-05-17.zip` | `30` | `None` | `BLOCK` | `BLOCK` |

## Benchmarks

- `python -m json.tool docs/intake/BRAIN_OS_POST_COMPILED_LEARNING_PROGRAM_2026-05-18.json`
- `python -m pytest tests/release/test_curador_preflight_selective_extraction.py tests/release/test_brain_os_post_unified_framework.py tests/release/test_brain_os_post_batch_insights.py tests/release/test_brain_os_post_learning_modules.py tests/release/test_brain_os_post_learning_program.py -q`
- `python -m pytest apps/local/wabi-sabi/tests/test_formal_contract_intake.py -q`
- `python -m pytest tests -q`
- `cd apps/local/wabi-sabi; python -m pytest -q`

## Next Action

If runtime is opened later, select one compiled module and create the target-lane failing test first.
