# Formal Duplicates Review - 2026-05-08

## Resultado

CERTEZA:
- Latest recheck observed `50` files in `Formal`; earlier pass counted `48`
  after adding `banananana.txt`.
- Comparison targets contained `643` files across:
  - `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-`
  - `MEDIOEVO_OBSERVACIONISMO_MASTER`
  - `runtime/cerebro_master_index`
- Exact SHA256 duplicates from `Formal` into those targets: `0`.

INFERENCIA:
- There may still be semantic overlap with PSI/master documents, but hash evidence does not support deletion or mirror cleanup.
- The apparent overlap is conceptual and iterative, not physical duplication.

INCOGNITA:
- PDF/PNG/ZIP content was not page-rendered or unpacked in this pass.
- Text similarity was not used as a delete signal; it can only nominate review.

## Wabi/Sabi Context

Wabi/Sabi CEREBRO checks were run as current context, not as a `Formal` delete authority:

| Check | Current result | Relevance to `Formal` |
|---|---:|---|
| `cerebro-audit` | `652` files, `294203` lines, `119` variant groups | Confirms live CEREBRO index has changed since prior pass. |
| `variant-compare` | `118` variant groups | These are internal CEREBRO/PSI variants, not `Formal` duplicates. |
| `duplicate-migration-plan` | `dry_run_only=true`, `source_mutations=0` | No cleanup executed. |
| `cerebro-merge-review` | `auto_merge_actions=0`, `source_mutations=0` | No merge executed. |

## Name-Level Observations

Only one weak name/stem overlap was seen during planning: `Untitled.txt` has a name-level match elsewhere. This is not delete evidence because:

- SHA256 differs.
- File title is non-semantic.
- The content may contain unique prompt/security framing.

## Cleanup Position

| Lane | Decision | Reason |
|---|---|---|
| Exact duplicates | `NONE_FOUND` | No matching SHA256 against PSI/master/runtime index. |
| Semantic variants | `REVIEW_REQUIRED` | Similarity can change meaning in formulas, gates and claims. |
| Binary/media/archive | `REVIEW_EXTRACTION_REQUIRED` | Need render or quarantined archive intake first. |
| Execution snippets | `BLOCKED_EXECUTION` | Keep for evidence; do not run or delete before extracting safe patterns. |

## Next Evidence Required

- Build excerpt-level comparison for `report.md`, `Auto.txt`, `BIBLIA_MEDIOEVO_Canon_Unificado.pdf`, `OI_P6R_paper_v0_1.md` and `paper_observacionismo_inverso.md` against master docs `00-22`.
- Render or extract the PDF before deciding if it supersedes text sources.
- Quarantine-unpack ZIPs into a review lane before deciding if their payload is duplicate, code insight or archive-only.

## Decision

No `DELETE_CANDIDATES.md` entry was created for `Formal` in this pass. Third-pass deletion is blocked until a file has canonical destination or discard reason, full SHA256, no unique insight/code/evidence, and cleanup gate approval.

## Secret/config delta

`banananana.txt` is not a duplicate review candidate. It is a provider credential/config source and is classified separately as `PRIVATE_SECRET_CONFIG`.

| File | SHA256 | Duplicate decision | Cleanup decision |
|---|---|---|---|
| `banananana.txt` | `2FA50B657189AE22D371CFECADC25857770914235CCD3DC2233DFA6EF311D5B2` | `NOT_CANON_DUPLICATE` | `KEEP_PRIVATE_REDACTED_EVIDENCE`; no deletion without secret rotation/owner review |
