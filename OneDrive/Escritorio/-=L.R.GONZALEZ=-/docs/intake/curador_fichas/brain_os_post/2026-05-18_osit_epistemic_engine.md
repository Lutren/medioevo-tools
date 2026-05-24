# Ficha Curador - BRAIN_OS POST OSIT Epistemic Engine

Status: `FICHADO_SELECTIVE_EXTRACTION`

ActionGate: `APPROVE_LOCAL_DOCS_ONLY`

PublicationGate: `BLOCK`

RuntimeImport: `BLOCK`

## Source

| field | value |
|---|---|
| path | `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Untitled.txt` |
| kind | `RAW_SOURCE_CODE_PROTOTYPE` |
| sha256 | `F5C992E17FAE57AB6B3F43488F0017BC635C0FE84A97EF1BBD34B5A90B84DF4B` |
| size_bytes | `35827` |
| preflight_before_ficha | `NEEDS_FICHA_BEFORE_USE` with name-only partial matches |
| classification | `OSIT_RUNTIME_PROTOTYPE_SOURCE` |
| intake_action | `CODE_INSIGHT_ONLY` |
| target_lane | `docs/intake`, Wabi-Sabi comparison docs, Claudio R/Phi backlog |
| raw_adoption | `BLOCK` |

## Useful Deltas

- `OSITMath` comparison against tested Wabi `geodia_math_core.py`.
- `PSIState` and `ObservationEnvelope` vocabulary comparison.
- `RCalibrator` comparison against Claudio `rphi_budget.py` and
  `rphi_calibration.py`.
- `GhostGate` as pre-action simulation vocabulary, separate from ActionGate.
- `Handoff` fields as continuity vocabulary.
- Benchmark defects as negative tests/falsifiers.

## Rejected Material

- Full-source import.
- Replacing current Wabi/Claudio runtime modules.
- Claiming benchmark pass or runtime readiness.
- Public packaging or release.
- Any move/delete/rename of the source.

## Claim Boundary

- Prototype claims are `CODE_INSIGHT` or `REQUIRES_EVIDENCE`.
- Benchmark status is `FAILED_PARTIAL`: audit run produced `5/6`.
- Handoff claim `Benchmark 5/5 OK` is rejected as false for this source.
- Future runtime use remains `REVIEW` until target-lane tests pass.

## Evidence

- Exact-path preflight before ficha returned `NEEDS_FICHA_BEFORE_USE`.
- Hash evidence: `Get-FileHash -Algorithm SHA256`.
- Static source anchors and audit-run defects are recorded in
  `docs/intake/BRAIN_OS_POST_CODE_INSIGHTS_2026-05-18.md`.
- Audit command: `PYTHONIOENCODING=utf-8 python <source>`.

## Tests

- Exact-path preflight after registration: `registered=true`,
  `partial_match_only=false`.
- Focused preflight template test:
  `python -m pytest tests\release\test_curador_preflight_selective_extraction.py -q`
  -> `3 passed`.
- Existing Wabi formal-contract intake guard:
  `python -m pytest apps\local\wabi-sabi\tests\test_formal_contract_intake.py -q`
  -> `6 passed`.
- Focused secret scans over new intake docs/fichas: `count_reported=0`.
- Broad `docs/intake` secret scan has one pre-existing unrelated finding in
  `FORMAL_SECRET_PROVIDER_INTAKE_2026-05-08.md`.

## Decision

`INTEGRATED_AS_CODE_INSIGHT_DOCS_ONLY`.

No raw source copied to runtime, release staging or public docs.
