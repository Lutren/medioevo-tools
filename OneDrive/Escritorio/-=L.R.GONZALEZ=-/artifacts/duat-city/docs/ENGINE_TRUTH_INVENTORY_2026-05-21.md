# ENGINE TRUTH INVENTORY 2026-05-21

Execution date: 2026-05-22

Scope: Fase 0 only. No feature code was changed. This inventory verifies the live `artifacts/duat-city` tree against the requested MEDIOEVO engine / DUAT simulator features.

Update 2026-05-22: after user confirmation, Fase 1/Fase 2/Fase 3 work was implemented in-place. The original table below is preserved as the checkpoint truth before feature code. Current deltas:

- Canon declared in `docs/ENGINE_CANON.md`; stale runtime copy marked with `LEER_STALE.md`.
- EML corrected to canonical bounded sigmoidal form in `src/core/eml.ts`.
- `Agent.lineage`, `Agent.originStory`, `Agent.skills`, deterministic lineage generator, theater profile creation, academy skill packs, city context, and psychologist repair cycle now exist with tests.
- Physics determinism test now exists in `src/tests/physicsDeterminism.test.ts`.
- Godot RPG private validations ran headless: 24 `Validate*.tscn` scenes passed in `E:\Medioevo_RPG`.

## Gate

| Check | Result | Evidence |
|---|---:|---|
| Dependencies | OK, no install run | `node_modules/` already existed in `artifacts/duat-city` |
| Tests | PASS | `npm test` -> 106 test files / 314 tests passed |
| Typecheck | PASS | `npm run typecheck` -> `tsc -p tsconfig.json --noEmit` |
| Build | PASS | `npm run build` -> Vite 5.4.21, 249 modules transformed, built in 19.90s |
| Current Go/No-Go | GO for Fase 1 consolidation; HOLD for feature code until user confirms gaps | Test/typecheck/build are green |

## Executive Truth

`duat-city` is the live MEDIOEVO/DUAT engine in this workspace. It already contains a mature TypeScript/Web simulation, renderer, agent city, physics, field physics, game modes, brain/runtime surfaces, procedural art, and RPG export path. The actual gap is not "build the whole engine"; the actual gap is to canonize this tree and implement four missing gameplay/simulation features.

Do not create `duat-city-v2`. Do not move this package. Do not import stale ZIP/runtime sources.

## Requested Feature Inventory

| Requested feature | Real status | Files checked | Current truth / gap |
|---|---|---|---|
| Canonical MEDIOEVO/DUAT engine | EXISTE | `package.json`, `docs/CODEX_FINAL_HANDOFF_v1_5.md`, `docs/TEST_REPORT_v1_5.md`, `src/` | Package is `@workspace/duat-city`, private workspace package. v1.5 handoff reports local review PASS. Current run confirms tests/typecheck/build PASS. |
| Physics per particle / per body | EXISTE | `src/physics/types.ts`, `src/physics/physicsEngine.ts`, `src/physics/integrator.ts`, `src/physics/collisions.ts`, `src/physics/spatialHash.ts`, `src/physics/agentPhysicsAdapter.ts` | Each `PhysicsBody` owns position, previous position, velocity, radius, mass, damping, needs, R, Phi_eff and gate. Engine integrates per body, resolves bounds/tile/circle collisions, uses spatial hash, and guards NaN. |
| Physics tests | EXISTE | `src/tests/physics.test.ts`, `src/tests/agentPhysicsAdapter.test.ts`, `src/tests/integrationV05.test.ts` | Current `npm test` passes all included physics tests. A dedicated same-seed physics hash determinism test is still Fase 3 work. |
| Field / pixel physics | EXISTE | `src/physicsField/fluidLite.ts`, `src/physicsField/fireSmoke.ts`, `src/physicsField/lightMatter.ts`, `src/physicsField/cellularPhysics.ts`, `src/physicsField/materials.ts` | Water, smoke, dust, fire, light decay, materials, cell metrics, finite guards and qPacked cell states exist. |
| Renderer / graphics engine | EXISTE | `src/render/`, `src/graphics/`, `src/iso3d/`, `docs/GRAPHICS_ENGINE.md`, `docs/ISOMETRIC_RENDER_ENGINE.md`, `docs/PERFORMANCE_BENCHMARK_REPORT_v1_5.md` | Canvas/isometric/pixel-realism rendering exists with benchmark evidence in v1.5 docs. Current build passes. |
| City with functional buildings | PARCIAL | `src/core/types.ts`, `src/sim/buildings.ts`, `src/sim/city.ts`, `src/sim/objects.ts`, `src/components/Toolbar.tsx` | `TileType` has 18 tile kinds. `BUILDING_DEFS` has 12 functional building definitions: plaza, residential, workshop, archive, observatory, market, clinic, academy, temple, garden, ruin, gatehouse. Initial city spawns 6 buildings. Toolbar exposes a subset plus terrain. Claim "14 functional buildings" is not current truth from code. |
| Agents / citizens | EXISTE | `src/core/types.ts`, `src/sim/agents.ts`, `src/sim/scheduler.ts`, `src/sim/engine.ts`, `src/sim/relationships.ts` | 12 roles exist: Observer, Engineer, Archivist, Medic, Builder, Trader, Teacher, Scout, Gatekeeper, Storykeeper, Artisan, Courier. Agents have needs, mood, trust, R/Phi/gate, memory, relationships and inventory. |
| Agent background / 2-generation lineage | FALTA | `src/core/types.ts`, `src/sim/agents.ts`, `src/generative/` | `Agent` has no `lineage`, no `originStory`, and no deterministic lineage generator. This is one of the four real gaps. |
| Era selection | EXISTE | `src/gameModes/eraProgressionMode.ts`, `src/gameModes/gameModeTypes.ts`, `src/tests/eraProgressionMode.test.ts` | 10 eras exist, including gated `duat_epoch`. Boundary is explicitly fictional, not historical/scientific claim. |
| Context / mode selection | EXISTE | `src/gameModes/gameModeRouter.ts`, `src/gameModes/gameModeTypes.ts` | 8 game modes are current code truth: DUAT Interface, Hormiguero, Agent Sims, City President, Era Progression, VS Arena, RPG, Metroidvania. Claim "10 game modes" is not current truth from router/types. |
| Climate / geography selection | FALTA | `src/core/types.ts`, `src/sim/city.ts`, `src/gameModes/gameModeTypes.ts` | No `climate`, `weather`, `geography`, `biome`, or map-context field is present in `CityState` or game mode state. Terrain tile types exist, but not a selectable climate/geography model. |
| Procedural generators | EXISTE | `src/generative/pixelArtGenerator.ts`, `src/generative/proceduralAgentGenerator.ts`, `src/generative/proceduralBuildingGenerator.ts`, `src/generative/proceduralPropGenerator.ts`, `src/generative/proceduralTileGenerator.ts`, `src/generative/generativeSceneComposer.ts` | Procedural bitmap generators exist for agents, buildings, props, tiles and UI. |
| Theater for profile creation | FALTA | `src/core/types.ts`, `src/generative/proceduralAgentGenerator.ts`, `src/sim/buildings.ts`, `src/gameModes/` | There is no `theater` tile/building/mode and the current procedural agent generator returns only a bitmap, not a complete agent profile with role, needs, lineage and sprite. This is one of the four real gaps. |
| Academy | PARCIAL | `src/sim/buildings.ts`, `src/sim/agents.ts`, `src/sim/objects.ts`, `src/core/types.ts` | `academy` exists as a building and restores purpose/curiosity. It produces knowledge/culture. It does not install skill packs and `Agent` has no skills field. |
| Skill packs / installed skills | FALTA | `src/core/types.ts`, `src/core/persistence.ts`, `src/brain/`, `src/sim/agents.ts` | No `skills` or `installedSkills` field exists on `Agent`. Persistence serializes the full state generically, but no skill schema or academy installation logic exists. This is one of the four real gaps. |
| Psychologist role | FALTA | `src/sim/agents.ts`, `src/brain/`, `src/sim/events.ts`, `src/core/witnesslog.ts` | `AGENT_ROLES` does not include `Psychologist`. No repair role or therapist routine exists. |
| Repair agents that desvarian | PARCIAL | `src/core/metrics.ts`, `src/sim/tasks.ts`, `src/brain/residueDreamCycle.ts`, `src/brain/truthGate.ts`, `src/core/witnesslog.ts` | The substrate exists: R/Phi/gate, failed/blocked tasks, witnesslog, truth gate and a design-only residue dream cycle. Missing: explicit "desvariando" criteria and repair cycle. This is one of the four real gaps. |
| Modular brain | EXISTE | `src/brain/affectEngine.ts`, `src/brain/truthGate.ts`, `src/brain/prefrontalActionGate.ts`, `src/brain/residueDreamCycle.ts`, `src/brain/socialCortex.ts`, `src/brain/brainRuntime.ts` | Brain runtime surfaces exist and are local/design-gated. `residueDreamCycle` is explicitly `enabled: false`, `designOnly: true`. |
| Witnesslog / handoff | EXISTE | `src/core/witnesslog.ts`, `src/core/handoff.ts`, `src/sim/engine.ts` | Periodic and quaternary witness entries exist. Handoff generation exists. |
| RPG / Godot export bridge | EXISTE | `src/rpg/worldExport.ts`, `src/rpg/rpgTypes.ts`, `src/tests/rpgWorldV2.test.ts`, `src/tests/rpgExport.test.ts`, `docs/MEDIOEVO_RPG_ENGINE_EXPORT_v2.md` | DUAT-to-RPG export exists and current tests pass. Full Godot consumption verification is Fase 3 and was not run in this checkpoint. |
| EML active math form | PARCIAL / NEEDS FASE 1 FIX | `src/core/eml.ts`, `src/tests/eml.test.ts`, `docs/THEORY.md` | `docs/THEORY.md` states active EML is sigmoidal. Current `src/core/eml.ts` still implements clamped `exp(x) - log(y)` and tests assert that behavior. This is not a feature-code gap, but it must be corrected/documented in Fase 1 before canon declaration. |
| Runtime import gate for stale sources | EXISTE AS POLICY / NEEDS DOC MARKER | `docs/GAME_OS_ARCHITECTURE_v1_3.md`, `src/tests/duatOSITFullInventory.test.ts`, stale path verified externally | Existing tests and docs keep raw adoption blocked. The stale BRAIN_OS copy exists, but `LEER_STALE.md` has not been added yet because that is Fase 1, not Fase 0. |
| Publication gate | EXISTE | `docs/CODEX_FINAL_HANDOFF_v1_5.md`, `docs/GAME_OS_ARCHITECTURE_v1_3.md`, `src/tests/duatOSITFullInventory.test.ts` | v1.5 docs and inventory tests state no push/deploy/cloud/publication and raw adoption blocked. |

## Four Real Feature Gaps To Confirm

1. Add `Agent.lineage` and `Agent.originStory`, plus deterministic `generative/agentLineageGenerator.ts`.
2. Add theater profile creation: full profile output from role + needs + lineage + sprite, likely backed by a `theater` tile/building or game-mode surface.
3. Add academy skill packs: `Agent.skills` or `Agent.installedSkills`, pack definitions, academy installation logic, and persistence tests.
4. Add psychologist/repair loop: role `Psychologist`, explicit "desvariando" criteria, repair routine using existing R/gate/tasks/residue/truth substrate, and witnesslog evidence.

Additional non-feature consolidation gap: fix/canonize EML because current `src/core/eml.ts` still uses legacy `exp/log` while `docs/THEORY.md` declares active sigmoidal EML.

## Commands Run

```powershell
python tools\release\pending_review.py --write --quiet
npm test
npm run typecheck
npm run build
```

## Current Evidence Snapshot

- `pending_review date=2026-05-22 active_dedup=0 claudio_open=0`
- `npm test`: 106 passed test files, 314 passed tests.
- `npm run typecheck`: PASS.
- `npm run build`: PASS, 249 modules transformed, output under `dist/public/`.

## Checkpoint Decision

Fase 0 passes. Recommended next step is Fase 1 consolidation, not feature expansion:

1. Add `docs/ENGINE_CANON.md`.
2. Mark stale BRAIN_OS copy with `LEER_STALE.md`.
3. Update workbench truth docs.
4. Fix/canonize EML to the sigmoidal active form with test update.

Feature code should remain on hold until the four real gaps above are confirmed.
