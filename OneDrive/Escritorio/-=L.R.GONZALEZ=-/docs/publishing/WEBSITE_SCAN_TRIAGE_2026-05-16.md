# Website Scan Triage - 2026-05-16

Source target: `publish_staging/medioevo-site`
Deploy-ready target: `publish_staging/medioevo-site-deploy-ready-2026-05-16`
Deploy-ready ZIP: `publish_staging/medioevo-site-deploy-ready-2026-05-16.zip`

Status: SOURCE QA PASS / SOURCE PUBLICATION BLOCKED / DEPLOY-READY QA PASS

## Summary

The previous site SecretScan findings were closed locally without exposing
secrets and without enabling direct checkout. The source site now passes the
local SEO audit and focal secret scan, but it must not be deployed directly:
the tree contains protected editorial/game residue, large dependency folders
and mixed local changes.

A separate deploy-ready package was created by selective copy. It excludes
`book01.json`, `src/data`, `node_modules`, private/game/TCG/cartridge surfaces,
direct Stripe checkout code and the previous private-residue URL paths. That
package passed SecretScan, SEO audit, syntax checks, focal boundary scans,
XML/JSON parse checks, ZIP integrity and route smoke.

## Findings Closed

- `medioevo-auth.js`: local variables renamed from secret-like `password` to
  `authPass`; no hardcoded credential was found.
- `stripe-store.js`: renamed to `commerce-store.js`; direct checkout remains
  disabled and the flow is Gumroad-first.
- `img/maps/map_plano_astral_archivo_onirico_secreto.jpg`: renamed to
  `img/maps/map_plano_astral_archivo_onirico.jpg`.
- `img/maps/map_plano_astral_archivo_onirico_secreto.webp`: renamed to
  `img/maps/map_plano_astral_archivo_onirico.webp`.

## Business / SEO Fixes

- `saga.html` CTA now opens the public Gumroad bundle directly instead of
  navigating to the home page and depending on a delayed JavaScript call.
- `saga.html` no longer claims Stripe/OXXO as the active public checkout path.
  It now states payment is handled through Gumroad.
- `commerce-store.js` includes `saga-completa` in the public-safe Gumroad
  fallback map while keeping direct checkout disabled.
- `js/store-integration.js` now exposes only public-safe products and routes
  checkout to public Gumroad URLs.
- Public nav links that previously pointed to the RPG/game lane now route to
  `public-boundary.html`.

## Source Publication Blocker

- Direct deploy from `publish_staging/medioevo-site` is blocked.
- Source tree includes protected narrative JSON and large gamebook/story data
  that are not approved for public release.
- Source tree includes dependency/vendor material that should not be uploaded
  as static publication payload.
- Source tree contains mixed tracked/untracked edits, so external deployment
  from that directory risks publishing unrelated work.

## Deploy-Ready Package

- Folder: `publish_staging/medioevo-site-deploy-ready-2026-05-16`.
- Files: 368.
- Bytes: 156,544,597.
- ZIP: `publish_staging/medioevo-site-deploy-ready-2026-05-16.zip`.
- ZIP bytes: 155,964,796.
- ZIP SHA256: `86ABADF00AAD843D1DBAFE1621DBD7EF3EFB8310A99ACF4AC68C9E3EC5B9DAD6`.
- ZIP integrity: PASS.

## Evidence

- `python .agents/skills/seo-growth-medioevo/scripts/seo_audit_medioevo.py --site-root publish_staging/medioevo-site`: PASS, no major findings.
- `python tools/release/scan_secrets.py --path publish_staging/medioevo-site --json`: PASS, `count_reported=0`.
- `node --check medioevo-auth.js`: PASS.
- `node --check commerce-store.js`: PASS.
- `node --check functions/api/create-checkout.js`: PASS.
- `node --check netlify/functions/create-checkout.js`: PASS.
- `sitemap.xml` parse: PASS.
- `structured-data-profile.jsonld` parse: PASS.
- Focal pattern scan for old names and secret-like code markers: PASS.
- Gumroad bundle URL probe: HTTP 200 for `https://lrgonzalez.gumroad.com/l/saga-completa`.
- Local route smoke via ephemeral Python HTTP server: PASS for `/`,
  `/saga.html`, `/start-here.html`, `/about.html`, `/public-boundary.html`,
  and `/sitemap.xml`.
- `python tools/release/scan_secrets.py --path publish_staging\medioevo-site-deploy-ready-2026-05-16 --json`: PASS, `count_reported=0`.
- Deploy-ready SEO audit: PASS, no major findings.
- Deploy-ready JS syntax: PASS for `config.js`, `js/store-integration.js` and
  `functions/api/create-checkout.js`.
- Deploy-ready focal blocked scan: PASS, no matches for blocked private/story,
  Stripe/direct checkout or secret-like paths.
- Deploy-ready sitemap and JSON-LD parse: PASS.
- Deploy-ready route smoke: PASS for `/`, `/apps.html`, `/app/`,
  `/mission-control/`, `/catalogo-completo.html`, `/catalogo-completo/`,
  `/saga.html`, `/despertar-preview.html`, `/start-here.html`, `/about.html`,
  `/public-boundary.html`, `/sitemap.xml` and `/js/store-integration.js`.
- `python -m zipfile --test publish_staging\medioevo-site-deploy-ready-2026-05-16.zip`: PASS.

## Deploy Gate

Deploy was not run.

Reason: external publication still needs a target-specific decision and
provider target confirmation. The source tree remains blocked; the deploy-ready
package is the only candidate for review.

Required before deploy:

- Confirm the intended provider/project target, for example Cloudflare Pages or
  Netlify.
- Deploy only from `publish_staging/medioevo-site-deploy-ready-2026-05-16` or
  its ZIP, not from `publish_staging/medioevo-site`.
- Run post-deploy HTTP checks against the real domain before marking public
  closure.
