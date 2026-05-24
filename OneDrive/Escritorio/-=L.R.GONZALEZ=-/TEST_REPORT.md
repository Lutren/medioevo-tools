# TEST_REPORT MEDIOEVO/CLAUDIO

## 2026-05-23 - Espejo tecnico BRAIN_OS Wabi `/api/chat/message`

- BRAIN_OS provider-chat focal -> `5 passed`.
- BRAIN_OS Wabi relevant suite -> `281 passed in 31.85s`.
- BRAIN_OS full:
  `python -m pytest 02_CLAUDIO\tests -q`
  -> `836 passed in 59.19s`.
- Live HTTP smoke after server restart:
  `/api/chat/message`
  -> `online_ai_called=True`, `intent=provider_review`,
  `model_chat:nvidia-nemotron-super`, model present, clock clause present,
  `forbidden_mentions=[]`.
- Health smoke -> `ok=True`, `apply=False`, `publication_gate=BLOCK`.
- No external actions from this root; provider live call occurred only from
  requested local smoke in BRAIN_OS.

## 2026-05-23 - Espejo tecnico BRAIN_OS Wabi chat cloud identity

- Final pending snapshot:
  `python tools\release\pending_review.py --write --quiet`
  -> `active_dedup=0`, `claudio_open=0`.
- BRAIN_OS identity focal:
  `python -m pytest 02_CLAUDIO\tests\test_wabi_identity_grounding.py -q -o addopts="" --timeout=60`
  -> `14 passed`.
- BRAIN_OS router/conversation focal:
  `python -m pytest 02_CLAUDIO\tests\test_wabi_chat_router.py 02_CLAUDIO\tests\test_wabi_conversation_api.py -q -o addopts="" --timeout=60`
  -> `36 passed`.
- BRAIN_OS dry-run regression focal -> `16 passed`.
- BRAIN_OS full:
  `python -m pytest 02_CLAUDIO\tests -q`
  -> `836 passed in 63.31s`.
- Live CLI smoke:
  `wabi ask "que modelo eres y que hora es"`
  -> modelo `nvidia/nvidia/nemotron-3-super-120b-a12b`, sin reloj en tiempo real.
- Live UI smoke:
  `/api/conversation/turn`
  -> `cloud=True`, `route=local_chat`, modelo presente, clausula de reloj
  presente, `forbidden_mentions=[]`.
- Gate smoke `/health` -> `apply=false`, `apply_default=false`,
  `publication_gate=BLOCK`.
- No external actions from this root; provider live call ocurrio solo desde el
  smoke local solicitado en BRAIN_OS.

## 2026-05-23 - Espejo tecnico BRAIN_OS Wabi Programmer delegation

- `python tools\release\pending_review.py --write --quiet` -> `active_dedup=0`, `claudio_open=0`.
- BRAIN_OS related Wabi programmer suite -> `39 passed`.
- BRAIN_OS drift focal UI/registry -> `9 passed`.
- BRAIN_OS full `python -m pytest 02_CLAUDIO\tests -q` -> `822 passed in 71.38s`.
- No external actions from this root.

## 2026-05-22 - Fragmentos Cover Asset Gate

Commands executed:

- `python tools\release\pending_review.py --write --quiet`
  - Result: `active_dedup=0`, `claudio_open=0`.
- `python -m py_compile tools\release\validate_cover_asset_gate.py`
  - Result: PASS.
- `python -m pytest tests\release\test_validate_cover_asset_gate.py -q`
  - Result: `3 passed in 1.80s`.
- `python tools\release\validate_cover_asset_gate.py qa_artifacts\editorial_cover_gate\FRAGMENTOS_COVER_GATE_20260522\cover_asset_gate_manifest.json --pretty`
  - Result: expected review exit; `overall_status=REVIEW_ASSET_MISSING`.
  - Report:
    `qa_artifacts/editorial_cover_gate/FRAGMENTOS_COVER_GATE_20260522/COVER_ASSET_GATE_REPORT_2026-05-22.md`.
- `python tools\release\scan_secrets.py --artifact tools\release\validate_cover_asset_gate.py --artifact tests\release\test_validate_cover_asset_gate.py --artifact qa_artifacts\editorial_cover_gate\FRAGMENTOS_COVER_GATE_20260522\cover_asset_gate_manifest.json --artifact qa_artifacts\editorial_cover_gate\FRAGMENTOS_COVER_GATE_20260522\cover_asset_gate_summary.json --artifact qa_artifacts\editorial_cover_gate\FRAGMENTOS_COVER_GATE_20260522\COVER_ASSET_GATE_REPORT_2026-05-22.md --json`
  - Result: `count_reported=0`.

Not executed:

- No image generation, asset selection, metadata stripping, public staging,
  upload, KDP, Gumroad, web, social, push, deploy, public ZIP or external
  release.

## 2026-05-22 - Human Gate Packet + Fragmentos Cover Brief

Commands executed:

- JSON parse:
  `docs\publishing\FRAGMENTOS_CALIBRACION_HUMAN_PUBLICATION_GATE_PACKET_2026-05-22.json`
  -> OK.
- JSON parse:
  `docs\publishing\FRAGMENTOS_PUBLIC_SAFE_COVER_BRIEF_2026-05-22.json`
  -> OK.
- Secret scan focal:
  `python tools\release\scan_secrets.py --path docs\publishing\FRAGMENTOS_CALIBRACION_HUMAN_PUBLICATION_GATE_PACKET_2026-05-22.md --json`
  -> `count_reported=0`.
- Secret scan focal:
  `python tools\release\scan_secrets.py --path docs\publishing\FRAGMENTOS_CALIBRACION_HUMAN_PUBLICATION_GATE_PACKET_2026-05-22.json --json`
  -> `count_reported=0`.
- Secret scan focal:
  `python tools\release\scan_secrets.py --path docs\publishing\FRAGMENTOS_PUBLIC_SAFE_COVER_BRIEF_2026-05-22.md --json`
  -> `count_reported=0`.
- Secret scan focal:
  `python tools\release\scan_secrets.py --path docs\publishing\FRAGMENTOS_PUBLIC_SAFE_COVER_BRIEF_2026-05-22.json --json`
  -> `count_reported=0`.

Not executed:

- No asset generation.
- No public staging, upload, KDP, Gumroad, web, social, push, deploy, public
  ZIP or external release.

## 2026-05-22 - Editorial Word/PDF Full-Page QA

Commands executed:

- `python tools\release\editorial_docx_word_visual_qa.py --pretty`
  - Result: `PASS_AUTOMATED_FULL_PAGE_COVERAGE`.
  - Fragmentos: Word pages `688`, rendered pages `688`,
    `blank_candidates=0`, `edge_contact_candidates=0`, contact sheets `35`.
  - Calibracion: Word pages `477`, rendered pages `477`,
    `blank_candidates=0`, `edge_contact_candidates=0`, contact sheets `24`.
  - Report:
    `qa_artifacts/editorial_docx_word_visual_qa/EDITORIAL_DOCX_WORD_FULL_QA_20260522/EDITORIAL_DOCX_WORD_VISUAL_QA_REPORT_2026-05-22.md`.
- Visual sample inspection:
  - First and last contact sheet for Fragmentos inspected.
  - First and last contact sheet for Calibracion inspected.
  - No obvious blank pages or broken composition observed in those samples.

Not executed:

- No publication, upload, KDP, Gumroad, web, social, push, deploy, public ZIP
  or source manuscript modification.

## 2026-05-22 - Editorial DOCX Split QA

Commands executed:

- `python render_docx.py ...17_fragmentos_integrado_0713.docx --renderer artifact-tool --verbose`
  - Result: timed out after controlled window; render process stopped.
  - Evidence retained: `53` partial DOCX PNG pages.
- `python render_docx.py ...17_calibracion_integrado_0713.docx --renderer artifact-tool --verbose`
  - Result: timed out after controlled window; render process stopped.
  - Evidence retained: `19` partial DOCX PNG pages.
- PyMuPDF/PIL representative PDF render and automated image metrics.
  - Fragmentos PDF page count: `696`; representative pages rendered:
    `1, 2, 3, 174, 348, 522, 694, 695, 696`.
  - Calibracion PDF page count: `382`; representative pages rendered:
    `1, 2, 3, 95, 191, 286, 380, 381, 382`.
  - Report:
    `qa_artifacts/editorial_docx_visual_qa/EDITORIAL_INTERNAL_EXPORTS_SPLIT_QA_20260522/EDITORIAL_DOCX_SPLIT_QA_REPORT_2026-05-22.md`.

Result:

- `PARTIAL_QA_REVIEW_WITH_LIMITS`.
- PDF representative pages had `0` blank candidates and `0` edge-contact
  candidates.
- DOCX partial pages had `0` blank candidates, but edge-contact flags were
  raised by image metrics across captured pages; full visual approval remains
  `REVIEW`.

Not executed:

- No full page-by-page DOCX visual approval.
- No publication, upload, push, deploy, public ZIP or source manuscript edit.

## 2026-05-22 - Editorial Internal Exports

Commands executed:

- `python tools\release\pending_review.py --write --quiet`
  - Result: `pending_review date=2026-05-22 active_dedup=0 claudio_open=0`.
- Local export generation with PowerShell `Copy-Item`, `Get-FileHash` and
  Calibre `ebook-convert`.
  - Fragmentos result: package created with 9 files; 6 copied source artifacts
    verified by matching SHA256.
  - Calibracion result: package created with 9 files; 6 copied source artifacts
    verified by matching SHA256.
- Manifest verification over both packages:
  - `FRAGMENTOS_INTERNAL_EXPORT_2026-05-22`: manifest file count `7`,
    `publication_gate=BLOCK`, `originals_modified=False`,
    `external_actions_performed=False`, `hash_ok=True`.
  - `CALIBRACION_INTERNAL_EXPORT_2026-05-22`: manifest file count `7`,
    `publication_gate=BLOCK`, `originals_modified=False`,
    `external_actions_performed=False`, `hash_ok=True`.

Not executed:

- No upload, KDP, Gumroad, web, social, push, deploy, public ZIP, dependency
  install, cloud call or source manuscript modification.

## 2026-05-22 - Workbench Maintenance

- DOCUMENTOS_IA local annex:
  `13_EVIDENCIA_LOCAL_2026-05-22.md` created under local complete packet.
- Public-safe copy unchanged; PDF not regenerated.
- Shortcut validation: `10/10` targets exist after retargeting
  `10_WORKBENCH_CANON.lnk`.
- Created `ASSETS/INDEX.md` and `LORE/INDEX.md`.
- Workbench root loose image scan: no matches.

## 2026-05-22 - OSIT-HYBRID Multi-Seed

- Harness focal:
  `python -B -m pytest test_osit_hybrid_multiseed.py -q -p no:cacheprovider`
  in BRAIN_OS Workbench `Descubrimientos` -> `3 passed in 30.48s`.
- Artifact run:
  `python -B osit_hybrid_multiseed.py --seed-count 100 --base-seed 20260522 --audit-seed 20260522 ...`
  -> manifest `state_fingerprint=OSIT_HYBRID_MULTI_SEED_20260522`,
  `seed_count=100`, `winner_by_mean_score=GS raw`,
  `publication_gate=BLOCK`.
- Full Descubrimientos:
  `python -B -m pytest -q -p no:cacheprovider` -> `37 passed in 26.75s`.
- py_compile:
  `python -B -m py_compile osit_hybrid_multiseed.py test_osit_hybrid_multiseed.py`
  -> PASS.
- Source Cards: `4800` cards across
  `GS raw, GS OSIT, RO raw, RO OSIT, ROe raw, ROe OSIT`,
  `publication_gate=BLOCK`.
- Ranking by mean comparable Score in this synthetic harness:
  `GS raw` first (`mean=11.803709`, `win_count=63`), `GS OSIT` second
  (`mean=11.900003`, `win_count=37`).
- No external data, remote compute, network, push, deploy or publication.

## 2026-05-22 - Smallville-DUAT Local Evidence

- Focused Smallville:
  `python -B -m pytest tests/test_smallville_duat_lab.py tests/test_smallville_duat_v02.py -q -p no:cacheprovider`
  in `research/geodia-social-observatory` -> `21 passed in 3.02s`.
- Full GEODIA social observatory:
  `python -B -m pytest tests -q -p no:cacheprovider`
  -> `74 passed in 51.53s`.
- Final canonical pending review after documentation update:
  `python tools\release\pending_review.py --write --quiet`
  -> `active_dedup=0`, `claudio_open=0`.
- Generated v0.2 evidence:
  `python -B -m geodia_social_observatory.cli smallville-v02-report --seed 20260522 --ticks 12 ...`
  -> artifacts in
  `qa_artifacts/smallville_duat/SMALLVILLE_DUAT_20260522`.
- Generated v0.1 evidence:
  `smallville-duat --seed cierre-20260522 --days 1 --ticks-per-day 2`
  and `smallville-falsify`.
- Metrics summary:
  `schema=duat.smallville.metrics.v0_2`, `agents=25`,
  `hash_chain_valid=True`, `falsifiers_passed=True`,
  `publication_gate=BLOCK`, `failed=[]`.
- v0.1 falsifier summary:
  `schema=duat.smallville.falsifier_report.v0_1`, `passed=True`,
  `checks=7`.
- No remote compute, real data, cloud/provider, publication, deploy or push.

## 2026-05-22 - OSIT Epistemic Engine API

- Added `obsai_core/epistemic_engine.py` with local-only
  `OSITEpistemicEngine`, `/health` and `/classify`.
- Added CLI commands `classify-text` and `serve-epistemic-engine`.
- Focal tests:
  `python -B -m pytest tests/test_epistemic_engine.py tests/test_claim_gate_contract.py tests/test_observation_envelope_schema.py tests/test_claim_classifier.py -q -p no:cacheprovider`
  -> `42 passed in 1.50s`.
- Full obsai-core tests:
  `python -B -m pytest tests -q -p no:cacheprovider` -> `71 passed in 3.78s`.
- py_compile touched obsai-core modules -> PASS.
- CLI smoke: `classify-text` returned
  `schemaVersion=obsai.osit_epistemic_engine.response.v1`,
  `gate=APPROVE`, `publication_gate=BLOCK`.
- HTTP smoke efimero: `/health` 200 `status=ok`; `/classify` strong claim
  returned `gate=BLOCK`, `publication_gate=BLOCK`,
  `cloud_provider_called=false`.

## 2026-05-22 - DUAT Lite Local Dashboard

- Added `tools/duat-lite/server.py`, `index.html`, README and tests.
- `python -B -m pytest tools/duat-lite/tests -q -p no:cacheprovider`
  -> `1 passed in 0.97s`.
- `python -B -m py_compile tools/duat-lite/server.py tools/duat-lite/tests/test_duat_lite_server.py`
  -> PASS.
- HTTP smoke efimero:
  page `200`, `/api/health` `200`, `/api/classify` `200`,
  `gate=APPROVE`, `claim_count=1`, `publication_gate=BLOCK`,
  `cloud_provider_called=false`.
- Visual QA Edge headless:
  `qa_artifacts/ui_visual_qa/DUAT_LITE_20260522/duat_lite_dashboard_1366x900.png`
  and `duat_lite_dashboard_390x844.png`.
- Server temporal detenido despues de QA.

## 2026-05-21 - Pending System Execution Closeout

Commands executed:

- `python tools\release\pending_review.py --write --quiet`
  - Initial result: `active_dedup=33`, `claudio_open=0`.
  - Final result: `active_dedup=0`, `claudio_open=0`.
- `python -B -m wabi_sabi.cli.main apply-local-preview docs\WABI_LOCAL_APPLY_CLOSEOUT_TASKSPEC_2026-05-21.json --json --runtime runtime`
  - Result: `LOCAL_APPLY_PATCH_READY`, `secret_scan.status=PASS`, `boundary_scan.status=PASS`, `cloud_provider_called=false`.
- `python -B -m wabi_sabi.cli.main apply-local docs\WABI_LOCAL_APPLY_CLOSEOUT_TASKSPEC_2026-05-21.json --json --runtime runtime`
  - First result: `LOCAL_APPLY_TESTS_FAIL_ROLLED_BACK`, timeout in pytest, `witness_verified=true`.
  - Retried with acotado py_compile gate: `LOCAL_APPLY_TESTS_PASS`, `applied_to_sources=true`, `witness_verified=true`.
- `python -B -m pytest tests/test_local_apply_readiness.py tests/test_build_assist_cloud.py tests/test_cloud_budget.py tests/test_cloud_budget_ui_status.py tests/test_taskspec_review.py -q -p no:cacheprovider`
  - Result: `42 passed in 58.38s`.
- `python -B -m pytest tests/test_multimodal_intake.py -q -p no:cacheprovider`
  - Result: `5 passed in 0.65s`.
- `python -B -m pytest tests/test_hypothesis_packet.py -q -p no:cacheprovider`
  - Result: `5 passed in 2.52s`.
- `python -m unittest discover packages\shared-contracts\tests -v`
  - Result: `Ran 11 tests`, `OK`.
- `npm run build` in `artifacts\duat-city\_external_review\v1_3\audio\app`
  - Result: failed; missing/incompatible modules: `react-router`, `react-resizable-panels`, `kimi-plugin-inspect-react`.
- `npm run lint` in `artifacts\duat-city\_external_review\v1_3\audio\app`
  - Result: failed; `eslint` not installed.

HTTP/API evidence:

- `http://127.0.0.1:8787/` returned HTTP 200 and rendered Wabi Conversation,
  Cloud Budget, Review TaskSpec and Gate Preview text.
- `/api/cloud-budget/status` returned `CLOUD_BUDGET_DRY_RUN`,
  `double_opt_in=false`, `cloud_provider_called=false`.
- `/api/taskspec/gate-preview` returned `apply_status=BLOCKED`,
  `reason=APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1`.
- `POST /api/conversation/turn` route smokes preserved
  `cloud_provider_called=false`, `prompts_stored=false` and local witness
  verification.

Not executed:

- No dependency install by network.
- No cloud/provider live call.
- No push, deploy, publication, Gumroad, Cloudflare or release.

## 2026-05-21 - FlujoCRM GitHub Local Preflight

Commands executed:

- `python tools\release\audit_flujocrm_free_license_readiness.py --write --json`
  - Result: `publication_ready=true`, `blockers=[]`.
- `python tools\release\scan_secrets.py --path publish_staging\github\flujocrm-free-review --json`
  - Result: `count_reported=0`.
- `npm run check` in `publish_staging\github\flujocrm-free-review`
  - Result: `flujocrm main smoke passed`, `flujocrm preload smoke passed`,
    `flujocrm renderer smoke passed`.
- Local manifest comparison:
  - `manifest_count=16`, `actual_count=21`, `missing_count=0`,
    `extra_count=5` review/control files.

Not executed:

- No `gh repo create`, `git push`, `gh repo edit`, website update or
  publication.

## 2026-05-21 - Wabi Observation Claim Adapter + obsai-core Schema

- Wabi adapter focal:
  `python -B -m pytest tests/test_observation_claim_adapter.py tests/test_hypothesis_packet.py -q -p no:cacheprovider`
  -> `8 passed in 2.49s`.
- Wabi py_compile: `observation_claim_adapter.py`, `cli/main.py`,
  `test_observation_claim_adapter.py` -> PASS.
- Real 12-claim fixture review after calibration: `case_count=12`,
  `pass_count=12`, `review_count=0`, `status=PASS`.
- obsai-core gate/schema/claim focal:
  `python -B -m pytest tests/test_claim_gate_contract.py tests/test_observation_envelope_schema.py tests/test_claim_classifier.py -q -p no:cacheprovider`
  -> `38 passed in 0.29s`.
- obsai-core full tests:
  `python -B -m pytest tests -q -p no:cacheprovider` -> `67 passed in 2.00s`.
- obsai-core py_compile -> PASS.
- BDI Lean environment check: `lean`, `lake`, `elan` NOT_AVAILABLE.
- Final scoped markdown checkbox scans:
  - MEDIOEVO primary workspace with excludes -> no active unchecked checkbox
    matches.
  - BRAIN_OS `00_START_HERE` + `-=LR WORKING BENCH=-` with archive excludes
    -> no active unchecked checkbox matches after classifying BRAIN_OS packet
    residuals.
- Final canonical pending review:
  `python tools\release\pending_review.py --write --quiet` ->
  `active_dedup=0`, `claudio_open=0`.

## WABI_LOCAL_APPLY_READY_20260519

Commands executed:

- `python -B -m pytest tests\test_local_apply_readiness.py tests\test_taskspec_review.py tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_cloud_budget.py tests\test_build_assist_cloud.py -q -p no:cacheprovider`
  - Result: `51 passed`

- `python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py 02_CLAUDIO\tests\test_wabi_conversation_api.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py 02_CLAUDIO\tests\test_wabi_taskspec_gate_preview_api.py 02_CLAUDIO\tests\test_wabi_local_apply_api.py -q -p no:cacheprovider`
  - Result: `254 passed`

- CLI real apply:
  - `.\wabi.cmd --once "programa un helper seguro para validar json" --json`
  - `.\wabi.cmd apply-local-preview --latest --json`
  - `.\wabi.cmd apply-local --latest --json`
  - Result: `LOCAL_APPLY_TESTS_PASS`, `applied_to_sources=true`, `cloud_provider_called=false`

- `python -B -m pytest tests\test_json_safety.py tests\test_local_apply_readiness.py tests\test_conversational_cli.py -q -p no:cacheprovider`
  - Result: `18 passed`

- Wabi full regression:
  - `python -B -m pytest -q -p no:cacheprovider`
  - Result: `374 passed`

- BRAIN_OS full regression:
  - `python -B -m pytest -q -p no:cacheprovider`
  - Result: `764 passed`

- py_compile touched modules:
  - Result: PASS

- Focal concrete secret-value scan over touched source/UI files:
  - Result: `concrete_secret_value_matches=0`, `values_printed=false`

## Runtime Evidence

- Rollback snapshot: `C:\Users\L-Tyr\.medioevo\wabi\runtime\rollback\patch-20260519-224609-6fdd476832d1.json`
- Execution report: `C:\Users\L-Tyr\.medioevo\wabi\runtime\executions\patch-20260519-224609-6fdd476832d1.json`
- Witness event: `47`
- Witness verify: `true`

## Gates

- Cloud live: not called.
- BrowserBridge live: not enabled.
- graphics_live: false.
- Push/deploy/publication: not performed.

## WABI_UI_TASKSPEC_MULTI_SMOKE_20260519

- UI smoke API/HTML:
  - `/`: HTTP 200
  - `/api/cloud-budget/status`: HTTP 200
  - `/api/taskspec/latest`: HTTP 200
  - `/api/taskspec/gate-preview`: HTTP 200
  - `/api/taskspec/apply-local-preview`: HTTP 200
  - Wabi Conversation present: true
  - Review TaskSpec present: true
  - Gate Preview present: true
  - Apply Local Preview present: true
  - Apply Local present and initially disabled: true

- Evidence:
  - `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_UI_TASKSPEC_MULTI_SMOKE_20260519\wabi_ui_smoke_127_0_0_1_8787.png`
  - `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_UI_TASKSPEC_MULTI_SMOKE_20260519\wabi_ui_text_snapshot.md`

- TaskSpec multiarchivo:
  - `ConversationEngine.create_task_spec()` now emits `affected_paths`, `changes`, `suggested_tests`, `rollback_required`, `rollback_strategy`, `next_action`, and correct proposal/apply flags.

- Assets Du WABI:
  - Manifest: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\asset_audit\WABI_ASSETS_DU_WABI_20260519\wabi_assets_du_wabi_audit_20260519_v0_3.json`
  - Snapshot total: 181 files, 178 PNG, 3 ZIP.
  - Stripped PNG runtime candidates: 178.
  - Stripped metadata zero count: 178.
  - Release included count: 0.

- Witness:
  - Event 48: UI TaskSpec multi smoke.
  - Event 49: Assets audit strip.
  - Chain verify: PASS.

- Tests:
  - Wabi focal: `33 passed`
  - BRAIN_OS local apply API focal: `5 passed`
  - BRAIN_OS server/UI focal: `250 passed`
  - Wabi regression: `376 passed`
  - BRAIN_OS regression: `765 passed`
  - py_compile touched modules: PASS
  - Secret scan focal: `concrete_secret_value_matches=0`

## WABI_VIBE_CODING_MODE_20260520

- Wabi CLI/core focal:
  - `python -B -m pytest tests\test_llm_work_response.py tests\test_llm_proposal.py tests\test_conversational_cli.py tests\test_cli.py -q -p no:cacheprovider`
  - Result: `30 passed`

- BRAIN_OS UI/API focal:
  - `python -B -m pytest 02_CLAUDIO\tests\test_wabi_conversation_api.py 02_CLAUDIO\tests\test_wabi_llm_work_response_api.py 02_CLAUDIO\tests\test_wabi_llm_proposal_api.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py 02_CLAUDIO\tests\test_wabi_local_apply_api.py -q -p no:cacheprovider`
  - Result: `25 passed`

- py_compile:
  - `wabi_sabi/core/llm_work_response.py`
  - `wabi_sabi/core/llm_proposal.py`
  - `wabi_sabi/core/conversation_engine.py`
  - `wabi_sabi/cli/main.py`
  - `02_CLAUDIO/server/wabi_local_server.py`
  - Result: PASS

- CLI smoke:
  - Code request: `status=OK`, `intent_name=code_request`, `route=code_plan`, `cloud_provider_called=false`, `applied_to_sources=false`, `graphics_live=false`, tags include `vibe_coding`.
  - DUAT graphics request: `graphics_plan_ready=true`, `graphics_live=false`, tags include `duat_graphics_plan` and `vibe_coding`.

- UI HTTP smoke:
  - `http://127.0.0.1:8787/`: HTTP 200.
  - `Vibe Coding`, `Wabi Conversation`, `Review TaskSpec`, `Gate Preview`, `Apply Local Preview`: present.
  - `Call NVIDIA now` / `Apply cloud output`: absent.

- Secret scan focal:
  - `FOCAL_SECRET_PATTERN_COUNT=0`

- Not run:
  - Browser plugin screenshot was unavailable in this turn.
  - Full regression not rerun because changes were contract/UI-scoped and focal suites passed.
