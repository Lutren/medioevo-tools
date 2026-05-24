# OFFSCREEN_CACHE_PERFORMANCE_v1_2

## Implemented

v1.2 adds cache boundaries for static and postprocess layers:

- `src/pixelRealism/offscreenLayerCache.ts`
- `src/pixelRealism/postprocessCache.ts`
- `src/pixelRealism/layerCompositor.ts`

Dirty keys cover camera, material changes, light/weather/vibe changes, agent movement and UI mode.

## Benchmark

`docs/PERFORMANCE_BENCHMARK_v1_2.json` was captured with local Edge/CDP and `focusStatus=focused`. The measured average FPS was 11.44 across the inherited focused benchmark scenarios.

Performance still has HIGH/BEAUTIFUL pressure from canvas/postprocess/light-cell costs. v1.2 adds the cache framework and tests; it does not claim a full renderer rewrite.
