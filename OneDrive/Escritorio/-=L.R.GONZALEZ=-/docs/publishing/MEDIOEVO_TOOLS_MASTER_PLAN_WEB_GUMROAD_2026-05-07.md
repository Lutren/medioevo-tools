# MEDIOEVO Tools Master Plan - web and Gumroad publication

Date: 2026-05-07

Status: `WEBSITE_LIVE / GUMROAD_UPDATED / EXTERNAL_VERIFIED`

## Scope

This pass published public-safe copy for the MEDIOEVO Tools master plan:

- a Spanish website post,
- an English website mirror,
- blog index links,
- sitemap entries,
- `publicacion.html` surface link,
- Gumroad description updates for `MEDIOEVO Agent Ops Pack`,
- Gumroad description updates for `DUAT Templates`.

The copy presents the long-range plan as a vision and roadmap, not as a shipped
feature or guaranteed commercial promise. It explicitly keeps hardware delivery,
autonomous safety, embodiment and the one-year prototype horizon as future/gated
work.

## Live URLs

- Spanish post: `https://medioevo.space/blog/medioevo-tools-plan-maestro.html`
- English post: `https://medioevo.space/blog/en/medioevo-tools-master-plan.html`
- Public map: `https://medioevo.space/publicacion.html`
- Sitemap: `https://medioevo.space/sitemap.xml`
- Gumroad Agent Ops Pack: `https://lrgonzalez.gumroad.com/l/medioevo-agent-ops-pack`
- Gumroad DUAT Templates: `https://lrgonzalez.gumroad.com/l/duat-templates`

## Files Changed

- `-=MEDIOEVO=-\-=LIBROS\claudio\website\blog\medioevo-tools-plan-maestro.html`
- `-=MEDIOEVO=-\-=LIBROS\claudio\website\blog\en\medioevo-tools-master-plan.html`
- `-=MEDIOEVO=-\-=LIBROS\claudio\website\blog\index.html`
- `-=MEDIOEVO=-\-=LIBROS\claudio\website\blog\en\index.html`
- `-=MEDIOEVO=-\-=LIBROS\claudio\website\sitemap.xml`
- `-=MEDIOEVO=-\-=LIBROS\claudio\website\publicacion.html`
- `packages\paid\medioevo-agent-ops-pack\commerce\gumroad_listing.json`
- `packages\paid\duat-templates\commerce\gumroad_listing.json`

## Gate Evidence

- `pending_review`: `active_dedup=0`, `claudio_open=0`.
- SEO audit for canonical website source: no major findings.
- Focused secret scan for changed website and Gumroad listing files:
  `count_reported=0`.
- `git diff --check` on the changed scope: no whitespace errors.
- Website ActionGate: `public_publish`, target `medioevo-site-deploy`,
  decision `46ea16ef-f1d7-4715-a01d-daafc529d240`, `pass`.
- Gumroad target ActionGates initially passed while host was `APPROVE`.
- During the actual Gumroad publisher run, host recalculated to `REVIEW`; the
  built-in `owner_override_with_evidence` was applied for host `REVIEW` only.
- No Gumroad product ZIP was uploaded: `with_file_requested=false` for both
  product updates.

## Publication Evidence

Cloudflare Pages deployment:

- command: `npx wrangler pages deploy . --project-name medioevo-site --branch main --commit-dirty=true --commit-message "Add MEDIOEVO Tools master plan"`
- preview URL: `https://869b5d23.medioevo-site.pages.dev`
- production custom domain verification: `https://medioevo.space/...` returned
  HTTP `200` for the new pages and sitemap.

Gumroad API updates:

- `MEDIOEVO Agent Ops Pack`: `operation=update_product`, `published=true`,
  `ok=true`, evidence:
  `qa_artifacts\release_validation\gumroad-medioevo-agent-ops-pack.json`.
- `DUAT Templates`: `operation=update_product`, `published=true`, `ok=true`,
  evidence:
  `qa_artifacts\release_validation\gumroad-duat-templates.json`.

Public HTTP verification:

- Spanish post: HTTP `200`, title marker present, prototype-plan marker present.
- English post: HTTP `200`, title marker present, non-promise marker present.
- Sitemap: HTTP `200`, both new URLs present.
- Public map: HTTP `200`, master-plan card and link present.
- Gumroad Agent Ops Pack: HTTP `200`, plan link present, MEDIOEVO Tools marker
  present, hardware/one-year boundary markers present.
- Gumroad DUAT Templates: HTTP `200`, plan link present, MEDIOEVO Tools marker
  present, hardware/one-year boundary markers present.

## Boundaries

- No book content was published.
- No private game material was published.
- No OS internals, raw DUAT internals, Observacionismo raw canon,
  Observacionismo Inverso raw canon or private information-theory material was
  published.
- No claim was made that the cafe/display/embodiment/robotics plan already
  exists as a finished product.
- No brand affiliation was claimed for the cafe example.

## Final Host State

The final host check after publication and documentation was
`CONTAMINADO/REVIEW`, `R=0.579`, `Phi_eff=0.421`, `lambda_sat=0.912`. The live
publication is already verified, but no additional external action should be
chained without a fresh target-specific ActionGate.

## Next Safe Step

Create a short social/link post that points to the live Spanish and English
posts, but only after a fresh target-specific ActionGate for the social surface.
