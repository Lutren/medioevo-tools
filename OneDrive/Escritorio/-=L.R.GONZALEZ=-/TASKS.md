# TASKS

## 2026-05-23 - Espejo tecnico BRAIN_OS Wabi `/api/chat/message`

- DONE: cierre ejecutado en `-= BRAIN_OS =-`: `/api/chat/message` modelo/hora
  usa LLM real y ya no diagnóstico stale como ruta primaria.
- EVIDENCE: BRAIN_OS relevant Wabi suite -> `281 passed`; full
  `02_CLAUDIO/tests` -> `836 passed in 59.19s`.
- EVIDENCE: live HTTP smoke -> `online_ai_called=True`, modelo real, cláusula
  de reloj, `forbidden_mentions=[]`.
- REVIEW: consolidar árboles Wabi y router por costo quedan como RFC/gate
  separado.

## 2026-05-23 - Espejo tecnico BRAIN_OS Wabi chat cloud identity

- DONE: cierre ejecutado en `-= BRAIN_OS =-`: Wabi chat CLI/UI con cloud LLM
  real e identidad de modelo anclada.
- DONE: `cloud_provider_called` ya no depende solo del flag legacy; dry-run no
  se marca como llamada real.
- EVIDENCE: BRAIN_OS full `02_CLAUDIO/tests` -> `836 passed in 63.31s`.
- EVIDENCE: CLI smoke vivo y UI HTTP smoke vivo pasaron sin identidades
  Claude/GPT/Gemini/Alibaba.
- REVIEW: este root queda como espejo tecnico; no publicar, pushear, desplegar,
  aplicar writes ni borrar.

## 2026-05-23 - Espejo tecnico BRAIN_OS Wabi Programmer delegation

- DONE: pending snapshot local sigue en cero: `active_dedup=0`, `claudio_open=0`.
- DONE: cierre ejecutado en `-= BRAIN_OS =-`: Wabi Programmer CLI apply -> SafeExecutor.
- EVIDENCE: BRAIN_OS full `02_CLAUDIO/tests` -> `822 passed in 71.38s`.
- REVIEW: este root queda como espejo tecnico; no publicar, pushear, desplegar ni borrar.

## 2026-05-22 - Espejo tecnico hacia BRAIN_OS principal

- DONE: `-= BRAIN_OS =-` seleccionado como arbol principal de pendientes y
  handoffs.
- DONE: `pending_review.py --write --quiet` actualizado en este workspace:
  `active_dedup=0`, `claudio_open=0`.
- DONE: cierre Wabi sincronizado desde BRAIN_OS: alias NVIDIA corregido y Wabi
  suite `439 passed`.
- REVIEW: este workspace mantiene ejecucion tecnica; la cola humana principal
  vive en `-= BRAIN_OS =-`.

## 2026-05-22 - Fragmentos Cover Asset Gate

- DONE: added reusable local gate validator
  `tools/release/validate_cover_asset_gate.py`.
- DONE: added focal tests for missing asset, clean synthetic asset and open
  publication gate block.
- DONE: created Fragmentos cover gate manifest under
  `qa_artifacts/editorial_cover_gate/FRAGMENTOS_COVER_GATE_20260522`.
- DONE: generated gate summary/report with
  `overall_status=REVIEW_ASSET_MISSING`.
- DONE: focal tests passed `3 passed`; py_compile passed.
- DONE: focal secret scan over script/test/gate artifacts returned
  `count_reported=0` in `--artifact` mode.
- REVIEW: actual cover generation/selection, asset path, provenance/license
  and platform dimensions remain gated.
- BLOCK: no KDP, Gumroad, web, social, push, deploy, public ZIP or external
  release.

## 2026-05-22 - Human Gate Packet + Fragmentos Cover Brief

- DONE: created human publication gate packet for Fragmentos/Calibracion.
- DONE: created machine-readable JSON gate packet.
- DONE: selected Fragmentos as lower-risk next candidate for cover review.
- DONE: created public-safe Fragmentos cover brief and JSON.
- DONE: validated JSON parsing for both packets.
- DONE: ran focal secret scans over all new docs; `count_reported=0`.
- REVIEW: real cover generation/selection remains gated by human asset review.
- BLOCK: no public staging, upload, push, deploy, Gumroad, KDP, web, social or
  public ZIP.

## 2026-05-22 - Editorial Word/PDF Full-Page QA

- DONE: added reusable local QA script
  `tools/release/editorial_docx_word_visual_qa.py`.
- DONE: confirmed Microsoft Word COM availability and used read-only invisible
  Word export for the private DOCX files.
- DONE: exported Fragmentos DOCX to PDF and rendered all `688` pages.
- DONE: exported Calibracion DOCX to PDF and rendered all `477` pages.
- DONE: generated image metrics, per-page PNGs, contact sheets and QA report.
- DONE: automated full-page coverage passed with `blank_candidates=0` and
  `edge_contact_candidates=0` for both books.
- REVIEW: human editorial/commercial approval remains required before any
  public/store/print action.
- BLOCK: publishing, uploading, pushing, deploying, public ZIP and external
  release remain blocked.

## 2026-05-22 - Editorial DOCX Split QA

- DONE: attempted full `artifact-tool` DOCX render for Fragmentos; timed out
  after controlled window and was stopped without leaving render processes.
- DONE: captured `53` Fragmentos DOCX PNG pages under
  `qa_artifacts/editorial_docx_visual_qa/FRAGMENTOS_INTERNAL_EXPORT_2026-05-22`.
- DONE: attempted full `artifact-tool` DOCX render for Calibracion; timed out
  after controlled window and was stopped without leaving render processes.
- DONE: captured `19` Calibracion DOCX PNG pages under
  `qa_artifacts/editorial_docx_visual_qa/CALIBRACION_INTERNAL_EXPORT_2026-05-22`.
- DONE: rendered representative integrated-PDF pages for both books and wrote
  split QA summary/report.
- REVIEW: full page-by-page visual DOCX approval remains open because the
  renderer did not complete and direct visual inspection of every page was not
  performed.

## 2026-05-22 - Editorial Internal Exports

- DONE: refreshed canonical pending review:
  `active_dedup=0`, `claudio_open=0`.
- DONE: created
  `books/editorial/internal_exports/FRAGMENTOS_INTERNAL_EXPORT_2026-05-22`
  from canon10 integrated Fragmentos artifacts.
- DONE: created
  `books/editorial/internal_exports/CALIBRACION_INTERNAL_EXPORT_2026-05-22`
  from canon10 integrated Calibracion artifacts.
- DONE: generated local EPUBs with Calibre `ebook-convert`.
- DONE: wrote README and `INTERNAL_EXPORT_MANIFEST.json` for both packages.
- DONE: verified manifest hashes for both packages: `hash_ok=True`.
- REVIEW: DOCX full visual QA, cover briefs, store assets, legal/commercial
  review and publication remain separate gates.
- BLOCK: GitHub, Gumroad, KDP, web, social, push, deploy, public ZIP and
  external release from these private exports.

## 2026-05-22 - Workbench Maintenance

- DONE: `DOCUMENTOS_IA/01_LOCAL_COMPLETA` updated with internal evidence annex.
- REVIEWED: `DOCUMENTOS_IA/02_PUBLIC_SAFE` unchanged; PDF not regenerated.
- DONE: Workbench shortcuts checked; `10/10` valid after retargeting
  `10_WORKBENCH_CANON.lnk`.
- DONE: `ASSETS/INDEX.md` and `LORE/INDEX.md` created.
- DONE: no loose images found in Workbench root.

## 2026-05-22 - OSIT-HYBRID Multi-Seed

- DONE: local synthetic OSIT-HYBRID multi-seed harness created in BRAIN_OS
  Workbench Descubrimientos.
- DONE: 100-seed run generated comparable `R_mu` for all six scenarios.
- DONE: Source Cards generated for all six scenarios on audit seed
  `20260522` (`4800` cards total).
- DONE: artifacts written to
  `qa_artifacts/osit_hybrid/OSIT_HYBRID_MULTI_SEED_20260522`.
- DONE: focal harness tests passed `3 passed`; full Descubrimientos tests
  passed `37 passed`.
- REVIEW: this is synthetic local evidence, not original-simulator recovery or
  external validation.

## 2026-05-22 - Smallville-DUAT Local Evidence

- DONE: Smallville-DUAT local reproducible lane revalidated with fresh
  artifacts.
- DONE: v0.1 ledger/falsifier generated under
  `qa_artifacts/smallville_duat/SMALLVILLE_DUAT_20260522`.
- DONE: v0.2 release-validation manifest generated with SignalSourcePack,
  baseline/intervention ledgers, replay verification, metrics and falsifier.
- DONE: focused Smallville tests passed `21 passed`; full
  `geodia-social-observatory` suite passed `74 passed`.
- REVIEW: Colab/Kaggle/SimScale remain remote-compute review only.
- NEXT_LOCAL: OSIT-HYBRID multi-seed now closed; rerun pending review before
  opening any additional backlog.

## 2026-05-21 - Wabi Observation Claim Adapter + obsai-core Schema

- DONE 2026-05-22: OSIT Epistemic Engine API minima added to obsai-core with
  CLI and local HTTP endpoints.
- DONE 2026-05-22: DUAT Lite local dashboard added under `tools/duat-lite`
  with visual QA and tests.
- DONE: Wabi `claim-fixtures` adapter created for proposal-only
  ObservationEnvelope + ClaimClassifier review.
- DONE: obsai-core ObservationEnvelope v2.1 JSON Schema added and tested.
- DONE: `TruthGate`, `C-GATE`, `PhysicsHonestyGate` and
  `ScienceClaimGate` unified as `obsai.claim_gate_contract.v1`.
- DONE: canonical OSIT/Wabi 12-claim fixture calibrated to `PASS`
  (`pass_count=12`, `review_count=0`).
- DONE: BRAIN_OS packet checkboxes classified: modular-brains item closed by
  tested contract; backup-deletion item moved to REVIEW/BLOCK without delete.
- DONE: BDI Lean environment check documented; Lean toolchain is not available
  in this host shell.
- REVIEW: Lean formal validation remains pending until toolchain exists.
- REVIEW: public schema/release adoption remains gated; this is local evidence,
  not publication.

## 2026-05-21 - Pending System Execution Closeout

- DONE: canonical scattered pending review reduced from `active_dedup=33` to
  `active_dedup=0`.
- DONE: Wabi local apply closeout executed with preview, rollback evidence and
  final `LOCAL_APPLY_TESTS_PASS`.
- DONE: Wabi UI/API local smokes verified on `127.0.0.1:8787` without cloud
  provider calls.
- DONE: Wabi multimodal dark-frame calibration added and tested.
- DONE: Hypothesis mode and shared contracts focal tests passed.
- DONE: MEDIOEVO_LIVE_TREE prompt timestamp item closed without inventing a
  source timestamp.
- REVIEW: DUAT-city audio automated tests/manual browser QA require dependency
  and manual-review lane.
- REVIEW: host next-login check and host clearance remain gated; host not
  declared `APPROVE`.
- NEXT: only reopen work from `docs\pending\PENDING_REVIEW_LATEST.md` if a
  future snapshot shows active local items again.

## 2026-05-21 - FlujoCRM GitHub Local Preflight

- DONE: license readiness preflight returned `publication_ready=true`.
- DONE: focused staging secret scan returned `count_reported=0`.
- DONE: `npm run check` passed main/preload/renderer smokes.
- DONE: Windows-first install notes confirmed in staging.
- REVIEW: live GitHub verification, post-publication scan, website URL update
  and screenshots remain gated until publication target is allowed.
- REVIEW: final manifest should be regenerated or explicitly include the five
  review/control files before push.

## Completed

- Implement Wabi Local Apply Readiness v0.1.
- Add PathAllowlist, SecretScan, BoundaryScan and rollback-backed apply flow.
- Add CLI commands `apply-local-preview` and `apply-local`.
- Add UI controls `Apply Local Preview` and `Apply Local`.
- Add API endpoints `/api/taskspec/apply-local-preview` and `/api/taskspec/apply-local`.
- Apply a real allowlisted patch through Wabi CLI.
- Add `json_safety.py` and `test_json_safety.py` via Wabi local apply.
- Run focal and regression tests.
- Audit `Assets Du WABI` metadata count.
- Document release blockers for GitHub/medioevo.space.
- Complete Wabi UI TaskSpec multi smoke at `127.0.0.1:8787`.
- Add multi-file TaskSpec fields from ConversationEngine.
- Keep `Apply Local` disabled until preview readiness.
- Strip 178 PNG asset candidates into runtime staging with zero metadata keys.
- Append WitnessLog events 48 and 49.
- Add Wabi Vibe Coding mode to the safe JSON contract and UI.
- Add Vibe Coding UI smoke and tests without enabling cloud live or auto-apply.

## Next

- Use Vibe Coding for a small local task and verify Apply Local Preview before explicit Apply Local.
- Create isolated release worktree or confirm correct GitHub repo/remote.
- Select and metadata-strip a public-safe asset subset.
- Owner review for asset provenance/license and zip contents.
- Interactive browser smoke if the Browser plugin runtime is exposed in a later session.
