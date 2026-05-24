# DECISIONS

## 2026-05-23 - Espejo BRAIN_OS Wabi UI chat endpoint

- Keep BRAIN_OS as execution root for `/api/chat/message` fix.
- Treat Wabi tree consolidation and cost-router as REVIEW/RFC work, not mirror
  auto-execution.
- Provider live call in this cycle was limited to local smoke verification; no
  secrets printed and no external publication/deploy/apply.

## 2026-05-23 - Espejo BRAIN_OS Wabi chat cloud identity

- Keep `-= BRAIN_OS =-` as the execution root for this Wabi chat fix.
- Treat this root as technical mirror only; do not reopen publication, push,
  deploy, apply or delete paths from the mirror.
- Record that provider live calls in this cycle were limited to requested local
  LLM smoke verification, with secrets not printed.

## 2026-05-22 - Fragmentos Cover Asset Gate

- Add a reusable asset gate before generating or selecting a cover so review
  state is machine-readable and repeatable.
- Treat missing asset as `REVIEW_ASSET_MISSING`, not as failure and not as
  approval.
- Keep the positive asset path at `REVIEW_READY_FOR_HUMAN_VISUAL`; even a
  clean image is not publication approval.
- Require `PublicationGate=BLOCK` in every cover asset manifest until a
  target-specific human gate exists.

## 2026-05-22 - Human Gate Packet + Fragmentos Cover Brief

- Keep Fragmentos and Calibracion in human publication review, not automatic
  publication.
- Choose Fragmentos as the next lower-risk visual candidate because the public
  framing can stay literary/archival and avoid technical claims.
- Create only a cover brief, not an image asset, until human asset review opens
  `REVIEW_ASSET_PRODUCTION`.
- Keep Calibracion prepared but unopened for staging because it requires more
  care around technical/proprietary-theory language.

## 2026-05-22 - Editorial Word/PDF Full-Page QA

- Use Microsoft Word COM local read-only export as the authoritative practical
  fallback when `artifact-tool` DOCX rendering times out on long manuscripts.
- Treat Word/PDF full-page automated coverage as closed local QA evidence for
  blank/edge-layout smoke, not as commercial/publication approval.
- Keep human editorial/store/print review in REVIEW before any public use.
- Keep all generated PNGs/contact sheets private because they contain full
  manuscript pages.

## 2026-05-22 - Editorial DOCX Split QA

- Do not mark Fragmentos or Calibracion DOCX layout as fully approved because
  full `artifact-tool` rendering timed out.
- Preserve partial DOCX PNG pages as smoke evidence only.
- Use representative integrated-PDF renders to improve confidence, while
  keeping full DOCX page-by-page approval in REVIEW.
- Stop only the render processes launched in this session; do not touch older
  Claudio/Wabi processes.

## 2026-05-22 - Editorial Internal Exports

- Treat Fragmentos and Calibracion exports as private editorial full-text
  material, not public staging.
- Use only the already integrated canon10 artifacts for this local closure:
  MD, HTML, DOCX, PDF, metrics and source manifest.
- Generate EPUB locally with Calibre for internal review parity with Deriva.
- Keep `PublicationGate=BLOCK`, `originals_modified=false` and
  `external_actions_performed=false` in both manifests.
- Do not convert `pending_review active_dedup=0` into permission to publish,
  push, deploy, upload, sell or create public ZIPs.

## 2026-05-22 - OSIT-HYBRID Multi-Seed

- Close OSIT-HYBRID multi-seed as a synthetic local harness because the
  original simulator source was not present in the active Workbench.
- Require the report to say that `GS raw` wins by mean comparable Score in this
  harness, while `GS OSIT` is close and has lower mean `R_mu`; do not preserve
  the older single-run conclusion as universal.
- Keep all external/NRMP/real-data claims blocked until source, license,
  preregistration and validation exist.

## 2026-05-22 - Smallville-DUAT Local Evidence

- Close the Smallville-DUAT local reproducible lane by revalidating the
  existing implementation and generating fresh local artifacts, instead of
  duplicating the simulator.
- Keep Smallville evidence synthetic/local with `PublicationGate=BLOCK`.
- Treat Colab, Kaggle, SimScale, real data and sensors as separate
  review-gated scopes.

## 2026-05-22 - OSIT Epistemic Engine API

- Implement OSIT Epistemic Engine as a dependency-free local API inside
  `obsai-core`, not as a Flask app or public service.
- Keep the HTTP surface localhost-oriented and minimal: `/health` and
  `/classify`.
- Preserve `publication_gate=BLOCK`, `calibration=DEMO_ONLY`,
  `cloud_provider_called=false` and `applied_to_sources=false` in outputs.

## 2026-05-22 - DUAT Lite Local Dashboard

- Place DUAT Lite under `tools/duat-lite` as a local tool because
  `claudio/apps` does not exist in this workspace root.
- Serve the dashboard with stdlib Python and the local OSIT Epistemic Engine
  instead of adding frontend or Flask dependencies.
- Treat screenshots as local QA evidence only, not publication approval.

## 2026-05-21 - Wabi Observation Claim Adapter + obsai-core Schema

- Treat the Wabi claim adapter as proposal-only local review: it emits
  envelopes, artifacts and WitnessLog evidence, but does not mutate source
  material.
- Treat `obsai.claim_gate_contract.v1` as the local unified contract for
  TruthGate, C-GATE, PhysicsHonestyGate and ScienceClaimGate.
- Keep canonical OSIT/Wabi fixture rules inside obsai-core as `DEMO_ONLY`
  calibration, not public scientific validation.
- Use ObservationEnvelope v2.1 schema as a local contract between Wabi and
  obsai-core before any release packaging.
- Do not install or assume Lean validation in this cycle; `BDI_Category.lean`
  remains environment-blocked until a toolchain is explicitly available.

## 2026-05-21 - Pending System Execution Closeout

- Treat `tools\release\pending_review.py --write --quiet` as the canonical
  scattered-pending snapshot for this cycle.
- Execute local reversible Wabi/Claudio items first and keep cloud, public,
  host-admin and manual-login checks outside automatic execution.
- Reclassify non-executable residues into `REVIEW_REQUIRED.md` rather than
  leaving them as active local checkboxes.
- Keep `PublicationGate=BLOCK`, `CloudGate=DRY_RUN`, and host `APPROVE` not
  declared from this run.
- For `prompt_started_at`, record source unavailability explicitly instead of
  inventing an approximate timestamp.

## 2026-05-19 - Wabi MCP Gated-Write Design v0.4
- Decision: Wabi MCP v0.4 may expose gated-write tools only as design-only/dry-run-only surfaces.
- Decision: real gated-write remains disabled with `gated_write_enabled=false` and `real_apply_allowed=false`.
- Decision: `scheduler_tick`, `execute_local_workpack`, `queue_workpack`, `run_ghostgate` and `rollback_workpack` must return blocked/design-only from MCP v0.4.
- Decision: dry-run lane allowlist is limited to `SANDBOX` and `DOCS_LOCAL`.
- Decision: cloud, publication, NVIDIA, DeepSeek, remote compute and protected material lanes are blocked.
- Decision: Mission Control may report v0.4 readiness, but cannot execute or mutate from the dashboard.
# WABI_LOCAL_APPLY_READY_20260519

- Enable local apply only through the new explicit Local Apply path, not the legacy TaskSpec apply endpoint.
- Keep cloud provider output proposal-only; no live cloud call was made.
- Keep graphics plan-only; `graphics_live=false`.
- Use `SafeExecutor` and `RollbackStore` as the only source-writing mechanism for this phase.
- Block GitHub/medioevo.space release because the detected git top-level is host-wide, the worktree is dirty with unrelated changes, no remote is configured, and AssetGate remains REVIEW.

# WABI_UI_TASKSPEC_MULTI_SMOKE_20260519

- Keep `Apply Local` visible but disabled until `/api/taskspec/apply-local-preview` returns a ready candidate.
- Extend TaskSpec generation to include multi-file `changes`, `affected_paths`, tests, rollback strategy and next safe action.
- Store raw TaskSpec only in server memory for apply-local; UI and saved drafts remain redacted.
- Treat stripped asset copies as internal runtime staging, not public-safe release assets.

# WABI_VIBE_CODING_MODE_20260520

- Treat Vibe Coding as an interaction mode over the existing Wabi safety stack, not as a new executor.
- Add `vibe_coding` to the safe JSON contract and UI so code/debug/DUAT requests are visibly routed through proposal, TaskSpec, Gate Preview and Apply Local Preview.
- Keep cloud proposal-only by default; live cloud still requires `WABI_BUILD_ASSIST_CLOUD=1`, `WABI_ALLOW_CLOUD_PROVIDERS=1` and CloudBudgetGate allowance.
- Keep DUAT graphics plan-only; `graphics_live=false`.
- Keep Apply Local separated from proposal generation and require explicit preview/readiness before local mutation.
