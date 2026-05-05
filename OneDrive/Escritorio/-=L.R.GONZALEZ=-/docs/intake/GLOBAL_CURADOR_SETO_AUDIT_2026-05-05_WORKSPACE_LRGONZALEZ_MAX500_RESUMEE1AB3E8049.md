# Global Curador SETO Dry Audit 2026-05-05

Status: `DRY_RUN_NO_DELETE_NO_MOVE`
Scan mode: `incremental`

This report implements a dry Curador pass over the selected roots. It records evidence for later cleanup gates; it does not approve deletion by itself.

## Artifacts

- JSON summary: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-seto-audit-2026-05-05-workspace_lrgonzalez_max500_resumee1ab3e8049.json`
- CSV file manifest: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05-workspace_lrgonzalez_max500_resumee1ab3e8049.csv`
- WitnessLog: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\witness_log\curador_seto_witnesslog.jsonl`

## Counts

| metric | value |
|---|---:|
| `files` | 500 |
| `generated_dirs_recorded` | 20 |
| `project_roots_detected` | 37 |
| `errors` | 0 |
| `hashed_files` | 25 |
| `zip_or_archive_files` | 0 |
| `exact_duplicate_groups` | 0 |
| `version_review_groups` | 24 |

## Resume

| field | value |
|---|---|
| `truncated` | `True` |
| `processed_files` | `500` |
| `max_files` | `500` |
| `start_after_found` | `True` |
| `next_start_after` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\claims\vitest.config.ts` |

## Root Stats

| root | exists | files | dirs | MB | hashed | hash_skipped | generated_dirs_skipped |
|---|---:|---:|---:|---:|---:|---:|---:|
| `workspace_lrgonzalez` | True | 500 | 687 | 6.95 | 25 | 0 | 20 |

## Focus Stats

| focus | files | MB | hashed |
|---|---:|---:|---:|
| `psi` | 0 | 0.00 | 0 |
| `downloads` | 0 | 0.00 | 0 |
| `desktop` | 500 | 6.95 | 25 |
| `workspace` | 500 | 6.95 | 25 |
| `e_drive` | 0 | 0.00 | 0 |

## ActionGate Summary

| gate | count |
|---|---:|
| `REVIEW` | 500 |

## Decision Summary

| decision | count |
|---|---:|
| `KEEP_OR_REVIEW` | 495 |
| `CANDIDATE_DELETE_REGENERABLE_REVIEW` | 5 |

## Exact Duplicate Groups

| sha256 | count | duplicate MB if one kept | gate | examples |
|---|---:|---:|---|---|

## Large Files

| size MB | gate | decision | path |
|---:|---|---|---|
| 0.85 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\package-lock.json` |
| 0.41 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\pnpm-lock.yaml` |
| 0.09 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\swarm\coordinator.ts` |
| 0.09 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\mcp\mcp-server.js` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\verification\rollback.ts` |
| 0.05 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\resources\resource-manager.ts` |
| 0.05 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\neural\NeuralDomainMapper.ts` |
| 0.05 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\enterprise\audit-manager.ts` |
| 0.05 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\swarm\sparc-executor.ts` |
| 0.05 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\core\orchestrator.ts` |
| 0.05 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\mcp\claude-flow-tools.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\verification\security.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\enterprise\security-manager.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\enterprise\analytics-manager.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\verification\alert-manager.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\verification\telemetry.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\enterprise\cloud-manager.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\hive-mind\core\Memory.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\enterprise\deployment-manager.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\browser\src\mcp-tools\browser-tools.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\swarm\advanced-orchestrator.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\verification\hooks.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\swarm\memory.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\core\config.ts` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\verification\tests\e2e\verification-pipeline.test.ts` |

## Delete Candidate Sample

| gate | decision | path |
|---|---|---|
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\.claw` |
| `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\releases` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.claude` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.git` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\.claude` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\.git` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\humanizer\.git` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\.claude` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\.git` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\bin` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\bin` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\.claude` |
| `REVIEW` | `REVIEW_ENV_DIR_SECRET_AND_REGENERABILITY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\chart\env` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\bin` |
| `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\docs\releases` |
| `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\docs\reports\releases` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\examples\litellm\.claude` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\cli\simple-commands\init\.claude` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\templates\claude-optimized\.claude` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\aidefence\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\browser\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\claims\tmp.json` |

## Boundaries

- No deletion, movement, extraction or publication was executed.
- `BLOCK` rows require private/secret/claim review and cannot be cleanup targets.
- `REVIEW` rows require ficha, canonical copy or regenerability proof before a later cleanup pass.
- The CSV manifest is the evidence base for follow-up exact-duplicate and generated-residue gates.
