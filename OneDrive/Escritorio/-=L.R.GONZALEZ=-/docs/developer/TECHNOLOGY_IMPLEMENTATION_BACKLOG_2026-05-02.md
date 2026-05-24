# Technology Implementation Backlog

Status: actionable backlog derived from curador review.

## P0

| module | implement | acceptance |
|---|---|---|
| Redacted token note | Classify `Downloads\r.txt` as `USER_ASSERTED_SAFE_NON_BLOCKING`; exclude from staging | no staging path contains `r.txt`; risk register and checklist no longer treat it as release blocker |
| Curador session | Preserve official output session under curador agent | required artifacts exist |
| Source intake | Register full `Downloads` set, including `He revisado...`, `#!usrbinenv python3.txt`, `Me has pedido...`, DUAT, NEUROSTATE and `r.txt` | generated register has hashes, classification, lane, action and target; no `CLASSIFY_BEFORE_USE` residue |
| Memory vault | Create clean MemPalace index in Claudio `memory_vault` | `README`, master index, fichas, paper queue, commercial split and external verification exist |
| External repo verification | Verify GitHub projects before dependency adoption | evidence JSON and `external_projects_verification.md` list license/status/current pushed date |
| GitHub staging policy | Public repos must be staged from allowlists only | staging script/dry-run reports no external action |
| Claims boundary | Add public GitHub allowed/prohibited claims | `CLAIMS_BOUNDARY.md` covers whitepapers and repos |
| Open core + UI paga | Lock product split and agent-wrapper model | product fichas, UI system, dependency gate, claim register and publishing runbook exist |
| OBS Safe Integration Kit | Promote curated kernel into `packages\open-dev` with release boundary docs | package contains source, tests, examples, `LICENSE`, `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md`, `SECURITY.md`; pytest/compile/CLI smoke/secret scan/path scrub pass |
| Curador Always-On | Make curator preflight mandatory for dirty repos, unknown sources and residue | `AGENTS.md`, Claudio `CLAUDE.md`, `docs/developer/CURADOR_ALWAYS_ON_PROTOCOL_2026-05-03.md`, `claudio/docs/CURADOR_ALWAYS_ON_CLAUDIO_2026-05-03.md` and `tools/release/curador_preflight.py` exist |
| Claudio Public Agent Runtime P0 | Convert Mercury-like patterns into a public-safe Claudio CLI surface without copying Mercury | `docs/developer/CLAUDIO_PUBLIC_AGENT_RUNTIME_BLUEPRINT_2026-05-15.md` and workpack exist; first implementation is stdlib-only, dry-run/read-only, no external channels, no secrets printed |
| DUAT Operator Shell v0.1 | Wrap the Claudio P0 kernel as a human/product operator shell with OSIT gates | `docs/developer/DUAT_OPERATOR_SHELL_V0_1_SPEC_2026-05-15.md` exists; P0 maps to `packages/open-dev/claudio-agent-runtime`; P1 waits for WitnessLog/GhostGate/ActionGate execute |

## P1

| module | implement | acceptance |
|---|---|---|
| Agent City UI shell | Convert commercial apps to city-of-agents shell | topbar, sidebar, agent panel, evidence ledger and ActionGate state visible per app |
| FlujoCRM agent wrapper | Reframe CRM as `Agente Mercado` | UI keeps CRM workflows, adds agent role, evidence notes and local/privacy copy |
| Asistente agent wrapper | Reframe Asistente as `Agente Mostrador` | drafting/approval flow explicit; no automatic send claim |
| Mini Office agent wrapper | Reframe Mini Office as `Oficina de agentes` | agents mapped to tasks, premium templates separated |
| Argus agent wrapper | Reframe Argus as `Agente Consola` | runtime state, private boundary and ActionGate visible |
| `data-curation-observatory` | Generic curador templates, manifest schema, demo folder, example report | tests or smoke produce manifest without touching inputs |
| `residueos-core` | ActionGate CLI, ledger, approve/review/block, sample payloads | pytest/smoke pass; thresholds marked DEMO_ONLY |
| `ai-web-gateway-observacionista` | `ObservationEnvelope`, router policy, retry policy, cache key spec, MCP tool schema | no browser action by default; docs and unit tests |
| Whitepapers | Low-claim docs for five repos | no prohibited claims; no local paths |
| Patrimony checklist | Redacted private action checklist for family continuity | no secrets, only actions and fields |

## P2

| module | implement | acceptance |
|---|---|---|
| `obs-info-kernel-lite` | claim registry, evidence store, anti-information/dark-information labels | synthetic corpus; no research overclaims |
| `observational-calibration-toolkit` | R/Phi/Jc schemas, falsifier templates, null model examples | unit tests; terms defined operationally |
| `la-biblioteca-de-alejandria` | public index and map of sanitized repos | links only to public-safe repos |
| `duat-lab` | Minimal synthetic DUAT event store, artifact graph and calibration simulator | no RPG/canon assets; claims say computational lab only |
| `neurostate-ui` | Split NEUROSTATE UI/runtime from mixed TXT into a local prototype | no medical/cognitive diagnostic claims; no local model action without gate |
| Commercial pack | Data Curation Pack and Research OS Templates packaging | Gumroad/listing copy reviewed, no source leak |

## Never In Public Repo

- `E:\Medioevo_RPG\assets`, `scripts`, `scenes`, `runtime`, builds or private docs.
- Full MEDIOEVO books or canon vaults.
- `E:\MEDIOEVO\seguridad`, `sesiones`, `tor`, backups.
- Raw Downloads texts containing private context.
- Secrets, tokens, credentials, session state, browser profiles.
- Vendors, pentest repos, caches and build outputs.
