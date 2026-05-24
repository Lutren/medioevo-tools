# PERFORMANCE SAMPLER v0.8

Fingerprint: `DUAT-v0.8-FPS-CAMERA-FRAMING-VISUAL-POLISH`
Date: 2026-05-19

## Scope

v0.8 adds an in-app `requestAnimationFrame` sampler. It measures browser frame pacing from inside DUAT instead of relying only on the deterministic Node estimate from v0.7.

## Files

- `src/performance/performanceTypes.ts`
- `src/performance/fpsSampler.ts`
- `src/performance/useFpsSampler.ts`
- `src/performance/performanceOverlay.ts`
- `src/components/PerformancePanel.tsx`

## Metrics

The sampler records:

- `currentFps`, `avgFps`, `minFps`, `maxFps`
- `frameMs`, `avgFrameMs`, `p50FrameMs`, `p95FrameMs`, `p99FrameMs`
- `droppedFrames`, `longFramesOver16ms`, `longFramesOver33ms`
- `sampleWindowSeconds`, `totalFrames`, `lastResetAt`
- render counters: agents, buildings, tiles, particles, active pixel cells, dirty chunks, overlays, view mode, camera zoom

## Runtime Contract

- The sampler uses refs internally and throttles React state updates to roughly 250 ms.
- It does not call `setState` every frame.
- `PerformancePanel` exposes Reset, Copy JSON and Run 30s Benchmark.
- The benchmark export uses schema `duat/performance-benchmark/v0.8`.

## Status Bands

- `avgFps >= 55`: `PERF_OPTIMO`
- `avgFps >= 30`: `PERF_FUNCIONAL`
- `avgFps >= 20`: `PERF_CARGADO`
- otherwise: `PERF_SATURADO`

## Evidence

- Screenshot: `docs/screenshots/v0_8/v0_8_osit_performance.png`
- Headless sampler artifact: `docs/PERFORMANCE_BENCHMARK_v0_8.json`
- Tests: `src/tests/fpsSampler.test.ts`, `src/tests/performancePanel.test.ts`

## Limits

The Edge headless screenshot run used virtual time to let the app settle before capture. That is useful for UI evidence but should not be treated as a CPU profiler. For CPU precision, run a headed browser benchmark or DevTools performance capture.
