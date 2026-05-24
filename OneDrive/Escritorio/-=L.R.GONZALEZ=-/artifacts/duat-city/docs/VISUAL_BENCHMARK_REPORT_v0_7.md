# VISUAL BENCHMARK REPORT v0.7

Fingerprint: `DUAT-VISUAL-QA-ASSET-ALLOWLIST-v0.7`
Date: 2026-05-19

## Method

Benchmark runner: `src/bench/runVisualBenchmark.ts`

Output JSON: `docs/VISUAL_BENCHMARK_v0_7.json`

Mode: deterministic Node simulation estimate. This is not a browser CPU profiler; it measures simulation/render-cost estimates for repeatable local scenarios.

## Results

| Scenario | Avg FPS | Min FPS | Avg frame ms | P95 frame ms | Agents | R_graphics | Phi_graphics | R_physics | Phi_physics |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline-12-agents | 416.44 | 92.70 | 2.40 | 3.31 | 12 | 0.07 | 1.00 | 0.09 | 0.26 |
| 50-agents | 209.30 | 131.14 | 4.78 | 5.56 | 50 | 0.07 | 1.00 | 0.14 | 0.11 |
| 100-agents | 88.86 | 36.28 | 11.25 | 12.82 | 100 | 0.07 | 1.00 | 0.11 | 0.08 |
| lights-off | 213.48 | 140.88 | 4.68 | 5.52 | 50 | 0.07 | 1.00 | 0.14 | 0.11 |
| particles-off | 219.55 | 153.28 | 4.55 | 5.44 | 50 | 0.07 | 1.00 | 0.14 | 0.11 |
| pixel-field-off | 326.88 | 180.75 | 3.06 | 3.76 | 50 | 0.07 | 1.00 | 0.14 | 0.11 |
| overlays-on | 169.52 | 111.42 | 5.90 | 6.79 | 50 | 0.20 | 0.88 | 0.14 | 0.11 |

## Interpretation

- 100 agents remain viable in the estimate, but physics Phi is low because many pair checks do not become useful resolutions.
- Pixel field adds visible cost; disabling it improved the 50-agent estimate from 209 FPS to 327 FPS.
- Debug overlays are the clearest graphics cost driver and raise `R_graphics` to 0.20.
- Browser FPS/CPU still needs owner review with DevTools or a dedicated in-app FPS sampler.
