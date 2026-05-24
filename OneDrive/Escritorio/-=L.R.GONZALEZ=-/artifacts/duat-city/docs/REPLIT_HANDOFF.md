# DUAT Agent City — Replit Handoff

## Status: COMPLETE v1.0

## Architecture

```
artifacts/duat-city/
  src/
    core/          — Pure math: types, fibmob, eml, metrics, handoff, witnesslog, persistence, math
    sim/           — City simulation: city, buildings, resources, agents, needs, tasks, events, relationships, scheduler, engine
    render/        — Canvas: palette, camera, lod-controller, input, canvasRenderer
    rpg/           — World export: rpgTypes, loreTags, factionGenerator, questGenerator, encounterGenerator, worldExport
    components/    — React: Topbar, ModeTabs, Toolbar, MainCanvas, CityPanel, AgentInspector,
                     BuildingInspector, ResourcePanel, TaskPanel, EventLogPanel,
                     RPGBuilderPanel, OSITPanel, HandoffPanel
    tests/         — 8 test suites, 85 tests
    App.tsx        — Main app with RAF simulation loop
    styles.css     — Plain CSS (game layer), Tailwind (layout)
  docs/
    THEORY.md      — FibMob math reference
    GAME_DESIGN.md — Game design document
    REPLIT_HANDOFF.md — this file
    CODEX_NEXT_STEPS.md — next actions
```

## Tests
```bash
pnpm --filter @workspace/duat-city run test
# → 8 test files, 85 tests, all passing
```

## Run
```bash
# Workflow auto-starts on port 18519 at /duat-city/
pnpm --filter @workspace/duat-city run dev
```

## Key Design Decisions
- **No backend**: All state in React (useState + useRef), RAF loop drives simulation
- **Plain CSS** for game-specific styling; Tailwind scaffold retained for components
- **Simulation at 200ms/tick** (5 ticks/sec at 1x speed, 20 at 4x)
- **Canvas 2D** for city rendering; no WebGL needed for 48×32 grid
- **FibMob identical to FibMob Lab**: same muK/fibK/fibKMult formulas, same VITEST guard
- **Auto-save to localStorage** every 15s; manual save/load available
- **RPG export** triggered from RPG mode panel; generates full MEDIOEVO world JSON

## Open Loops
1. Pathfinding: agents currently use linear interpolation toward building center
   (simple, fast). A* or flow field could improve realism.
2. Building upgrades (level > 1) not yet implemented — scaffold exists in types
3. Zone system (zoneId on tiles) scaffolded but not exposed in UI
4. Multiplayer/shared state not in scope (no backend)
5. DUAT FibMob Lab ↔ City cross-link: handoff JSON format compatible, but
   city doesn't consume lab's residue benchmark output directly
