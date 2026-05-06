# Open Source Max + Patrimony Guard

Status: implementation control, not publication proof.

## Decision

Open source as much as possible, but do not destroy family patrimony, privacy or security.

Open:

- developer tools;
- schemas and validators;
- CLIs;
- synthetic examples;
- benchmarks;
- whitepapers;
- generic curador workflow;
- ActionGate and evidence patterns.

Protect:

- MEDIOEVO books and full canon;
- RPG, TCG, WorldPulse runtime, assets, scenes and scripts;
- commercial app binaries, installers and premium templates;
- private prompts, sessions, tokens and account data;
- brand, domains, monetization assets and family succession instructions.

## Repo Lanes

| repo | lane | license default | publish condition | monetize by |
|---|---|---|---|---|
| `data-curation-observatory` | open | MIT or Apache-2.0 | synthetic demo, no user paths, no private data | premium templates, audits, support |
| `residueos-core` | open core | MIT or Apache-2.0 | tests, DEMO_ONLY thresholds, no private data | integrations, hosted gate, support |
| `ai-web-gateway-observacionista` | protective open | AGPL-3.0 or Apache-2.0 + commercial option | no credentials, no unsafe browser action, MCP docs | commercial license, hosted service |
| `obs-info-kernel-lite` | open research/toolkit | Apache-2.0 or MIT after review | synthetic corpus, low-claim `CLAIMS.md` | consulting, research templates |
| `observational-calibration-toolkit` | open | MIT or Apache-2.0 | schemas/tests/falsifiers, no physics claim | workshops, premium dashboards |
| `duat-genesis` | open research sandbox | MIT now / Apache-2.0 optional later | synthetic simulator only, no DUAT Geodia private engineering, no RPG/canon/assets, no physics proof claim | research templates, workshops, private lab setup |
| `duat-geodia` | private research/runtime | proprietary/private | no public code; may be described low-claim | private lab, RPG living-world integration, internal research |
| `neurostate-ui` | guarded local prototype | license review required | split from raw mixed source; privacy/claims review; no medical claim | local dashboard, integrations, private setup |
| `la-biblioteca-de-alejandria` | public index | CC BY-SA for docs | links only to sane repos | Sponsors, lead gen |

## Minimum Repo Contract

Every public repo must include:

- `README.md`;
- `LICENSE`;
- `CLAIMS.md`;
- `PRIVATE_EXCLUSIONS.md`;
- `SECURITY.md`;
- tests or a reproducible demo;
- synthetic fixtures only;
- no local paths;
- no secrets;
- no full books;
- no RPG/private assets.

## First Implementation Order

1. `data-curation-observatory`: lowest technical and legal risk; directly matches curador.
2. `residueos-core`: useful ActionGate package; keep thresholds `DEMO_ONLY`.
3. `ai-web-gateway-observacionista`: docs and interface first, implementation second.
4. `obs-info-kernel-lite`: only after claims and license review.
5. `observational-calibration-toolkit`: publish schemas and falsifiers before complex math.

## Blockers

- `Downloads\r.txt` is `USER_ASSERTED_SAFE_NON_BLOCKING`; keep it out of staging and rely on allowlist secret scans.
- No external push until ActionGate and host gate approve.
- No repo public until secret scan, path scrub and claims scan are clean.
