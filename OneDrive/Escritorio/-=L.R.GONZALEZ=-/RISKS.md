# RISKS

## 2026-05-22 - Fragmentos Cover Asset Gate

- Risk: a green validator run could be mistaken for publication approval.
  Mitigation: the validator only reaches `REVIEW_READY_FOR_HUMAN_VISUAL` and
  always emits `not_publication_approval=true`.
- Risk: missing asset state could be hidden as a generic failure. Mitigation:
  the current manifest records `REVIEW_ASSET_MISSING` and
  `LICENSE_STATUS_REVIEW_REQUIRED`.
- Risk: future raster assets may carry metadata. Mitigation: the validator
  reports metadata keys and requires strip/review before public staging.
- Risk: image content could leak manuscript text, private diagrams or RPG/TCG
  material. Mitigation: report requires manual text and visual boundary checks.

## 2026-05-22 - Human Gate Packet + Fragmentos Cover Brief

- Risk: a cover brief could be mistaken for approval to generate or publish an
  asset. Mitigation: docs mark `REVIEW_ASSET_PRODUCTION` and
  `PublicationGate=BLOCK`.
- Risk: Calibracion public copy could expose or imply proprietary method claims.
  Mitigation: Calibracion stays prepared but not selected for first cover
  staging.
- Risk: generated cover could accidentally include private manuscript text or
  RPG/TCG assets. Mitigation: brief explicitly blocks text, private diagrams,
  runtime internals, RPG/TCG and local paths.

## 2026-05-22 - Editorial Word/PDF Full-Page QA

- Risk: automated full-page coverage may be mistaken for human editorial
  approval. Mitigation: trackers keep human store/print/publication review in
  REVIEW and `PublicationGate=BLOCK`.
- Risk: rendered PNGs/contact sheets expose manuscript pages. Mitigation:
  artifacts remain internal under `qa_artifacts` and must not be packaged
  publicly.
- Risk: Word COM could leave a background process. Mitigation: post-run process
  check found no active `WINWORD` or QA script process.

## 2026-05-22 - Editorial DOCX Split QA

- Risk: partial render evidence could be mistaken for complete visual approval.
  Mitigation: trackers state `PARTIAL_QA_REVIEW_WITH_LIMITS` and keep full
  page-by-page approval in REVIEW.
- Risk: QA PNGs/PDF renders contain private manuscript pages. Mitigation:
  artifacts stay under internal `qa_artifacts`; `PublicationGate=BLOCK`.
- Risk: long `artifact-tool` render jobs can consume CPU after timeout.
  Mitigation: exact render `python.exe`/`node.exe` processes launched in this
  session were identified and stopped.

## 2026-05-22 - Editorial Internal Exports

- Risk: internal exports contain full manuscript material. Mitigation:
  manifests and trackers mark them `BOOKS_EDITORIAL_INTERNAL_FULL_TEXT` with
  `PublicationGate=BLOCK`.
- Risk: generated EPUBs could be mistaken for store-ready assets. Mitigation:
  they are internal review artifacts only; KDP/Gumroad/web/social/public ZIP
  remain blocked.
- Risk: root and BRAIN_OS pending mirrors can drift. Mitigation: root trackers
  and LIVE_STATE mirrors are synchronized in this closeout.

## 2026-05-22 - OSIT-HYBRID Multi-Seed

- Risk: the synthetic harness could be mistaken for the original simulator.
  Mitigation: closeout docs state original simulator source was not recovered.
- Risk: ranking change could be overinterpreted. Mitigation: report only local
  synthetic results and keep `PublicationGate=BLOCK`.
- Risk: Source Cards may look like real applicant/program records. Mitigation:
  all cards use synthetic IDs and `source_scope=SYNTHETIC_LOCAL_AUDIT`.

## 2026-05-22 - Smallville-DUAT Local Evidence

- Risk: synthetic Smallville evidence could be mistaken for real-world
  predictive validation. Mitigation: docs and artifacts keep
  `PublicationGate=BLOCK` and report this as local synthetic evidence only.
- Risk: remote-compute plans could be treated as permission to execute Colab,
  Kaggle or SimScale. Mitigation: remote compute remains REVIEW and was not
  run.
- Risk: generated ledgers are evidence artifacts, not public packages.
  Mitigation: they remain under `qa_artifacts` with no push/deploy/upload.

## 2026-05-22 - OSIT Epistemic Engine API

- Risk: local API may be mistaken for public-ready service. Mitigation:
  outputs keep `PublicationGate=BLOCK` and docs state local-only.
- Risk: claim classification thresholds may be overstated. Mitigation:
  `calibration=DEMO_ONLY` remains in API, envelope and source card.
- Risk: long-running server could be left open accidentally. Mitigation:
  no server was left running; smoke used an ephemeral in-process server.

## 2026-05-22 - DUAT Lite Local Dashboard

- Risk: local dashboard could be mistaken for deploy-ready product.
  Mitigation: README and outputs keep `publication_gate=BLOCK`.
- Risk: server process could remain running. Mitigation: QA server was stopped
  and no persistent service was installed.
- Risk: UI could overstate claim status. Mitigation: dashboard displays gate,
  R, Phi_eff and next action from the OSIT engine output.

## 2026-05-21 - Wabi Observation Claim Adapter + obsai-core Schema

- Risk: calibrated OSIT/Wabi fixture rules could be overstated as external
  validation. Mitigation: mark them `DEMO_ONLY`, keep `PublicationGate=BLOCK`
  and report only local fixture evidence.
- Risk: ObservationEnvelope schema may drift before public packaging.
  Mitigation: keep schema tests and adapter tests as the current contract.
- Risk: Lean formal file may be mistaken for verified proof. Mitigation:
  environment check records `lean/lake/elan` unavailable; no proof is claimed.
- Risk: adapter output may be mistaken for source adoption. Mitigation:
  payloads include `proposal_only=true`, `applied_to_sources=false` and
  `cloud_provider_called=false`.

## 2026-05-21 - Pending System Execution Closeout

- Risk: marking gated/manual host items as locally done would invent evidence.
  Mitigation: moved them to `REVIEW_REQUIRED.md` and kept host approval unset.
- Risk: DUAT-city audio tests require dependency changes that may use network.
  Mitigation: build/lint were attempted without install; dependency install is
  review-gated.
- Risk: Wabi Apply Local can mutate files. Mitigation: used allowlisted
  TaskSpec, preview, rollback, py_compile gate and WitnessLog verification.
- Risk: pending count can hide deferred Kairos decisions. Mitigation: final
  pending snapshot reports active markdown `0`; stale Kairos fastlane remains
  snapshot-only and not permission to execute broad batches.

## Wabi MCP Gated-Write Design v0.4
- Risk: dry-run could be mistaken for real execution. Mitigation: outputs include `executed=false`, `mutated=false`, `real_apply_allowed=false`.
- Risk: scheduler tick could be invoked through MCP. Mitigation: `scheduler_tick` returns design-only blocked response and no scheduler state change.
- Risk: workpack execution could be invoked through MCP. Mitigation: `execute_local_workpack` returns design-only blocked response and no workpack state change.
- Risk: public/cloud/protected lanes could be requested. Mitigation: validator blocks `PUBLICATION`, `CLOUD`, `NVIDIA`, `DEEPSEEK`, `REMOTE_COMPUTE`, `PROTECTED_MATERIAL`.
- Risk: external bind could expose local MCP. Mitigation: endpoint remains localhost-only; external bind scan PASS.
# WABI_LOCAL_APPLY_READY_20260519

- Local Apply can now write files, so keep allowlist narrow and do not add arbitrary command execution from UI.
- Current release git boundary is unsafe: `git rev-parse --show-toplevel` resolves to `C:\Users\L-Tyr`.
- Worktree has many unrelated changes; do not broad-stage or push.
- `Assets Du WABI` contains 167 PNGs with property metadata and 3 zip files; public copy remains REVIEW until stripping/provenance review.
- NVIDIA usage/cost remains unknown unless provider returns usage; cloud stays proposal-only.

# WABI_UI_TASKSPEC_MULTI_SMOKE_20260519

- Source asset folder changed during audit, so manifests are point-in-time snapshots, not a stable release list.
- PNG metadata is stripped in runtime staging, but public release still needs provenance/license review.
- ZIP assets remain unextracted and REVIEW_REQUIRED.
- Browser plugin Node REPL was unavailable; UI smoke used HTTP, HTML snapshot and Edge headless screenshot fallback.

# WABI_VIBE_CODING_MODE_20260520

- Vibe-style UI can make proposal output feel executable. Mitigation: keep `proposal_only`, Gate Preview, Apply Local Preview and explicit Apply Local visible in the same flow.
- Live cloud remains a cost/quota risk. Mitigation: double opt-in plus CloudBudgetGate; no live cloud call in this cycle.
- Browser plugin was not exposed in this turn, so visual QA is HTTP/HTML smoke rather than screenshot evidence.
