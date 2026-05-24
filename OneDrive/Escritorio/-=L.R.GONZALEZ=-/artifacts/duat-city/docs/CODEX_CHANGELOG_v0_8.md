# CODEX CHANGELOG v0.8

Fingerprint: `DUAT-v0.8-FPS-CAMERA-FRAMING-VISUAL-POLISH`
Date: 2026-05-19

## Added

- In-app FPS sampler and performance snapshot types.
- Performance panel in OSIT with reset, copy JSON and 30s benchmark controls.
- Camera preset helpers for City, Agent, RPG, OSIT, Beautiful and Debug.
- Toolbar controls: Reset Camera, Follow Critical, Hide UI.
- v0.8 screenshot review, visual QA, camera and performance docs.
- v0.8 tests for FPS sampler, camera presets, performance schema and mode regression.

## Changed

- `MainCanvas` now uses layout effects for resize/render to reduce first-paint empty canvas captures.
- `renderCity` returns render counters for the sampler.
- Beautiful mode hides technical chrome and suppresses debug overlays.
- Debug mode owns pixel/FibMob/chunk/physics overlays.
- Building and agent renderers received small legibility/shadow polish.

## Preserved

- No new assets were copied.
- v0.7 reviewed assets remain `INTERNAL_REVIEWED_ASSET` and `publication_allowed=false`.
- Wabi remains design-only: no execution, no real apply, no sandbox execution.
- No push, deploy, commit, cloud, backend or MCP execution.

## Tests

- Added test files:
  - `src/tests/fpsSampler.test.ts`
  - `src/tests/camera.test.ts`
  - `src/tests/performancePanel.test.ts`
  - `src/tests/beautifulMode.test.ts`
  - `src/tests/visualPolishRegression.test.ts`

## Risks

- Edge headless virtual-time FPS is useful as UI evidence, not as a CPU profiler.
- Final visual quality still depends on owner-approved building/tile/agent assets.
