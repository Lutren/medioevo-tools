# DUAT_VARIANTS_COMPARISON v0.6

## Current DUAT City

Status before v0.6: functional Canvas 2D simulation with agents, tasks, needs, buildings, resources, RPG export, Wabi design-only bridge, physics adapter, graphics budget and tests.

Strengths:
- Deterministic local app.
- Tests/build/typecheck already passing.
- Good operational layer: R, Phi_eff, gate, witnesslog, handoff and Wabi drafts.

Weaknesses:
- Visuals were mostly flat tiles and circles.
- City loop had limited Sims-style object interaction.
- RPG export lacked map layer, schedules and environmental hazards.

## Local Candidates

| candidate | value | risk | action |
|---|---|---|---|
| `ROOT_BRAIN_OS/DUAT ASSETS` | DUAT visual kit, icons, UI panels, style guide | provenance/license review | reference only |
| `ROOT_WORKSPACE/publish_staging/medioevo-site/.../buildings` | existing isometric building art | commercial/public boundary review | reference only |
| `ROOT_WORKSPACE/docs/design/MEDIOEVO_AGENT_CITY_UI_SYSTEM_2026-05-02.md` | visual tokens and agent-city shell | low code risk | extracted design rules |
| `ROOT_BRAIN_OS/.../medioevo-duat-geodia-unified/public/assets/.../maps` | GEODIA maps and district images | likely internal/editorial | reference only |
| zips under scanned roots | possible asset packs | archive review required | registered, not extracted |

## Decision

No external/local owner asset was copied into `artifacts/duat-city/public`. v0.6 improves visuals with procedural Canvas 2D renderers and keeps the asset path ready through manifests and atlas fallback support.
