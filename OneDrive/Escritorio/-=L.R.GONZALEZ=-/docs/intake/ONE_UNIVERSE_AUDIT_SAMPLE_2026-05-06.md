# Global Curador SETO Dry Audit 2026-05-05

Status: `DRY_RUN_NO_DELETE_NO_MOVE`
Scan mode: `incremental`

This report implements a dry Curador pass over the selected roots. It records evidence for later cleanup gates; it does not approve deletion by itself.

## Artifacts

- JSON summary: `qa_artifacts\release_validation\one-universe-audit-workspace-sample-2026-05-06.json`
- CSV file manifest: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05-workspace_lrgonzalez_max5000.csv`
- WitnessLog: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\witness_log\curador_seto_witnesslog.jsonl`

## Counts

| metric | value |
|---|---:|
| `files` | 5000 |
| `generated_dirs_recorded` | 32 |
| `project_roots_detected` | 78 |
| `errors` | 0 |
| `hashed_files` | 1216 |
| `zip_or_archive_files` | 11 |
| `exact_duplicate_groups` | 53 |
| `version_review_groups` | 210 |

## Resume

| field | value |
|---|---|
| `truncated` | `True` |
| `processed_files` | `5000` |
| `max_files` | `5000` |
| `start_after_found` | `True` |
| `next_start_after` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\research_watch_state.json` |

## Root Stats

| root | exists | files | dirs | MB | hashed | hash_skipped | generated_dirs_skipped |
|---|---:|---:|---:|---:|---:|---:|---:|
| `workspace_lrgonzalez` | True | 5000 | 1110 | 276.38 | 1216 | 40 | 32 |

## Focus Stats

| focus | files | MB | hashed |
|---|---:|---:|---:|
| `psi` | 139 | 8.50 | 139 |
| `downloads` | 0 | 0.00 | 0 |
| `desktop` | 5000 | 276.38 | 1216 |
| `workspace` | 5000 | 276.38 | 1216 |
| `e_drive` | 0 | 0.00 | 0 |

## ActionGate Summary

| gate | count |
|---|---:|
| `REVIEW` | 4960 |
| `BLOCK` | 40 |

## Decision Summary

| decision | count |
|---|---:|
| `KEEP_OR_REVIEW` | 4908 |
| `KEEP_BLOCKED_BOUNDARY` | 40 |
| `CANDIDATE_DELETE_REGENERABLE_REVIEW` | 34 |
| `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | 11 |
| `CANDIDATE_DELETE_EMPTY_REVIEW` | 7 |

## Exact Duplicate Groups

| sha256 | count | duplicate MB if one kept | gate | examples |
|---|---:|---:|---|---|
| `9b5089dcde899933...` | 2 | 0.14 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\styles.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\styles.csv` |
| `9043c3f06faa9b43...` | 2 | 0.10 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\design.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\design.csv` |
| `eaa93e65d11b96a2...` | 2 | 0.06 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-037-AUTOPILOT-CHAT-MODE.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\docs\adr\ADR-037-AUTOPILOT-CHAT-MODE.md` |
| `47160ddcdbda79bb...` | 2 | 0.06 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-029-HUGGINGFACE-CHAT-UI-CLOUD-RUN.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\docs\adr\ADR-029-HUGGINGFACE-CHAT-UI-CLOUD-RUN.md` |
| `6ea44a7725d708a2...` | 2 | 0.06 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\products.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\products.csv` |
| `41976082ecae1100...` | 2 | 0.05 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\ui-reasoning.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\ui-reasoning.csv` |
| `a393558b7acc7919...` | 2 | 0.05 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\typography.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\typography.csv` |
| `ef67afdbd03f9517...` | 2 | 0.04 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\scripts\design_system.py`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\scripts\design_system.py` |
| `891d5f75a997485a...` | 2 | 0.03 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\docs\integrations\epic-sdk\epic-sdk-integration.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\docs\sdk\epic-sdk-integration.md` |
| `b8d7bc2b2f9865a1...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\_sync_all.py`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\_sync_all.py` |
| `3dd1271b04e21e30...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\PROMPT_MAESTRO_HANDOFF_2026-04-25.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\extra_psi_pre_final_v1_1\PROMPT_MAESTRO_HANDOFF_2026-04-25.md` |
| `08a5093e039f0381...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\claudio_daemon.db`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio_daemon.db` |
| `ebb565308115f955...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\charts.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\charts.csv` |
| `70a909411f1e26d9...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\mcp-bridge\test-harness.js`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\mcp-bridge\test-harness.js` |
| `1870ee048f2a2bdd...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\ux-guidelines.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\ux-guidelines.csv` |
| `47c0a454cb73bf32...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\react-performance.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\react-performance.csv` |
| `42f3cbd6297d81be...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\shared\src\mcp\types.ts`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\mcp\types.ts` |
| `594bf80e39704882...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\shared\src\mcp\session-manager.ts`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\mcp\session-manager.ts` |
| `a08ca77fcf6b6d95...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\stacks\react-native.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\stacks\react-native.csv` |
| `22b5ade511d386fd...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-035-MCP-TOOL-GROUPS.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\docs\adr\ADR-035-MCP-TOOL-GROUPS.md` |

## Large Files

| size MB | gate | decision | path |
|---:|---|---|---|
| 49.70 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\models\phi-4-mini\cpu_and_mobile\cpu-int4-rtn-block-32-acc-level-4\model.onnx` |
| 42.66 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\models\phi-4-mini\cpu_and_mobile\cpu-int4-rtn-block-32-acc-level-4\model.onnx.data` |
| 27.55 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\memory_index.db` |
| 15.11 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.chroma_db\chroma.sqlite3` |
| 10.54 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\grok-video-4d563a03-3e1b-40ec-bd3c-a80214c7ee0b.MP4` |
| 8.90 | `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\OBSERVACIONISMO_ARTEFACT_RUN_v0_2.zip` |
| 7.08 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\assets\piri\piri_reis_world_map_01.jpg` |
| 5.36 | `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\VOYNICH_MUSIC_MICRORUN_v0_8b.zip` |
| 3.73 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.chroma_db\2143d7eb-4303-47af-9cdf-d02277ab8564\data_level0.bin` |
| 3.58 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\face_landmarker.task` |
| 2.81 | `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\VOYNICH_PIRI_REAL_RUN_v0_3.zip` |
| 2.75 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Claudiocobain.png` |
| 2.37 | `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\website_deploy.zip` |
| 2.36 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\docs\reasoningbank\models\domain-expert\memory.db` |
| 2.29 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=Artistas=-\Raul Herrera\Raul HM.pdf` |
| 2.01 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_face.png` |
| 1.33 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\10e44f41-1247-4e17-9b19-d122cb12a72c-video.MP4` |
| 1.25 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=Artistas=-\Luis Rene Tren Tyr\CV LUIS RENÉ GONZÁLEZ LÓPEZ.pdf` |
| 1.24 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\chat-ui\static\chatui\omni-welcome.gif` |
| 1.08 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\screenshots\website.png` |
| 1.07 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\guidance\wasm-pkg\guidance_kernel_bg.wasm` |
| 0.98 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\images\cctask.png` |
| 0.96 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\images\subagents.png` |
| 0.94 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\images\genui.png` |
| 0.93 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Logo.png` |

## Delete Candidate Sample

| gate | decision | path |
|---|---|---|
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\.claw` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\.pytest_cache` |
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
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\cli\.claude` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\cli\bin` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\hooks\bin` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\mcp\.claude` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\.claude` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\.git` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.claude` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.claw` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.git` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.pytest_cache` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.claudio_consciousness.json` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.image_download_log.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\discord_bot.log` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\download_monitor.log` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\RC_03_TEMPORADA_9` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\CLAUDE.md` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\scripts\setups\vitest-setup-client.ts` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\routes\settings\(nav)\+page.svelte` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\stub\@reflink\reflink\index.js` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\aidefence\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\browser\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\claims\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\cli\cloud-functions\publish-registry\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\cli\src\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\cli\src\transfer\tmp.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\codex\tmp.json` |

## Boundaries

- No deletion, movement, extraction or publication was executed.
- `BLOCK` rows require private/secret/claim review and cannot be cleanup targets.
- `REVIEW` rows require ficha, canonical copy or regenerability proof before a later cleanup pass.
- The CSV manifest is the evidence base for follow-up exact-duplicate and generated-residue gates.
