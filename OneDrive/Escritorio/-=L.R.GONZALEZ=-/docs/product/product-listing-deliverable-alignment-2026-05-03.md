# Product Listing Deliverable Alignment - 2026-05-03

Status: `LISTINGS_ALIGNED_TO_REAL_DELIVERABLES / NEW_SALES_STILL_GATED`

This file is the working boundary between a buyer-facing listing and the thing
that can actually be delivered today. It does not publish, upload, push or
change any store listing.

## Rule

Every listing must point to one real delivery lane before sale:

- `published_artifact`: already published and verified.
- `founder_access_only`: buyer can get guided access/support, but not a public
  download checkout yet.
- `private_demo_only`: demo can be shown with synthetic or authorized data, but
  no public sale/download yet.
- `draft_blocked`: product idea exists, but the deliverable is not verified.

Source ZIPs under `releases\paid-apps` are internal QA artifacts by default.
They are not customer downloads unless a separate license, support boundary and
release gate explicitly approve source delivery.

## Current Alignment

| Listing | Current buyer-facing lane | Real deliverable now | Evidence | Decision |
|---|---|---|---|---|
| MEDIOEVO Agent Ops Pack | Gumroad published | `published_artifact`: `releases\paid\medioevo-agent-ops-pack.zip` | SHA256 `7cf8fdf5c8da49d691947becebdd3feae5f93b7e062212af38e3063404fab948`; live evidence `qa_artifacts\release_validation\publication-live-verification-2026-05-02.json`; manifest `release_manifests\medioevo-agent-ops-pack.json` has `file_count=10`, `blocked_count=0` | keep published; monitor support and keep hash synchronized |
| DUAT Templates | Gumroad published | `published_artifact`: `releases\paid\duat-templates.zip` | SHA256 `03c926b549307ef6106d80117183bb22121354671a10e0f2527473c06f6ca518`; live evidence `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json`; manifest `release_manifests\duat-templates.json` has `file_count=8`, `blocked_count=0` | keep published as synthetic templates only |
| FlujoCRM | founder access / website contact first | `founder_access_only`: Windows app with local QA evidence; source ZIP remains internal QA | `releases\paid-apps\flujocrm.zip` SHA256 `39b40abbedef13e6561beadf0a95ba4f1f546f9bed4a7c9808ecd2be40029a76`; manifest `file_count=20`, `blocked_count=0`; current-user install and SQLite QA evidence exist under `qa_artifacts\flujocrm_*` | no Gumroad/public checkout until clean-machine install, legal review and signing/unsigned decision |
| Asistente Negocio | founder access / website contact first | `founder_access_only`: Windows installer/package evidence; source ZIP remains internal QA | `releases\paid-apps\asistente-negocio.zip` SHA256 `c2a73e1b82db8b1174164398a4ce27c3bbbe42b817ef2b5a887bf95b1b10f423`; manifest `file_count=37`, `blocked_count=0`; install evidence under `qa_artifacts\asistente_negocio_windows_install_2026-05-02-r2` | no public checkout until clean-machine install, legal review and signing/unsigned decision |
| Mini Office | founder access review | `founder_access_only`: local runtime/package evidence; source ZIP remains internal QA | `releases\paid-apps\mini-office.zip` SHA256 `4315003693566d93f6f48def1c5eace14bbe6531cedfb878be121699502d3710`; manifest `file_count=53`, `blocked_count=0`; cleanup evidence `qa_artifacts\release_validation\mini-office-cleanup-2026-05-03.json` | no Gumroad/public checkout until legal review, clean-machine install, support/privacy/refund and checkout verification |
| Argus Desktop | internal/commercial review | `draft_blocked`: internal app artifact only | `releases\paid-apps\argus-desktop.zip` SHA256 `b8b8bf292e4d72267a6c3a6683cf759e5b60f514e4c710f5880e5770f0c9bbfb`; manifest `file_count=52`, `blocked_count=0` | do not list as customer download until UX/public-safe review and final package gate |
| Wave FC | pilot interest only | `private_demo_only`: synthetic local demo/evidence pack | `docs\product\wave-fc-public-safe-release-closure-2026-05-01.md`; `docs\WAVE_FC_EVIDENCE_PACK_2026-05-01.md`; captures under `qa_artifacts\2026-05-01-wave-fc-captures`; focused suite previously `61 passed` | no public sale until DOCX visual QA, EULA/legal, install/listing copy and ActionGate |
| MEDIOEVO Starter Pack | draft/review | `draft_blocked`: existing ZIP detected but not verified for sale | `GUMROAD_PRODUCTS.md` marks review; large ZIPs are called out in `DUPLICATES_AND_DEAD_CODE.md` | generate manifest/hash and editorial rights boundary before listing |
| MEDIOEVO Ultimate Archive | draft/review | `draft_blocked`: existing huge ZIP detected but not verified for sale | `GUMROAD_PRODUCTS.md` marks review; large archive risk is in `RISK_REGISTER.md` and `DUPLICATES_AND_DEAD_CODE.md` | do not sell until rights, contents, size, support and sample boundary are reviewed |
| EL OBSERVADOR ebook | draft | `draft_blocked`: manuscript/export not approved here | `GUMROAD_PRODUCTS.md` marks legal/editorial review | approve final manuscript and sample boundary before listing |
| Brain OS Companion PDF | draft | `draft_blocked`: companion product not packaged in this pass | `GUMROAD_PRODUCTS.md` marks draft | pair only with verified blueprint/docs and low-claim copy |
| ResidueOS Pro Templates | draft | `draft_blocked`: product definition not closed | `GUMROAD_PRODUCTS.md` marks draft | create paid template allowlist before listing |
| Claudio Special Agent Pack | draft | `draft_blocked`: premium pack not separated from private/runtime/vendor material | `GUMROAD_PRODUCTS.md` marks draft | create clean package allowlist and scan before listing |
| MEDIOEVO Writer Toolkit | draft | `draft_blocked`: writer deliverable not aligned to a package here | `GUMROAD_PRODUCTS.md` marks draft | define app/templates package and editorial rights boundary |
| Developer Lifetime Bundle | draft | `draft_blocked`: bundle depends on several products still gated | `GUMROAD_PRODUCTS.md` marks draft | only sell after included products have independent deliverables |
| NEUROSTATE UI | blocked by split | `draft_blocked`: no public medical/cognitive claim surface | `GUMROAD_PRODUCTS.md` marks blocked by split | privacy and no-diagnosis review required before any public listing |

## Buyer-Facing Copy Guard

Allowed for published artifacts:

- "includes the ZIP/artifact listed in this product";
- "synthetic templates";
- "support notes and checklists";
- "human-reviewed setup or implementation help".

Allowed for founder/private demo lanes:

- "founder access";
- "private demo";
- "guided setup";
- "available after install/legal/support review";
- "request access".

Blocked unless a later gate approves:

- "instant download" for FlujoCRM, Asistente Negocio, Mini Office, Argus or
  Wave FC;
- "source code included" for commercial apps;
- "production-ready SaaS";
- guaranteed safety, guaranteed anti-hallucination, medical/legal/financial
  advice, or autonomous external action.

## Next Closures

1. FlujoCRM: clean-machine Windows smoke, legal/support finalization and
   unsigned/signing decision.
2. Asistente Negocio: clean-machine smoke, legal/support finalization and
   unsigned/signing decision.
3. Mini Office: clean-machine install, legal/support/privacy/refund and checkout
   verification.
4. Wave FC: DOCX visual render QA, EULA/legal and concrete listing ActionGate.
5. Draft bundles/books: manifest/hash plus rights boundary before any listing.
