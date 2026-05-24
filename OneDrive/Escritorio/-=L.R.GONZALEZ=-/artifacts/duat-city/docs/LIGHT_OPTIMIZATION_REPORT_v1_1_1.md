# LIGHT OPTIMIZATION REPORT v1.1.1

Fingerprint: DUAT-v1.1.1-FOCUSED-FPS-CLOSURE

## Implemented

- Added `src/light/lightBudget.ts` with per-preset caps, intensity threshold, reflection scale and update cadence.
- Added `src/pixelRealism/dirtyRegions.ts` for deterministic dirty-region signatures and tests.
- Added `src/pixelRealism/renderBudget.ts` for particle caps and reflection skipping.
- Pixel Realism runtime now reuses cached light grids when the dirty signature and cadence bucket are stable.
- Light budgets are applied before metrics so `activeLightCells` reflects capped work.

## Budgets

| Preset | Active light cap | Cadence | Bounce |
|---|---:|---:|---:|
| LOW | 1800 | 23 frames | 0 |
| MEDIUM | 7200 | 23 frames | 1 |
| HIGH | 20000 | 12 frames | 1 |
| BEAUTIFUL | 28000 | 12 frames | 2 |
| DEBUG | 9000 | 23 frames | 1 |

## Result

The optimization reduced active light cell counts from full-grid values
to preset caps. It did not make HIGH/BEAUTIFUL sustain 30 FPS in the
automated CDP run. The next real optimization should move expensive canvas
postprocess passes and light propagation to cached/offscreen surfaces with
explicit invalidation.

## Boundary

This remains a physically inspired light approximation for pixel-art realism,
not exact physics, path tracing or WebGPU.
