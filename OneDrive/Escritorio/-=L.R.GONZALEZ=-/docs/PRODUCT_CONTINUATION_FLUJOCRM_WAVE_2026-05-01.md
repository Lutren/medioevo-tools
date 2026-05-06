# Product Continuation - FlujoCRM / Wave FC - 2026-05-01

Status: `CONTINUITY_UPDATED / DO_NOT_PUBLISH_PRODUCTS`

2026-05-02 update: FlujoCRM was cleaned and rebuilt after this continuity note.
Use `docs\product\flujocrm-release-evidence-2026-05-02.md` for the current
source ZIP and installer hashes. The FlujoCRM hashes in this 2026-05-01 file are
historical only.

## Decision

The fast account/security items that the user took over are closed in the
tracker as user-owned: GitHub 2FA, Google Rapid Agent Hackathon cloud/video
steps, and historical secret rotation. Codex did not copy, store or verify
2FA factors, tax/bank/payout values, or secret values.

Commercial work continues locally:

- FlujoCRM is standalone first, Windows x64 first, bundle later.
- Wave FC is ready for private/local demo with synthetic data, not broad public
  publication.
- Product publication, Gumroad, deploys, social posts and broad releases remain
  blocked until a concrete product gate passes.

## FlujoCRM

Current state: `WINDOWS_FIRST_QA_PREP / PUBLICATION_BLOCKED`.

Evidence:

- `npm run check` in `apps\commercial\flujocrm` passed:
  `flujocrm main smoke passed` and `flujocrm preload smoke passed`.
- Installer exists:
  `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe`.
- Installer SHA256:
  `b7ba740ad82e976dd84fcfc959e78f9a9c9db50117cfcdf419fed106f664723f`.
- Authenticode status: `NotSigned`.
- Decision doc:
  `docs\product\flujocrm-windows-first-release-decision-2026-05-01.md`.

Open before sale:

- Clean install test on a fresh Windows user/VM.
- Final icon and unsigned-warning or code signing decision.
- Final legal/support/privacy/refund/terms review.
- Windows-first listing review.

Not active for initial release:

- macOS `.dmg`.
- `Pack Empresarial` bundle.
- Source ZIP as customer deliverable.

## Wave FC

Current state: `LOCAL_DEMO_READY / PUBLICATION_BLOCKED`.

Evidence:

- Focused Wave suite passed with `61 passed`.
- Evidence pack:
  `docs\WAVE_FC_EVIDENCE_PACK_2026-05-01.md`.
- Public-safe closure:
  `docs\product\wave-fc-public-safe-release-closure-2026-05-01.md`.
- Captures exist under:
  `qa_artifacts\2026-05-01-wave-fc-captures`.

Open before sale/publication:

- DOCX visual render QA when artifact-tool or LibreOffice is available.
- Final EULA/legal review.
- Installation/listing copy public-safe.
- ActionGate for a concrete channel.

Not active for current closure:

- Demo video, unless landing or Devpost reopens it as a requirement.

## Pending Projects After User-Owned Closure

1. FlujoCRM Windows clean install and final commercial gate.
2. Wave FC DOCX visual QA/legal/install/listing gate.
3. Puerto Observacionista reader/API lane with `ObservationEnvelope` and SQLite.
4. Obs Info Kernel / AIA validation on a small real corpus with low-claim copy.
5. Open-dev publication only if a concrete ActionGate approves the target.
6. Commercial legal matrix finalization before any paid app sale.
