# COMMERCIAL_AGENT_PUBLICATION_MATRIX_2026-05-02

Status: operational matrix for MEDIOEVO app-agents and Gumroad/website offers.

Rule: every app is positioned as a specialized agent, but only verified deliverables
can be sold as "buy now". Everything else is founder access, pilot interest or lab.

## Buyer-facing lanes

| lane | buyer label | allowed CTA | rule |
|---|---|---|---|
| BUY_NOW | Disponible ahora | Gumroad / checkout | Package exists, hash exists, secret/path/claims checks passed, public URL verified |
| FOUNDER_ACCESS | Acceso fundador | mailto/contact form | Product has local evidence but lacks clean-machine/legal/support/payment closure |
| PILOT_INTEREST | Piloto / lista de interes | contact | Concept or local demo exists; no paid delivery promise yet |
| LAB_FREE | Lab gratis | open web demo | Educational/synthetic demo only; no prediction, diagnosis or external automation claims |
| INTERNAL_ONLY | Interno / privado | none | Runtime, private game, TCG, sessions, credentials or unresolved private data |

## Current commercial matrix

| product | specialized agent | buyer-facing status | offer now | hard blocker before checkout/public download | next closure evidence |
|---|---|---|---|---|---|
| MEDIOEVO Agent Ops Pack | Agente Curador Datos | BUY_NOW | USD 29 Gumroad package with templates, checklists, curator report and support notes | Keep ZIP hash, support policy and website link synchronized | Verify Gumroad URL HTTP 200 and package SHA256 after every update |
| FlujoCRM | Agente Mercado | FOUNDER_ACCESS | Windows-first founder access by contact; demo can remain public | Clean-machine install, legal review and code-signing decision | Source ZIP rebuilt/scanned; Windows QA installer rebuilt/scanned; current-user install/launch/uninstall QA passed; installed UI writes to SQLite via E2E; unsigned/support/privacy/refund pilot copy drafted; clean VM remains open |
| Asistente Negocio | Agente Mostrador | FOUNDER_ACCESS | Windows founder access by contact; HTML preview demo can remain public | Clean-machine install, final legal/support review, code-signing certificate or approved unsigned-installer customer warning; no autonomous sending claims | Source ZIP rebuilt/scanned; Windows one-click installer built/scanned; current-user install/E2E/uninstall QA passed; package-final output includes installer, portable ZIP, demo, install notes, support/privacy/refund draft and checksums |
| Mini Office | Agente Oficina | FOUNDER_ACCESS | Contact only; no instant checkout | Legal review, clean-machine install, support/privacy/refund and checkout verification | Copy, license posture, install scripts and marketing generators cleaned on 2026-05-02; `python -m pytest -q` 22 passed; `mini_office.py --status` OK; manifest `blocked_count=0`; ZIP SHA256 `4315003693566D93F6F48DEF1C5EACE14BBE6531CEDFB878BE121699502D3710`; source/artifact secret scans 0 |
| Writer Workbench / Companero Escritura | Agente Editorial | FOUNDER_ACCESS | Request access; do not promise final paid bundle until package is verified | Delivery ZIP/build, export QA, editorial rights boundary | Export smoke, package hash and customer-facing scope |
| Wave Collapse | Agente Curador Documental | PILOT_INTEREST | Demo/product interest and setup conversation | Claims review, sanitized document tests, listing/legal final | Sanitized sample run with before/after evidence and rollback |
| Argus Desktop | Agente Consola | INTERNAL_ONLY / REVIEW | Internal wrapper candidate; no public checkout yet | Local route audit, private runtime boundary, UX review | Path audit, secret scan and public-safe feature map |
| DUAT Genesis | Agente Laboratorio | LAB_FREE / OPEN_CORE_LIVE | Free synthetic sandbox at `https://github.com/Lutren/duat-genesis` | Keep claims bounded to synthetic simulations; no DUAT Geodia private engine, no RPG/TCG and no science/medical/social prediction claims | Repo public URL HTTP 200; tests `3 passed`; ZIP SHA256 `f672d974d88c3190699ea16caad04b8a6de9839f20aa9513cfd7fdf51c0cbb44`; evidence `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json` |
| DUAT Templates | Agente Laboratorio | BUY_NOW | USD 19 Gumroad template pack at `https://lrgonzalez.gumroad.com/l/duat-templates` | Keep artifact hash, Gumroad listing and website links synchronized; no DUAT Geodia private engine, datasets, diagnosis or real-world prediction claims | Gumroad `published=true`; public URL HTTP 200; ZIP SHA256 `03c926b549307ef6106d80117183bb22121354671a10e0f2527473c06f6ca518`; evidence `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json` |
| GEODIA OMNIS | Agente Sociometro | INTERNAL_ONLY | Private scenario lab; no public checkout | Private Geodia boundary, data provenance, historical backtests, licensing and no human-society guarantee | `duat_omnis_v1.py` identified; next evidence is private offline fixture and deterministic replay |
| NEUROSTATE Dashboard | Agente Estado | LAB_FREE / BLOCKED_BY_SPLIT | Privacy-first demo/skeleton only | Privacy, medical/cognitive claims review, split from raw sources | Public-safe UI skeleton with no diagnosis wording |
| Claudio OS / Brain OS | Agente Sistema | PILOT_INTEREST / OPEN_CORE | Blueprint/open core and support conversation | ISO/QEMU/runtime proof and private boundary | Blueprint repo evidence plus no-private-runtime package |

## Website copy rules

- Use "Disponible ahora" only for Agent Ops Pack and DUAT Templates until another
  product has package evidence and checkout verification.
- Use "Acceso fundador" for products that can be discussed or manually delivered
  after review, but do not imply instant Gumroad delivery.
- Use "Lab gratis" for DUAT Genesis only; use "Piloto" for Wave and NEUROSTATE unless a
  specific paid package is created and verified.
- Keep DUAT Geodia/OMNIS private; public pages may describe the concept without
  engineering, code, fixtures or bridges.
- Keep the private RPG, TCG, Claudio runtime, sessions, credentials and customer
  data out of public listings and open-source packages.

## Next closure order

1. Keep Agent Ops Pack and DUAT Templates live and synchronized on website/Gumroad.
2. Keep DUAT Genesis repo copy low-claim and synchronized with website/software.
3. Close FlujoCRM and Asistente clean-VM/legal/support/signing evidence, then
   create the first paid app checkout.
4. Close Mini Office legal/clean-machine/package/support/privacy/refund gates before checkout.
5. Convert Writer Workbench into a founder-access package.
6. Keep Wave, OMNIS and NEUROSTATE as labs until falsification/privacy
   gates are documented.
