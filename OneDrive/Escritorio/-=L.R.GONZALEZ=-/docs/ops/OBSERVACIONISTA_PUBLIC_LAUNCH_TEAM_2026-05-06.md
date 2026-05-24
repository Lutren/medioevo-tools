# Observacionista Public Launch Team - 2026-05-06

Status: `ACTIVE_LOCAL_AGENT_SPECS / EXTERNAL_ACTIONS_BLOCKED`

This is the professional public-facing observacionista team. It does not create
daemons, does not post, does not send messages and does not edit dashboards.

Canonical bus: `COMMS/`

Coordinator:

- `publicacion-perfiles-observatorio`

Registered specialist agents:

- `social-media-observatorio`
- `prensa-observatorio`
- `publicidad-growth-observatorio`
- `editorial-research-release`
- `claims-falsifier-observatorio`
- `community-sponsors-observatorio`

## Operating Model

| agent | department | problem owned | output |
|---|---|---|---|
| `social-media-observatorio` | plaza-mercado/social | platform-specific posts without leaking private IP | captions, threads, carousels, calendar drafts |
| `prensa-observatorio` | plaza-mercado/prensa | press narrative, media kits and outreach preparation | press notes, pitch drafts, media brief, no sending |
| `publicidad-growth-observatorio` | plaza-mercado/growth | visitor growth and campaign hypotheses without ad spend | campaign hypotheses, landing angles, metric plans |
| `editorial-research-release` | biblioteca/research | staged release of theory papers and research | release ladder, paper slices, sponsor brief plan |
| `claims-falsifier-observatorio` | curaduria/claims | prevent strong unsupported public claims | claim audit, falsifiers, downgrade recommendations |
| `community-sponsors-observatorio` | plaza-mercado/sponsors | sponsor continuity and community updates | monthly update drafts, tier copy, retention notes |

## Shared Reads

- `AGENTS.md`
- `PRODUCT_MAP.md`
- `VISIBILITY_MATRIX.md`
- `RISK_REGISTER.md`
- `docs/control/CLAIMS_BOUNDARY.md`
- `docs/publishing/*.md`
- `docs/observacionismo/*.md`
- `COMMS/README.md`
- `COMMS/agents_state/*.json`
- `docs/developer/LEY_KERNEL_ORDEN_CRITERIO_DISCIPLINA_2026-05-06.md`

## Shared Blocks

Always blocked without target-specific ActionGate and post-action evidence:

- social posting;
- DMs, emails, pitches or press outreach;
- Gumroad dashboard saves/uploads/pricing;
- GitHub push/profile/Sponsors dashboard changes;
- LinkedIn edits/posts;
- website deploys;
- paid ads or payment changes;
- raw research dump release;
- account/session/login material exposure;
- RPG/TCG, private books, private canon or full runtime exposure.

## Output Contract

Every agent output must include:

1. current truth;
2. audience;
3. problem solved;
4. public-safe message;
5. private exclusion;
6. next gated action;
7. evidence files;
8. falsifiers.

## Agent Registry

The agent state files live in:

- `COMMS/agents_state/social-media-observatorio.json`
- `COMMS/agents_state/prensa-observatorio.json`
- `COMMS/agents_state/publicidad-growth-observatorio.json`
- `COMMS/agents_state/editorial-research-release.json`
- `COMMS/agents_state/claims-falsifier-observatorio.json`
- `COMMS/agents_state/community-sponsors-observatorio.json`

## Handoff

Current handoff:

`COMMS/handoffs/2026-05-06-observacionista-public-launch-team.md`

## Reason For The Team

The public layer now needs specialization:

- social media adapts message;
- press frames the story;
- growth tests visitor paths;
- editorial controls staged theory release;
- claims/falsifier protects epistemic integrity;
- community/sponsors maintains recurring support.

The team is professional because every role has ownership, gates, evidence and
private boundaries.
