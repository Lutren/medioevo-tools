# Ficha Curador - BRAIN_OS POST Portafolio MEDI

Status: `FICHADO_SELECTIVE_EXTRACTION`

ActionGate: `APPROVE_LOCAL_DOCS_ONLY`

PublicationGate: `BLOCK`

## Source

| field | value |
|---|---|
| path | `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# 00 — LEER PRIMERO Portafolio MEDI.txt` |
| kind | `RAW_SOURCE` |
| sha256 | `C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD` |
| size_bytes | `37381` |
| preflight_before_ficha | `NEEDS_FICHA_BEFORE_USE` |
| classification | `INTERNAL_CANON_PORTFOLIO_SOURCE` |
| intake_action | `SELECTIVE_CLAIM_EXTRACTION_ONLY` |
| target_lane | `docs/intake`, `claim-boundary docs`, `publication review` |
| raw_adoption | `BLOCK` |

## Useful Deltas

- Internal/public boundary model: local-only, no public action without gate.
- Claim labels: `CERTEZA`, `INFERENCIA`, `INCOGNITA`, `BLOQUEO`.
- Falsifier-first framing for strong claims.
- Blocked overclaim list for consciousness, AGI, universal physics, medicine,
  secrets and publication.
- Downgrade rule for unsupported `PASS`, `PROBADO` and derivation language.

## Rejected Material

- Full-source adoption.
- Public copy or publication workflow.
- Strong scientific, consciousness, AGI or medical claims as fact.
- Secret, credential, payment, push, deploy or social-media action.
- Any move/delete/rename of the source.

## Claim Boundary

- `PublicationGate: BLOCK`.
- `PASS`: `SOURCE_SELF_REPORT` until verified by current test/scan.
- `PROBADO`: `REQUIRES_EVIDENCE` unless backed by primary-source review and
  current local evidence.
- `derivada no conjetura`: `REQUIRES_EVIDENCE` unless a reviewed derivation and
  focused test exist.
- Physics/consciousness/AGI/medicine overclaims: `blocked_claim`.

## Evidence

- Exact-path preflight before ficha returned `NEEDS_FICHA_BEFORE_USE`.
- Hash evidence: `Get-FileHash -Algorithm SHA256`.
- Source line anchors recorded in
  `docs/intake/BRAIN_OS_POST_CLAIMS_DELTA_2026-05-18.md`.

## Tests

- Exact-path preflight after registration: `registered=true`,
  `partial_match_only=false`.
- Focused preflight template test:
  `python -m pytest tests\release\test_curador_preflight_selective_extraction.py -q`
  -> `3 passed`.
- Focused secret scans over new intake docs/fichas: `count_reported=0`.
- Broad `docs/intake` secret scan has one pre-existing unrelated finding in
  `FORMAL_SECRET_PROVIDER_INTAKE_2026-05-08.md`.

## Decision

`INTEGRATED_AS_BOUNDARY_DOCS_ONLY`.

No raw source copied to runtime, release staging or public docs.
