# TECH_REUSE_MAP v0.6

| source signal | extracted reusable idea | implemented in |
|---|---|---|
| DUAT style guide | dark operational surface, cyan/teal signal, amber caution, subtle glow | `src/graphics/lightEngine.ts`, `src/render/canvasRenderer.ts` |
| Agent City UI system | city as agents/buildings, not dashboard-only | `src/sim/objects.ts`, `src/sim/agentLife.ts` |
| DUAT asset manifests | atlas must tolerate missing assets and fallback procedural | `src/graphics/atlas.ts`, `src/graphics/spriteLoader.ts` |
| SimCity/Sims target | zoning/districts, needs, homes/workplaces, object interactions | `src/core/types.ts`, `src/sim/city.ts`, `src/sim/agentLife.ts` |
| Pixel physics prompt | low-resolution active-cell field, not per-screen-pixel object physics | `src/physicsField/*` |
| Wabi design-only policy | workpacks remain drafts with rollback and execution disabled | `src/wabi/workpackDraft.ts`, `src/components/WabiPanel.tsx` |
| RPG builder target | world v2 needs map tiles, schedules, hazards and asset refs | `src/rpg/worldExport.ts`, `src/rpg/rpgTypes.ts` |

No dependency was added.
