# BRAIN_OS POST Selective Extraction - 2026-05-18

Status: `LOCAL_INTAKE_GOVERNANCE`

ActionGate: `APPROVE_LOCAL_DOCS_ONLY`

PublicationGate: `BLOCK`

## Sources

| source | sha256 | preflight before ficha | action |
|---|---|---|---|
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# 00 — LEER PRIMERO Portafolio MEDI.txt` | `C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD` | `NEEDS_FICHA_BEFORE_USE`, no matches | `SELECTIVE_CLAIM_EXTRACTION_ONLY` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Untitled.txt` | `F5C992E17FAE57AB6B3F43488F0017BC635C0FE84A97EF1BBD34B5A90B84DF4B` | `NEEDS_FICHA_BEFORE_USE`, name-only partial matches | `CODE_INSIGHT_ONLY` |

## Protocol

`RAW_SOURCE -> FICHA -> USEFUL_DELTA -> TARGET_LANE -> TEST/EVIDENCE -> INTEGRATED_OR_REVIEW`

Raw adoption is `BLOCK`. This pass does not move, rename, publish, import or
copy either POST source into runtime. It creates fichas, registers exact source
paths, records useful deltas and keeps public/scientific claims gated.

## Useful Deltas

Portfolio file:

- Internal/publication boundary model: `INTERNO_LOCAL`, `NO_PUBLICAR_SIN_GATE`,
  `PublicationGate: BLOCK`.
- Claim labels: `CERTEZA`, `INFERENCIA`, `INCOGNITA`, `BLOQUEO`.
- Falsifier framing for strong theory positions.
- Blocked overclaim list for consciousness, AGI, universal physics, medicine,
  secrets and publication.
- Rule to downgrade unsupported `PASS`, `PROBADO` and "derivada no conjetura"
  language to `REQUIRES_EVIDENCE` unless current local evidence exists.

Runtime prototype:

- `OSITMath` as comparison material for `apps/local/wabi-sabi/wabi_sabi/core/geodia_math_core.py`.
- `PSIState` and `ObservationEnvelope` as comparison material for
  `apps/local/wabi-sabi/wabi_sabi/core/observation.py`.
- `RCalibrator` as comparison material for
  `packages/open-dev/claudio-agent-runtime/claudio_agent_runtime/rphi_budget.py`
  and `rphi_calibration.py`.
- `GhostGate` and `Handoff` as comparison material for ActionGate/handoff docs,
  not as runtime imports.
- Benchmark evidence: raw audit run produced `SCORE: 5/6`; `F1_regime_prediction`
  failed; the handoff still claimed `Benchmark 5/5 OK`; stable Lyapunov output
  printed `lambda=0.0000 -> INESTABLE`, which needs tolerance handling before use.

## Rejected Material

- Whole-file adoption or vendoring into Wabi-Sabi, Claudio or packages.
- Publication copy, website copy, Gumroad copy, social posts or public claims.
- Claims that OSIT proves consciousness, AGI, universal physics, medicine or
  subjective experience.
- Secret, credential, account, private-canon or raw personal context handling.
- Any cleanup/move/delete action against the POST folder.

## Evidence

- `python tools\release\curador_preflight.py --path <portfolio> --path <untitled> --json`
  before fichas: both sources returned `NEEDS_FICHA_BEFORE_USE`; `Untitled.txt`
  had only name-level partial matches.
- The same exact-path preflight after registration returned `registered=true`
  and `partial_match_only=false` for both sources.
- `Get-FileHash -Algorithm SHA256 <portfolio>,<untitled>` produced the hashes
  listed above.
- `PYTHONIOENCODING=utf-8 python <Untitled.txt>` produced `SCORE: 5/6`,
  failing `F1_regime_prediction`, and exposed the false `Benchmark 5/5 OK`
  handoff statement.
- `python -m pytest tests\release\test_curador_preflight_selective_extraction.py -q`:
  `3 passed`.
- `python -m pytest apps\local\wabi-sabi\tests\test_formal_contract_intake.py -q`:
  `6 passed`.
- Focal scans over the new intake docs and `docs\intake\curador_fichas\brain_os_post`
  returned `count_reported=0`.
- Broad `python tools\release\scan_secrets.py --path docs\intake --json`
  returned one pre-existing finding in
  `docs/intake/FORMAL_SECRET_PROVIDER_INTAKE_2026-05-08.md`, outside this pass.
- Runtime raw-copy check over `runtime`, `apps` and `packages` found no match
  for the two new source hashes or source titles outside docs.

## Artifacts

- `docs/intake/BRAIN_OS_POST_CLAIMS_DELTA_2026-05-18.md`
- `docs/intake/BRAIN_OS_POST_CODE_INSIGHTS_2026-05-18.md`
- `docs/intake/BRAIN_OS_POST_UNIFIED_FRAMEWORK_MATRIX_2026-05-18.md`
- `docs/intake/BRAIN_OS_POST_UNIFIED_FRAMEWORK_MATRIX_2026-05-18.json`
- `docs/intake/curador_fichas/brain_os_post/2026-05-18_portafolio_medi.md`
- `docs/intake/curador_fichas/brain_os_post/2026-05-18_osit_epistemic_engine.md`

## Next Gate

ActionGate remains `REVIEW` for any future runtime implementation. The next
step is not to choose one isolated `CODE_INSIGHT`; it is to use the unified
matrix to integrate deltas by uniqueness/convergence, keep contradictions as
falsifiers and add target-lane tests before changing runtime behavior.
