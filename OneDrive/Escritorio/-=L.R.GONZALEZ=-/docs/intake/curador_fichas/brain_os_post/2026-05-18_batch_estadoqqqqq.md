# Ficha Curador - BRAIN_OS POST Batch - estadoqqqqq_post

Status: `FICHADO_BATCH_SELECTIVE_EXTRACTION`

ActionGate: `APPROVE_LOCAL_DOCS_ONLY`

PublicationGate: `BLOCK`

RuntimeImport: `BLOCK`

RawAdoption: `BLOCK`

## Source

| field | value |
|---|---|
| path | `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\ESTADOqqqqq.txt` |
| kind | `.txt` |
| sha256 | `4744D5E3947591D8B5D7D53A9B284D4B0EFC13ECE0B3239C07F40FE53982E473` |
| size_bytes | `7941` |
| classification | `POST_BATCH_META_REVIEW_SOURCE` |
| lane | `continuity` |
| intake_action | `CURATED_META_REVIEW_ONLY` |
| target_lane | `batch intake decisions; deduplication log; next-session handoff` |
| action_gate | `APPROVE_LOCAL_DOCS_ONLY` |
| publication_gate | `BLOCK` |
| runtime_import | `BLOCK` |
| raw_adoption | `BLOCK` |
| line_count | `146` |
| encoding | `utf-8-sig` |

## Useful Deltas

- Names which POST docs are direct, cleanup-needed or dangerous without demotion.
- Reinforces ObservationEnvelope, Handoff and GhostGate as existing contracts.

## Rejected Material

- Using the meta-review as a substitute for fichas.
- Adopting dangerous/overclaim sources without demotion.

## Claim Boundary

`META_REVIEW_GUIDANCE_ONLY`

Strong terms are not promoted by this ficha. Publication, runtime import and raw adoption stay blocked.

## Term Signals

- `Benchmark`: count `1`, first lines `[37]`
- `GhostGate`: count `1`, first lines `[37]`
- `Handoff`: count `2`, first lines `[37, 144]`
- `ObservationEnvelope`: count `1`, first lines `[37]`
- `Phi`: count `1`, first lines `[18]`
- `Phi_eff`: count `1`, first lines `[18]`
- `consciencia`: count `6`, first lines `[15, 35, 89, 93, 102, 146]`
- `fisica`: count `1`, first lines `[57]`
- `física`: count `9`, first lines `[11, 15, 60, 71, 95, 101, 115, 141]`

## ZIP Internal Entries

- Not a ZIP container.

## Evidence

- Hash computed from exact source path on 2026-05-18.
- Evidence hint: Useful for prioritization and duplicate prevention.
- Matrix: `docs/intake/BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.json`.

## Decision

`DOCUMENTED_FOR_SELECTIVE_EXTRACTION_ONLY`.

No source was moved, extracted into runtime, published or imported.
