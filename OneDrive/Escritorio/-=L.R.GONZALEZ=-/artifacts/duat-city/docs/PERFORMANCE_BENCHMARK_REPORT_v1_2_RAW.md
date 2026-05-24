# PERFORMANCE BENCHMARK v1.1.1

Fingerprint: DUAT-v1.1.1-FOCUSED-FPS-CLOSURE

Local focused/headed benchmark attempted with Microsoft Edge and CDP. No MCP execution, cloud, external API, push, deploy or commit.

- URL: http://127.0.0.1:18519/duat-city/?benchmark=v1_1_1&durationMs=1000&browserMode=CDP
- Duration per scenario: 1000 ms
- Browser mode: CDP
- Focus status: focused
- Focused browser available: true
- Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0

| Scenario | Quality | View | avg FPS | p95 ms | p99 ms | min FPS | max FPS | dropped | active light cells | active material cells | particles | agents | browser mode | focus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| LOW 80x45 baseline | LOW | OPERATIONAL | 0.1 | 19200.9 | 19200.9 | 0.05 | 2.14 | 2 | 1800 | 0 | 12 | 12 | CDP | focused |
| MEDIUM 160x90 | MEDIUM | OPERATIONAL | 1 | 1000 | 1000 | 1 | 1 | 1 | 7200 | 0 | 12 | 12 | CDP | focused |
| HIGH 320x180 | HIGH | OPERATIONAL | 1 | 1000 | 1000 | 1 | 1 | 1 | 20000 | 0 | 12 | 12 | CDP | focused |
| BEAUTIFUL sunny/castle/lake | BEAUTIFUL | BEAUTIFUL | 11.06 | 316.4 | 316.4 | 3.16 | 60.24 | 3 | 28000 | 2 | 12 | 12 | CDP | focused |
| BEAUTIFUL neon rain street | BEAUTIFUL | BEAUTIFUL | 51.64 | 33.8 | 83.3 | 12 | 61.35 | 3 | 28001 | 4 | 66 | 12 | CDP | focused |
| warm interior tavern | HIGH | OPERATIONAL | 1 | 1000 | 1000 | 1 | 1 | 1 | 20002 | 1 | 18 | 12 | CDP | focused |
| archeopunk city night | HIGH | OPERATIONAL | 11.01 | 249.7 | 249.7 | 4 | 60.24 | 4 | 20001 | 1 | 60 | 12 | CDP | focused |
| DEBUG light grid | DEBUG | DEBUG | 23.35 | 149.8 | 149.9 | 6.67 | 60.24 | 6 | 9000 | 0 | 12 | 12 | CDP | focused |
| material placement water/fire/smoke/stone/neon | HIGH | OPERATIONAL | 7.51 | 316.4 | 316.4 | 3.16 | 60.24 | 4 | 20002 | 4 | 24 | 12 | CDP | focused |
| 100 agents + light engine active | HIGH | OPERATIONAL | 6.77 | 316.4 | 316.4 | 3.16 | 60.24 | 4 | 20001 | 4 | 66 | 100 | CDP | focused |

## Notes

- Focused benchmark runner is local-only. Browser focus is verified with document.hasFocus and visibilityState.
- Focused browser was observed by the app.
- Light budget and dirty-signature cache are enabled for v1.1.1.
- Local focus attempt: focused_by_pid
- Focused browser verified by document.hasFocus().
