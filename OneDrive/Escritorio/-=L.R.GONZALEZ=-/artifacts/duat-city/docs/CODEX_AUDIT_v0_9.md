# CODEX AUDIT v0.9

Fingerprint: `DUAT-v0.9-QUATERNARY-TIMING-CORE`
Date: 2026-05-19

## Baseline

- Target: `artifacts/duat-city`
- Baseline tests: PASS.
- Baseline typecheck: PASS.
- Baseline build: PASS.
- Prior known v0.8: 33 test files / 150 tests PASS, HTTP smoke 200.

## Scope

v0.9 implements a local deterministic quaternary/tetranary timing core inspired by cascaded binary filters. It is operational software for DUAT City diagnostics, render/LOD modulation, OSIT visibility, RPG export enrichment and Wabi design-only workpack drafts.

## Boundaries

- No new assets copied.
- No push, deploy, cloud, commit or MCP execution.
- Wabi remains design-only: `execution_allowed=false`, `sandbox_execution_allowed=false`, `real_apply_allowed=false`.
- Claims remain formal-lab/operational. This does not claim quantum physics, new hardware or a validated physical theory.

## Integration Points

- Core: `src/quaternary/*`
- Simulation: `src/sim/quaternaryAdapter.ts`, `src/sim/engine.ts`
- UI: `src/components/QuaternaryPanel.tsx`, `src/components/OSITPanel.tsx`, `src/components/AgentInspector.tsx`
- Render: `src/graphics/graphicsMetrics.ts`, `src/render/canvasRenderer.ts`
- Pixel field: `src/physicsField/pixelTypes.ts`, `src/physicsField/cellularPhysics.ts`
- Handoff/RPG/Wabi: `src/core/handoff.ts`, `src/rpg/worldExport.ts`, `src/wabi/*`

