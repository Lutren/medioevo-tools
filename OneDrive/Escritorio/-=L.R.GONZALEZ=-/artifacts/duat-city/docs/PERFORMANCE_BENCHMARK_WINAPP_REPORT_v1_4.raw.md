# Performance Benchmark v1.4

Fingerprint: DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL

Mode: Edge/CDP/headless-frame-sampler

| Scenario | external avg FPS | external p95 ms | app avg FPS | app p95 ms | dropped | focus | runtime |
|---|---:|---:|---:|---:|---:|---|---|
| high_iso3d_operational | 60 | 16.8 | 60.18 | 16.8 | 0 | unconfirmed | static-render-benchmark |
| beautiful_vermeer_city | 60 | 16.7 | 60.18 | 16.7 | 0 | unconfirmed | static-render-benchmark |
| debug_osit_formula_lab | 60 | 16.8 | 60.17 | 16.8 | 0 | unconfirmed | static-render-benchmark |

Notes:
- Focused/headed benchmark runner timed out earlier in this environment.
- This fallback uses requestAnimationFrame sampling in Edge/CDP headless plus the app internal FPS snapshot.
- A warmup route is loaded before measurement so startup/module load cost is not counted as scenario FPS.
- Scenarios use benchmarkStatic=1 to isolate render cost from simulation ticks; normal playable mode remains live.
- Manual headed FPS remains the next verification step.
