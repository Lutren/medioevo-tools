# Performance Benchmark v1.4

Fingerprint: DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL

Mode: Edge/CDP/headless-frame-sampler

| Scenario | external avg FPS | external p95 ms | app avg FPS | app p95 ms | dropped | focus | runtime |
|---|---:|---:|---:|---:|---:|---|---|
| high_iso3d_operational | 30.3 | 133.4 | 28.24 | 149.9 | 20 | unconfirmed | static-render-benchmark |
| beautiful_vermeer_city | 54.82 | 33.3 | 54.95 | 33.3 | 9 | unconfirmed | static-render-benchmark |
| debug_osit_formula_lab | 51.71 | 50 | 50.82 | 50 | 20 | unconfirmed | static-render-benchmark |

Notes:
- Focused/headed benchmark runner timed out earlier in this environment.
- This fallback uses requestAnimationFrame sampling in Edge/CDP headless plus the app internal FPS snapshot.
- Scenarios use benchmarkStatic=1 to isolate render cost from simulation ticks; normal playable mode remains live.
- Manual headed FPS remains the next verification step.
