# Formal Code Rescan + Claudio/Wabi Integration - 2026-05-08

## Scope

Source: `C:\Users\L-Tyr\OneDrive\Escritorio\Formal`

Mode: static analysis plus gated provider smoke. No Formal script was executed,
no ZIP was unpacked in place, no file was deleted or moved, and no secret value
was copied into this report.

## Provider Reality

| Provider | Result | Evidence | Gate |
|---|---|---|---|
| NVIDIA NIM `super` | Real call succeeded through `Claudio -> Wabi -> nvidia-nim` | output `OK`, action `cloud_chat_completion` | `APPROVE_FOR_GATED_SMOKE` |
| NVIDIA NIM `ultra` | Authenticated env key reached provider but model/function was unavailable to current account | provider returned `404 Function not found for account` | `MODEL_ACCESS_REVIEW` |
| NVIDIA token from `banananana.txt` | Tried as NVIDIA bearer; provider returned unauthorized | `401 Authentication failed` | `CREDENTIAL_TYPE_MISMATCH` |
| Qwen cloud | Not called | no `DASHSCOPE_API_KEY` or `QWEN_API_KEY` present; Alibaba AccessKey material is not treated as DashScope bearer | `MISSING_QWEN_BEARER` |

Decision: Wabi/Sabi cloud wiring is functional. NVIDIA `super` is the current
working cloud programming fallback. Qwen remains configured but inactive until a
proper DashScope/Qwen API key is provided in env/vault.

## Claudio Change

`core/wabi_gateway.py` now supports explicit per-call cloud opt-in:

- default remains `WABI_ALLOW_CLOUD_PROVIDERS=0`;
- `allow_cloud=True` is accepted only for `nvidia`, `nvidia-nim`, `qwen` or
  `qwen-cloud`;
- `model_alias` maps to provider-specific Wabi env vars;
- secret-like prompts are still blocked before reaching Wabi;
- invalid cloud opt-in returns `REVIEW`, not an unhandled crash.

Validation:

- `python -m pytest tests\test_wabi_gateway.py -q` -> `6 passed`.
- Real smoke: `WabiGateway.ask(... provider="nvidia", allow_cloud=True,
  model_alias="super")` -> `ok=true`, provider `nvidia-nim`, output `OK`.

## Formal Code Candidates

| File | SHA256 prefix | Classification | Safe value | Direct execution |
|---|---:|---|---|---|
| `medioevo_core_v01.py` | `fd8941b2b009604c` | `CODE_INSIGHT_CANON_CANDIDATE` | agent loop with ActionDecision/Signal/State/Task/Plan/Response/CycleMetrics, EML calculation, observe/process/decide/execute/handoff cycle | `NO` |
| `medioevo_agent_core.py` | `f646b34113fb7ca3` | `CODE_INSIGHT_CANON_CANDIDATE` | compact AgentConfig/Observation/DOResult/Plan/GhostSimulation/GateDecision/AgentOutput pipeline; explicit `compute_phi_eff`, `ghostgate`, `actiongate`, `measure_residue`, `persist_handoff` | `NO` |
| `PR11.txt` | `f31664d1af3c51aa` | `CODE_AND_CLAIM_DELTA` | dense restatement of ActionGate/GhostGate/Handoff/Phi_eff/residue contract; useful as spec comparison | `NO` |
| `uno.py` | `ddcde60ce0b83767` | `BLOCKED_EXECUTION_CODE_INSIGHT` | negative requirements for host/process safety and memory pressure gates | `BLOCK` |
| `The Solution deploy_overlord.shThis.txt` | `b2241a5c87a8dd76` | `BLOCKED_EXECUTION_CODE_INSIGHT` | negative requirements for payload/network/dependency execution, plus agent orchestration cautionary patterns | `BLOCK` |

## Full Formal Signal Sweep

All 50 files in `Formal` were rescanned by metadata and text signals. This is
not a final claim review; it is a routing map for the next extraction pass.

| Bucket | Count | Meaning |
|---|---:|---|
| Text/code sources with claim signals | 36 | compare against `16_CLAIMS_REGISTER.md` before canon changes |
| Text/code sources with code/agent signals | 35 | extract contracts/tests/patterns, not whole files |
| Experiment/evidence signals | 41 | preserve provenance and link to claims before reuse |
| Binary/visual/archive extraction required | 13 | PDF/PNG/ZIP need dedicated extraction/QA |
| Blocked execution signals | 9 | use as negative tests or requirements, never execute directly |
| Secret-like signal review | 14 | mostly keyword hits plus `banananana.txt`; publish gate stays blocked until redacted review |

Highest-priority text/code sources after this sweep:

| Priority | File | Why |
|---|---|---|
| P0 | `banananana.txt` | real secret/config material; keep private and rotate/review |
| P1 | `medioevo_agent_core.py` | compact ActionGate/GhostGate/Phi_eff/residue/handoff implementation candidate |
| P1 | `medioevo_core_v01.py` | cleaner cycle contract candidate with standard-library-only imports |
| P1 | `PR11.txt` | spec-dense bridge between code and observacionista contracts |
| P1 | `report.md`, `P1R.txt`, `Completar04.txt`, `Completar07.txt` | highest claim density; require claims delta review |
| P1 | `experimento_medioevo2_datos.json`, `results_full.csv` | evidence/data lane; bind to falsifiers before claims |
| BLOCK | `uno.py`, `The Solution deploy_overlord.shThis.txt` | execution/process/network/payload risk; extract negative requirements only |

## Static Findings

`medioevo_core_v01.py`:

- classes: `ActionDecision`, `Signal`, `State`, `Task`, `Plan`, `Response`,
  `CycleMetrics`, `MedioevoAgent`;
- strong matches: `ActionGate`, `GhostGate`, `Handoff`, `Phi_eff`,
  `observador`, `agent`;
- imports are standard-library only;
- candidate extraction: typed cycle contract and handoff state, not whole-file
  import.

`medioevo_agent_core.py`:

- classes: `AgentConfig`, `Observation`, `DOResult`, `Plan`, `GhostSimulation`,
  `GateDecision`, `AgentOutput`, `MedioevoAgent`;
- strong matches: `ActionGate`, `GhostGate`, `Handoff`, `Phi_eff`, `residue`;
- candidate extraction: `compute_phi_eff`, `ghostgate`, `actiongate`,
  `measure_residue`, `persist_handoff`;
- should be compared against Wabi `ActionGate`, `SafeExecutor`,
  `RollbackStore`, `DecisionLogAdapter` and Claudio `session_cosmos`.

Blocked sources:

- `uno.py` touches process/memory/priority/shell surfaces and remains blocked
  for execution.
- `The Solution deploy_overlord...txt` contains dependency/network/payload/API
  orchestration patterns and remains blocked for execution.

## Integration Backlog

- [x] Add explicit Claudio cloud opt-in through Wabi gateway.
- [x] Verify NVIDIA real call through Claudio gateway with `super`.
- [x] Strengthen Wabi redaction for Alibaba AccessKey-style material.
- [x] Extract `AgentOutput` / `GateDecision` shape into a small contract test,
      not a production import. Evidence:
      `apps/local/wabi-sabi/tests/test_formal_contract_intake.py`.
- [x] Compare `compute_phi_eff` against `core/session_cosmos.py` and Wabi EML
      helpers; keep as research metric unless tests prove behavior. Evidence:
      `docs/intake/FORMAL_WABI_CONTRACT_COMPARISON_2026-05-13.md` and
      `test_phi_eff_and_eml_remain_bounded_research_helpers`.
- [x] Build fixture cases from `PR11.txt` for ActionGate/GhostGate/Handoff.
      Evidence: `test_pr11_fixture_cases_map_to_gate_ghost_and_handoff_contracts`
      in `apps/local/wabi-sabi/tests/test_formal_contract_intake.py`.
- [x] Keep `uno.py` and deploy-overlord material as negative test cases for
      ActionGate/SafeExecutor. Evidence:
      `test_blocked_formal_execution_sources_stay_negative_cases` blocks
      destructive text, publication/secret text, shell composition and
      `runtime/` patch targets.

## Decision

The technology has real value, but the safe path is extraction-by-contract:
tests, schemas and adapters first; no direct import of Formal runtime files, no
script execution, no autonomous cloud use, and no weight/model mutation.
