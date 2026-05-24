# Public Profile SEO Business Review - 2026-05-16

Status: `GITHUB_PROFILE_UPDATED / WEBSITE_LOCAL_HARDENED / WEBSITE_DEPLOY_REVIEW`

Scope: GitHub, GitHub Sponsors, LinkedIn, Gumroad, website SEO and commercial funnel for MEDIOEVO / Lutren.

Boundary: this run is authorized for public-surface changes, but secrets, private runtime, formulas, unpublished books, RPG/TCG assets/systems, account state and private patrimony remain blocked.

## Current Truth

| surface | result |
|---|---|
| `https://medioevo.space/` | HTTP `200` |
| `https://medioevo.space/robots.txt` | HTTP `200` |
| `https://medioevo.space/sitemap.xml` | HTTP `200` |
| `https://github.com/Lutren` | HTTP/API reachable; profile has 24 public repos and 13 followers |
| `https://github.com/sponsors/Lutren` | HTTP `200` |
| `https://github.com/Lutren/Lutren` | HTTP `200` |
| `https://lrgonzalez.gumroad.com/` | HTTP `200` |
| `https://lrgonzalez.gumroad.com/l/medioevo-agent-ops-pack` | HTTP `200` |
| `https://lrgonzalez.gumroad.com/l/duat-templates` | HTTP `200` |
| LinkedIn candidate URLs | public GET returns LinkedIn `999`; authenticated owner view still required |

## Implemented

### GitHub Profile

Updated live profile README in `Lutren/Lutren` with a `Start Here` block:

- public tools -> `https://medioevo.space/software.html`;
- products -> `https://lrgonzalez.gumroad.com`;
- recurring support -> `https://github.com/sponsors/Lutren`;
- author/boundary -> `https://medioevo.space/about.html`.

Commit:

```text
10f103834e1d72895ce73fb1511fe1ebf715d954 Improve profile start routes
```

Verification:

- raw README contains `## Start Here`;
- raw README contains `https://lrgonzalez.gumroad.com`;
- raw README contains `The private layer stays private`;
- focused profile SecretScan: `count_reported=0`;
- `git diff --check`: no whitespace errors.

### Website Local Hardening

Local files changed in `publish_staging/medioevo-site`:

- added `Start here` and `Saga` to home navigation;
- added `start-here.html` and `saga.html` to sitemap;
- removed `play-medioevo.html` from sitemap;
- removed direct homepage CTAs to `play-medioevo.html`;
- added `noindex,nofollow` to `play-medioevo.html`;
- improved `about.html` JSON-LD/social routes;
- updated `structured-data-profile.jsonld` with Gumroad and date;
- lowered `company.md` claims from broad archive claims to public-safe route language;
- disabled direct Stripe checkout locally and routes checkout requests to Gumroad while the product allowlist is reconciled.

Website QA:

- SEO audit on `publish_staging/medioevo-site`: all checks `OK`, no major findings;
- sitemap XML parse: OK;
- profile JSON-LD parse: OK;
- `about.html` JSON-LD parse: OK;
- JS syntax: `stripe-store.js`, `functions/api/create-checkout.js`, `netlify/functions/create-checkout.js` OK;
- private-route grep: no direct `play-medioevo`, `Abrir RPG` or `Entrar al RPG` remains in home/sitemap.

Website deploy decision:

`REVIEW`, not deployed in this run. Reason: full site SecretScan still reports four review findings from existing public auth/checkout filenames/content markers and two image filenames containing `secreto`. No private value was printed or detected by the focused literal-pattern grep, but the full deploy target needs a dedicated deploy allowlist or asset rename pass before live publication.

### Gumroad / Business

Live Gumroad surfaces remain reachable. No Gumroad listing, price, file upload or product metadata was changed in this run.

Business reading:

- Gumroad remains checkout/delivery, not the discovery engine.
- GitHub profile now routes more clearly to public tools, store and Sponsors.
- Website staging now reduces exposure of private game/editorial material and points uncertain checkout to the official Gumroad store.

### LinkedIn

No LinkedIn edit was attempted. Both known candidate URLs return LinkedIn `999` from unauthenticated public checks. The profile copy remains paste-ready, but canonical URL and live edit require authenticated owner view.

## Scan Summary

| scan | result |
|---|---|
| GitHub profile SecretScan | `PASS`, `count_reported=0` |
| GitHub profile boundary grep | `PASS`, only boundary/negative-claim sections matched |
| Website SEO audit | `PASS` |
| Website syntax | `PASS` |
| Website full SecretScan | `REVIEW`, 4 findings |
| LinkedIn public verification | `REVIEW`, public access blocked by LinkedIn `999` |

## Business Recommendations

1. Keep GitHub as trust/proof: README, repos, Sponsors, tests and claim boundaries.
2. Keep website as the canonical hub: books, software, author, public boundary and store route.
3. Keep Gumroad as the checkout target until Stripe product allowlist, legal/support and private-boundary review are clean.
4. Do not publish direct RPG/TCG/game checkout paths until a private-to-public teaser policy is explicitly approved.
5. Confirm LinkedIn from authenticated owner view, then paste the prepared headline/about/featured links.

## Next Exact Step

Create a clean website deploy allowlist or deploy package that excludes `netlify/functions/node_modules`, reviews `medioevo-auth.js`, `stripe-store.js`, renames the two `*_secreto.*` public image filenames, and keeps `play-medioevo.html` out of sitemap/search.
