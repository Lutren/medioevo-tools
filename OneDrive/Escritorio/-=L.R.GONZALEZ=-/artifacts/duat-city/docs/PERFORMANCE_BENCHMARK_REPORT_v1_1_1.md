# PERFORMANCE BENCHMARK v1.1.1

Fingerprint: DUAT-v1.1.1-FOCUSED-FPS-CLOSURE

Local focused/headed benchmark attempted with Microsoft Edge and CDP. No MCP execution, cloud, external API, push, deploy or commit.

- URL: http://127.0.0.1:18519/duat-city/?benchmark=v1_1_1&durationMs=10000&browserMode=CDP
- Duration per scenario: 10000 ms
- Browser mode: CDP
- Focus status: focused
- Focused browser available: true
- Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0

| Scenario | Quality | View | avg FPS | p95 ms | p99 ms | min FPS | max FPS | dropped | active light cells | active material cells | particles | agents | browser mode | focus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| LOW 80x45 baseline | LOW | OPERATIONAL | 0.01 | 77120.1 | 77120.1 | 0.01 | 0.01 | 1 | 1800 | 0 | 12 | 12 | CDP | focused |
| MEDIUM 160x90 | MEDIUM | OPERATIONAL | 0.1 | 10000 | 10000 | 0.1 | 0.1 | 1 | 7200 | 0 | 12 | 12 | CDP | focused |
| HIGH 320x180 | HIGH | OPERATIONAL | 5.59 | 433 | 433 | 2.31 | 60.24 | 3 | 20000 | 0 | 12 | 12 | CDP | focused |
| BEAUTIFUL sunny/castle/lake | BEAUTIFUL | BEAUTIFUL | 1.16 | 16703 | 16703 | 0.06 | 60.24 | 4 | 28000 | 2 | 12 | 12 | CDP | focused |
| BEAUTIFUL neon rain street | BEAUTIFUL | BEAUTIFUL | 0.13 | 14971 | 14971 | 0.07 | 8.58 | 2 | 28001 | 4 | 66 | 12 | CDP | unconfirmed |
| warm interior tavern | HIGH | OPERATIONAL | 10.49 | 266.4 | 299.8 | 3.34 | 60.61 | 44 | 20002 | 1 | 18 | 12 | CDP | unconfirmed |
| archeopunk city night | HIGH | OPERATIONAL | 12.29 | 216.6 | 299.6 | 3.16 | 60.61 | 47 | 20001 | 1 | 60 | 12 | CDP | unconfirmed |
| DEBUG light grid | DEBUG | DEBUG | 36.97 | 100 | 133.3 | 5.46 | 60.61 | 44 | 9000 | 0 | 12 | 12 | CDP | unconfirmed |
| material placement water/fire/smoke/stone/neon | HIGH | OPERATIONAL | 10.56 | 249.8 | 283.1 | 3.34 | 60.24 | 41 | 20002 | 4 | 24 | 12 | CDP | unconfirmed |
| 100 agents + light engine active | HIGH | OPERATIONAL | 9.76 | 249.8 | 299.7 | 3.34 | 60.24 | 41 | 20001 | 4 | 66 | 100 | CDP | unconfirmed |

## Notes

- Focused benchmark runner is local-only. Browser focus is verified with document.hasFocus and visibilityState.
- Focused browser was observed by the app.
- Light budget and dirty-signature cache are enabled for v1.1.1.
- Local focus attempt: focused_by_pid
- Focused browser verified by document.hasFocus().

## Interpretation

- The focused run closed the v1.1 gap: the app observed focus in the browser and the runner is reproducible from the local command line.
- Active light cell budgets are now enforced: LOW 1800, MEDIUM 7200, HIGH 20000, BEAUTIFUL 28000 and DEBUG 9000.
- HIGH/BEAUTIFUL still fail the 30 FPS target in the CDP run. The optimization lowered light-cell pressure, but render cadence remains uneven under Edge/CDP automation.
- The in-app `Run Focused FPS` control is available in OSIT Performance with 10s/30s/60s durations for owner-controlled manual focus.
- This benchmark measures a physically inspired light approximation for pixel-art realism. It is not a claim of exact physical simulation.
