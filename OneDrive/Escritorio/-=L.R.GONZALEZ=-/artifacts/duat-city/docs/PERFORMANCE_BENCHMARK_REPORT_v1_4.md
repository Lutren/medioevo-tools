# Performance Benchmark v1.4

Fingerprint: DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL

Mode: Edge/CDP/headless-frame-sampler

| Scenario | external avg FPS | external p95 ms | app avg FPS | app p95 ms | dropped | focus | runtime |
|---|---:|---:|---:|---:|---:|---|---|
| high_iso3d_operational | 34.69 | 116.7 | 32.48 | 133.3 | 20 | unconfirmed | static-render-benchmark |
| beautiful_vermeer_city | 50.2 | 50 | 49.1 | 50.1 | 20 | unconfirmed | static-render-benchmark |
| debug_osit_formula_lab | 54.8 | 33.3 | 53.73 | 33.4 | 13 | unconfirmed | static-render-benchmark |

Notes:
- Focused/headed benchmark runner timed out earlier in this environment.
- This fallback uses requestAnimationFrame sampling in Edge/CDP headless plus the app internal FPS snapshot.
- Scenarios use benchmarkStatic=1 to isolate render cost from simulation ticks; normal playable mode remains live.
- Manual headed FPS remains the next verification step.
