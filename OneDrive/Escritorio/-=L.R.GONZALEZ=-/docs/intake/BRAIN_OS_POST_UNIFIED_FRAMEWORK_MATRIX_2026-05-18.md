# BRAIN_OS POST Unified Framework Matrix - 2026-05-18

Status: `LOCAL_INTAKE_GOVERNANCE`

Decision: `INTEGRATE_DELTAS_BY_UNIQUENESS_AND_CONVERGENCE`

ActionGate: `APPROVE_LOCAL_DOCS_ONLY`

RuntimeImport=BLOCK

PublicationGate=BLOCK

RawAdoption=BLOCK

This matrix replaces the earlier next-step framing of selecting one isolated
`CODE_INSIGHT`. The correct closure is to integrate deltas through uniqueness,
overlap and falsifier status: what is already covered reinforces the existing
Wabi/Claudio contracts, what contradicts them becomes a falsifier, and what is
not evidenced remains in `REQUIRES_EVIDENCE`.

The parallel JSON artifact is the testable source of truth:
`docs/intake/BRAIN_OS_POST_UNIFIED_FRAMEWORK_MATRIX_2026-05-18.json`.

## Sources

| source | sha256 | intake action | gate |
|---|---|---|---|
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# 00 — LEER PRIMERO Portafolio MEDI.txt` | `C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD` | `SELECTIVE_CLAIM_EXTRACTION_ONLY` | `APPROVE_LOCAL_DOCS_ONLY` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Untitled.txt` | `F5C992E17FAE57AB6B3F43488F0017BC635C0FE84A97EF1BBD34B5A90B84DF4B` | `CODE_INSIGHT_ONLY` | `APPROVE_LOCAL_DOCS_ONLY` |

Both sources were fichados by exact path. Neither source is copied into runtime,
release staging, website copy, social copy or package output.

## Canonical Layers

| layer | role | integration posture |
|---|---|---|
| `Boundary` | Publication gate, public/private labels, claim downgrade rules. | `OVERLAP_REINFORCES_EXISTING` when it matches current policy; `BLOCK` for public/runtime escalation. |
| `Math/State` | R/Phi vocabulary, `PSIState`, `ObservationEnvelope`, calibrator patterns. | Compare to existing Wabi/Claudio helpers; no replacement without target tests. |
| `Gate` | Separate `GhostGate` planning from `ActionGate` execution. | Keep as contract vocabulary and future test fixture. |
| `Continuity` | Fingerprint, handoff, brief, and evidence-derived truth. | Continuity text must be generated from actual results, not source self-report. |
| `Falsifiers` | Benchmark `5/6`, `F1_regime_prediction`, false handoff, Lyapunov tolerance. | Preserve as negative fixtures before any runtime change. |

## Delta Matrix

| id | layer | source evidence | target lane | evidence state | action gate | integration |
|---|---|---|---|---|---|---|
| `boundary.publication_gate_and_raw_adoption` | `Boundary` | portfolio lines `5-7`, `160-165`; hash `C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD` | `docs/intake`, `VISIBILITY_MATRIX.md`, publication review docs | `CERTEZA_FROM_EXACT_PATH_FICHA_AND_EXISTING_POLICY` | `APPROVE_LOCAL_DOCS_ONLY` | `OVERLAP_REINFORCES_EXISTING` |
| `boundary.epistemic_labels` | `Boundary` | portfolio lines `29-33`; hash `C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD` | curador fichas, ActionGate docs, ObservationEnvelope-style reports | `OVERLAP_REINFORCES_EXISTING` | `APPROVE_LOCAL_DOCS_ONLY` | `OVERLAP_REINFORCES_EXISTING` |
| `boundary.overclaim_downgrade` | `Boundary` | portfolio lines `108-112`, `157`, `973-989`, `1013-1016` | claim falsification register, public copy review, research backlog | `REQUIRES_EVIDENCE` | `REVIEW` | `REQUIRES_EVIDENCE` |
| `math_state.r_phi_comparison` | `Math/State` | `Untitled.txt` lines `54-90`, `127-160`, `301-310`, `381-400`; hash `F5C992E17FAE57AB6B3F43488F0017BC635C0FE84A97EF1BBD34B5A90B84DF4B` | Wabi `geodia_math_core.py`, Claudio `rphi_budget.py`, `rphi_calibration.py` | `REQUIRES_EVIDENCE` | `REVIEW` | `REQUIRES_EVIDENCE` |
| `math_state.psi_state_observation_envelope` | `Math/State` | `Untitled.txt` lines `240-294`, `774-788` | Wabi `observation.py` and runtime state docs | `OVERLAP_REINFORCES_EXISTING` | `APPROVE_LOCAL_DOCS_ONLY` | `OVERLAP_REINFORCES_EXISTING` |
| `gate.ghostgate_actiongate_split` | `Gate` | `Untitled.txt` lines `485-540`, `721-751`, `801-802` | Claudio GhostGate planning lane, Wabi ActionGate contracts | `OVERLAP_REINFORCES_EXISTING` | `APPROVE_LOCAL_DOCS_ONLY` | `OVERLAP_REINFORCES_EXISTING` |
| `continuity.handoff_fingerprint_truth` | `Continuity` | `Untitled.txt` lines `419-469`, `806-808`, `921-923` | `SESSION_FINGERPRINT.json`, `NEXT_SESSION_BRIEF.md`, Claudio handoff docs | `FALSIFIER_OR_DEFECT_REQUIRES_EVIDENCE` | `REVIEW` | `FALSIFIER_OR_DEFECT` |
| `falsifiers.benchmark_negative_fixtures` | `Falsifiers` | `Untitled.txt` lines `615`, `923`, `935-936` | `tests/release`, Wabi tests, Claudio R/Phi backlog | `FALSIFIER_OR_DEFECT_REQUIRES_EVIDENCE` | `REVIEW` | `FALSIFIER_OR_DEFECT` |

## Claim Guardrails

| term | required status | reason |
|---|---|---|
| `PASS` | `REQUIRES_EVIDENCE` | Source self-report is not current test evidence. |
| `PROBADO` | `REQUIRES_EVIDENCE` | Strong proof language needs reviewed derivation and local tests. |
| `derivada no conjetura` | `REQUIRES_EVIDENCE` | Derivation language is not elevated without a focused evidence artifact. |
| `Benchmark 5/5 OK` | `FALSIFIER_OR_DEFECT_REQUIRES_EVIDENCE` | The observed run reported `5/6`; handoff truth must derive from actual results. |

## Integration Rules

- Portfolio POST contributes boundary rules, claim labels, falsifier posture and
  overclaim blocking.
- `Untitled.txt` contributes runtime patterns only as `CODE_INSIGHT_ONLY`; no
  class, function or benchmark result is imported into Wabi/Claudio.
- Every delta must carry exact source path, SHA256, line evidence, target lane,
  claim boundary, evidence state and ActionGate.
- Existing Wabi/Claudio overlap is `OVERLAP_REINFORCES_EXISTING`.
- Contradictions and partial runs are `FALSIFIER_OR_DEFECT`.
- Missing target-lane proof is `REQUIRES_EVIDENCE`.

## Next Gate

Use this matrix to select convergent deltas and negative fixtures. Runtime work
stays `REVIEW` until a target-lane failing test, patch, rerun and evidence
prove the change. Publication stays blocked.
