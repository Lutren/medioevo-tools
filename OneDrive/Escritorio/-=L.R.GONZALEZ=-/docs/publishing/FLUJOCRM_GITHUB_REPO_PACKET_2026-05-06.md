# FlujoCRM GitHub Repo Packet - 2026-05-06

Estado: `READY_LOCAL_PACKET / DO_NOT_PUSH`

Este paquete deja listo el contenido operacional para publicar FlujoCRM en
GitHub cuando pasen licencia, host y ActionGate. No crea remoto, no hace push y
no cambia la licencia.

## Target

- Owner: `Lutren`
- Repo recomendado: `flujocrm`
- Ruta local publicable, cuando pase gate:
  `publish_staging\github\flujocrm-free-review`
- Estado actual: repo Git local limpio, commit `a16c019`, sin remoto.

## GitHub Metadata

Description:

```text
Local-first desktop CRM for contacts, pipeline stages and follow-up notes.
```

Website:

```text
https://medioevo.space/software.html
```

Topics:

```text
crm
desktop-app
electron
local-first
sqlite
small-business
pipeline
productivity
medioevo
```

Social preview note:

```text
Use a product screenshot only after the staging license is decided and the repo
is public. Do not use private MEDIOEVO, Claudio runtime, book, RPG/TCG or
account screenshots.
```

## Public Release Notes Draft

```md
# FlujoCRM initial free source release

FlujoCRM is a local-first desktop CRM for contacts, pipeline stages and
follow-up notes.

This first public source release focuses on a small, inspectable desktop app:

- Electron shell
- local business workflow
- contact and pipeline surfaces
- smoke checks for main, preload and renderer entry points
- explicit public/private boundary docs

Not included:

- hosted cloud service
- team sync
- private MEDIOEVO runtime
- unreleased books
- RPG/TCG material
- credentials, customer data or account state

Support, setup help, templates, installers and premium workflows may live in
Gumroad or Sponsors around the free source.
```

## GitHub First Issue Draft

```md
# Post-release hardening checklist

- LOCAL_PREFLIGHT_DONE / POST_PUBLICATION_RECHECK_REQUIRED: Re-run secret scan
  after publication. Local 2026-05-21 scan returned `count_reported=0`.
- REVIEW_REQUIRED_AFTER_PUBLICATION: Verify GitHub repo files match the final
  local staging manifest.
- REVIEW_REQUIRED_AFTER_VISUAL_QA: Add screenshots after public-safe visual QA.
- DONE_LOCAL: Add install notes for Windows-first local use.
  `CUSTOMER_INSTALL_NOTES.md` exists in staging.
- REVIEW_REQUIRED_AFTER_PUBLICATION: Confirm the website points to the final
  GitHub URL.
- LOCAL_PREFLIGHT_DONE / POST_PUBLICATION_RECHECK_REQUIRED: Keep private
  MEDIOEVO/Claudio/runtime/book/RPG material out of repo. Local secret scan
  returned `count_reported=0`; remaining MEDIOEVO/Claudio/RPG text hits are
  boundary statements, not private content payloads.
```

Local preflight continuation:
`docs\publishing\FLUJOCRM_GITHUB_LOCAL_PREFLIGHT_2026-05-21.md`.

## Commands - Blocked Until Gate

Do not run these while ActionGate blocks the target.

```powershell
cd publish_staging\github\flujocrm-free-review
gh repo create Lutren/flujocrm --public --source . --remote origin --description "Local-first desktop CRM for contacts, pipeline stages and follow-up notes."
git push -u origin main
gh repo edit Lutren/flujocrm --homepage "https://medioevo.space/software.html" --add-topic crm --add-topic desktop-app --add-topic electron --add-topic local-first --add-topic sqlite --add-topic small-business --add-topic pipeline --add-topic productivity --add-topic medioevo
```

## Required Preflight Before Running

```powershell
python tools\release\audit_flujocrm_free_license_readiness.py --write --json
python tools\release\scan_secrets.py --path publish_staging\github\flujocrm-free-review --json
npm --prefix publish_staging\github\flujocrm-free-review run check
python tools\action_gate_cli.py public_publish --target github-flujocrm-free-release --external-authorized --evidence-ref flujocrm-free-license-readiness
```

Required truth before publication:

- `publication_ready=true`
- secret scan `count_reported=0`
- `npm run check` passed
- ActionGate `github-flujocrm-free-release` allowed
- `git status --short` in staging empty
- no remote already configured unless intentionally verified

## Current Block

Current license readiness is `publication_ready=true`. External publication is
still blocked by ActionGate/host, decision
`efb26b49-6e6a-4dee-b8db-a9e5e6e685fb`.
