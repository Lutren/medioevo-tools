# Global Curador SETO Dry Audit 2026-05-05

Status: `DRY_RUN_NO_DELETE_NO_MOVE`
Scan mode: `incremental`

This report implements a dry Curador pass over the selected roots. It records evidence for later cleanup gates; it does not approve deletion by itself.

## Artifacts

- JSON summary: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-seto-audit-2026-05-05-workspace_lrgonzalez_max500_resume7d57d3e8fd.json`
- CSV file manifest: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05-workspace_lrgonzalez_max500_resume7d57d3e8fd.csv`
- WitnessLog: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\witness_log\curador_seto_witnesslog.jsonl`

## Counts

| metric | value |
|---|---:|
| `files` | 500 |
| `generated_dirs_recorded` | 10 |
| `project_roots_detected` | 9 |
| `errors` | 0 |
| `hashed_files` | 137 |
| `zip_or_archive_files` | 0 |
| `exact_duplicate_groups` | 1 |
| `version_review_groups` | 22 |

## Resume

| field | value |
|---|---|
| `truncated` | `True` |
| `processed_files` | `500` |
| `max_files` | `500` |
| `start_after_found` | `True` |
| `next_start_after` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude\checkpoints\1754319970.json` |

## Root Stats

| root | exists | files | dirs | MB | hashed | hash_skipped | generated_dirs_skipped |
|---|---:|---:|---:|---:|---:|---:|---:|
| `workspace_lrgonzalez` | True | 500 | 516 | 3.71 | 137 | 3 | 10 |

## Focus Stats

| focus | files | MB | hashed |
|---|---:|---:|---:|
| `psi` | 0 | 0.00 | 0 |
| `downloads` | 0 | 0.00 | 0 |
| `desktop` | 500 | 3.71 | 137 |
| `workspace` | 500 | 3.71 | 137 |
| `e_drive` | 0 | 0.00 | 0 |

## ActionGate Summary

| gate | count |
|---|---:|
| `REVIEW` | 497 |
| `BLOCK` | 3 |

## Decision Summary

| decision | count |
|---|---:|
| `KEEP_OR_REVIEW` | 495 |
| `KEEP_BLOCKED_BOUNDARY` | 3 |
| `CANDIDATE_DELETE_EMPTY_REVIEW` | 2 |

## Exact Duplicate Groups

| sha256 | count | duplicate MB if one kept | gate | examples |
|---|---:|---:|---|---|
| `637c6acf13b4ae15...` | 2 | 0.00 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\static\chatui\favicon.svg`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\static\chatui\icon.svg` |

## Large Files

| size MB | gate | decision | path |
|---:|---|---|---|
| 0.60 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\package-lock.json` |
| 0.42 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\static\huggingchat\tools-thumbnail.png` |
| 0.27 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\pnpm-lock.yaml` |
| 0.23 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\static\huggingchat\omni-welcome.gif` |
| 0.20 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\static\huggingchat\assistants-thumbnail.png` |
| 0.11 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\CHANGELOG.md` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\static\huggingchat\castle-example.jpg` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\static\chatui\omni-welcome.png` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\tests\context-persistence-hook.test.mjs` |
| 0.03 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\tests\rvf-capability-verify.test.ts` |
| 0.03 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\scripts\verify-appliance.sh` |
| 0.03 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\static\chatui\omni-welcome.gif` |
| 0.03 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude\agents\consensus\quorum-manager.md` |
| 0.03 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude\agents\consensus\performance-benchmarker.md` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude\agents\consensus\crdt-synchronizer.md` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude\agents\reasoning\agent.md` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude\agents\optimization\topology-optimizer.md` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\routes\conversation\[id]\+server.ts` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\utils\parseIncompleteMarkdown.ts` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\tests\rvf-embeddings.test.ts` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\tests\rvf-backend.test.ts` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude\agents\optimization\benchmark-suite.md` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude\agents\consensus\security-manager.md` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude\agents\optimization\performance-monitor.md` |
| 0.02 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude\agents\optimization\resource-allocator.md` |

## Delete Candidate Sample

| gate | decision | path |
|---|---|---|
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\.pytest_cache` |
| `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\releases` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.git` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\.git` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\humanizer\.git` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\.git` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\bin` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\bin` |
| `REVIEW` | `REVIEW_ENV_DIR_SECRET_AND_REGENERABILITY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\chart\env` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\bin` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\routes\settings\(nav)\+page.svelte` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\stub\@reflink\reflink\index.js` |

## Boundaries

- No deletion, movement, extraction or publication was executed.
- `BLOCK` rows require private/secret/claim review and cannot be cleanup targets.
- `REVIEW` rows require ficha, canonical copy or regenerability proof before a later cleanup pass.
- The CSV manifest is the evidence base for follow-up exact-duplicate and generated-residue gates.
