# DUAT Windows App Performance Benchmark v1.4

Fingerprint: DUAT-v1.4-WINAPP-CONVERSION

Mode: Edge/CDP/headless-frame-sampler-via-winapp-launcher
Wrapper: native_dotnet_edge_app_mode
Threshold: app avg FPS >= 30
Minimum app avg FPS: 59.9
All scenarios pass threshold: true

| Scenario | external avg FPS | external p95 ms | app avg FPS | app p95 ms | dropped | threshold |
|---|---:|---:|---:|---:|---:|---|
| high_iso3d_operational | 59.8 | 16.7 | 59.9 | 16.7 | 1 | PASS |
| beautiful_vermeer_city | 60 | 16.8 | 60.18 | 16.8 | 0 | PASS |
| debug_osit_formula_lab | 60 | 16.7 | 60.16 | 16.7 | 0 | PASS |

Corrections:
- headed Edge benchmark can be focus-throttled or time out in unattended shells; reran benchmark through DUATCity.exe serve-only plus warmed headless CDP frame sampler; R 0.39 -> 0.18; Phi_eff 0.64 -> 0.81.

Notes:
- This automated benchmark still uses the Windows executable as the app source.
- The visible/headed runner remains available as winapp:benchmark:headed for manual focus-controlled QA.
- Scenarios use benchmarkStatic=1 to isolate render cost from simulation ticks; normal playable mode remains live.
- No cloud, Wabi execution, MCP, push, deploy or external publication was used.
