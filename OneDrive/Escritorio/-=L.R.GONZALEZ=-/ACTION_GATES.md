# ACTION_GATES

## 2026-05-22 - Fragmentos Cover Asset Gate

- Create local validator script/test/manifest/report:
  APPROVE_LOCAL_REVIEW_TOOLING.
- Validate current Fragmentos manifest with no asset:
  REVIEW_ASSET_MISSING.
- Any real image generation or asset selection:
  REVIEW_ASSET_PRODUCTION.
- Asset provenance/license confirmation:
  REVIEW_LICENSE_PROVENANCE.
- Metadata strip after asset selection:
  REVIEW_LOCAL_ASSET_HARDENING.
- KDP, Gumroad, web, social, push, deploy, public ZIP or external release:
  BLOCK_PUBLICATION.

## 2026-05-22 - Human Gate Packet + Fragmentos Cover Brief

- Human publication gate packet docs/JSON: APPROVE_LOCAL_METADATA.
- Fragmentos public-safe cover brief docs/JSON: APPROVE_LOCAL_BRIEF.
- Real cover generation or asset selection: REVIEW_ASSET_PRODUCTION.
- Public staging allowlisted folder: REVIEW_PUBLIC_STAGING.
- KDP, Gumroad, web, social, push, deploy, public ZIP or external release:
  BLOCK_PUBLICATION.

## 2026-05-22 - Editorial Word/PDF Full-Page QA

- Microsoft Word COM read-only invisible export from private DOCX to internal
  QA PDF: APPROVE_LOCAL_TOOLING.
- PyMuPDF/PIL render and automated image-metric QA over all pages:
  APPROVE_LOCAL_EVIDENCE.
- Contact sheets for internal review: APPROVE_LOCAL_PRIVATE_QA.
- Human editorial/store/print decision: REVIEW_HUMAN_EDITORIAL.
- KDP, Gumroad, web, social, push, deploy, public ZIP or external release:
  BLOCK_PUBLICATION.

## 2026-05-22 - Fragmentos/Calibracion Internal Exports

- Copy canon10 integrated Fragmentos artifacts into
  `books\editorial\internal_exports\FRAGMENTOS_INTERNAL_EXPORT_2026-05-22`:
  APPROVE_LOCAL_EDITORIAL_INTERNAL.
- Copy canon10 integrated Calibracion artifacts into
  `books\editorial\internal_exports\CALIBRACION_INTERNAL_EXPORT_2026-05-22`:
  APPROVE_LOCAL_EDITORIAL_INTERNAL.
- Generate local EPUBs from integrated HTML with Calibre `ebook-convert`:
  APPROVE_LOCAL_TOOLING.
- Hash manifests and README files inside internal packages:
  APPROVE_LOCAL_EVIDENCE.
- Public upload, KDP, Gumroad, deploy, social post, git push or public ZIP
  from these packages: BLOCK_PUBLICATION.
- Treat all `internal_exports` full manuscript files as private editorial
  material: BLOCK_PUBLIC_REDISTRIBUTION.

## 2026-05-15 - Local Queue Closeout LEVEL 4.5

- Local docs/reports/tests/fixtures sanitizados: APPROVE.
- R/Phi runtime episode and calibration: APPROVE.
- DUAT_WDI_BACKTEST_DRY_RUN_v0_9: REVIEW_INTERNAL_ONLY.
- WDI legal/comparability: REVIEW.
- Publishing metadata sprint for Deriva/Fragmentos/Calibracion: REVIEW_METADATA_ONLY.
- Book publication/upload/store edits: BLOCK_PUBLICATION.
- MTS v0.4 synthetic preregistration and local evaluation: APPROVE_LOCAL_SYNTHETIC.
- MTS real sensors, personal data, model changes, label changes or holdout recalibration: BLOCK.
- Git push/deploy/Gumroad/KDP/social release/public ZIP: BLOCK.

Worst gate wins: any external or public action remains blocked until human/legal/commercial review passes and a new explicit gate opens.

## CLAUDIO_PROVIDER_AND_GITLEAKS_PORTABLE_REVIEW_v0_1 - 2026-05-16

- DeepSeek: deepseek-4 -> deepseek-v4-flash, status REVIEW_MODEL_ALIAS_RESOLVED_LOCAL; live smoke REVIEW_BILLING_OR_QUOTA; no secret values printed.
- Gitleaks: portable local v8.30.1 installed under BRAIN_OS tools, official ZIP checksum matched, binary SHA256 $(@{available=True; binary_path=C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\tools\security\gitleaks\gitleaks.exe; binary_sha256=17157e2ee8b76fc8b1d8bee607a250e34b8a8023c8bc81822d4b5ee4d78fcb7c; install_mode=PORTABLE_LOCAL; ok=True; product_publication=REVIEW_OR_BLOCK; publication_gate=BLOCK; secret_values_printed=False; status=ADOPT_LOCAL_TOOL; version=8.30.1}.binary_sha256).
- POC-01 rerun: fixtures only, Gitleaks findings 0, MEDIOEVO minimal findings 7; use as companion tool, not replacement.
- PublicationGate: BLOCK.
- Artifacts: $qa\HANDOFF_CLAUDIO_PROVIDER_GITLEAKS_REVIEW_v0_1.md, $qa\CLAUDIO_PROVIDER_GITLEAKS_REVIEW_v0_1_QA_SUMMARY.json, $poc\reports\POC-01_GITLEAKS_PORTABLE_COMPARISON_REPORT.md.

## 2026-05-17 - PENDIENTES_MASTER reconciliation

- `PENDIENTES_MASTER.md` reconciliation docs and local review packet: APPROVE_LOCAL_DOCS.
- WDI methodology governance: CLOSED_LOCAL_REVIEW, while WDI redistribution/public claims remain REVIEW_EXTERNAL.
- Deriva/Fragmentos/Calibracion review packet: APPROVE_LOCAL_REVIEW_PACKET_ONLY.
- Final exports, KDP-ready covers, store pages and storefront copy: REVIEW_ASSET_PRODUCTION.
- Book upload, KDP, Gumroad, deploy, git push, social post or public ZIP: BLOCK_PUBLICATION.
- Manuscripts, private canon, secrets, tokens and sensitive local routes: BLOCK_PRIVACY.
- MTS real sensors, personal data, telemetry, camera, microphone, location or biometrics: BLOCK_MTS_REAL_DATA.

## 2026-05-17 - Deriva Internal Export

- Copy canon10 integrated Deriva artifacts into `books\editorial\internal_exports\DERIVA_INTERNAL_EXPORT_2026-05-17`: APPROVE_LOCAL_EDITORIAL_INTERNAL.
- Generate local EPUB from integrated HTML with Calibre `ebook-convert`: APPROVE_LOCAL_TOOLING.
- Hash manifest and README inside internal package: APPROVE_LOCAL_EVIDENCE.
- Secret scan focal over internal package: APPROVE_LOCAL_SCAN, result `count_reported=0`.
- Public upload, KDP, Gumroad, deploy, social post, git push or public ZIP from this package: BLOCK_PUBLICATION.
- Treat full manuscript files in `internal_exports` as private editorial material: BLOCK_PUBLIC_REDISTRIBUTION.
