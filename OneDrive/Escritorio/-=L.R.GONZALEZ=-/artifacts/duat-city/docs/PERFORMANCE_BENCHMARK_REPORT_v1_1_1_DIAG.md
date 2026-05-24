# PERFORMANCE BENCHMARK v1.1.1

Fingerprint: DUAT-v1.1.1-FOCUSED-FPS-CLOSURE

Local focused/headed benchmark attempted with Microsoft Edge and CDP. No MCP execution, cloud, external API, push, deploy or commit.

- URL: http://127.0.0.1:18519/duat-city/?benchmark=v1_1_1&durationMs=1200&browserMode=CDP
- Duration per scenario: 1200 ms
- Browser mode: CDP
- Focus status: focused
- Focused browser available: true
- Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0

| Scenario | Quality | View | avg FPS | p95 ms | p99 ms | min FPS | max FPS | dropped | active light cells | active material cells | particles | agents | browser mode | focus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| LOW 80x45 baseline | LOW | OPERATIONAL | 0.06 | 32607.8 | 32607.8 | 0.03 | 3.82 | 2 | 2572 | 0 | 12 | 12 | CDP | focused |
| MEDIUM 160x90 | MEDIUM | OPERATIONAL | 0.83 | 1200 | 1200 | 0.83 | 0.83 | 1 | 7210 | 0 | 12 | 12 | CDP | focused |
| HIGH 320x180 | HIGH | OPERATIONAL | 0.83 | 1200 | 1200 | 0.83 | 0.83 | 1 | 20000 | 0 | 12 | 12 | CDP | focused |
| BEAUTIFUL sunny/castle/lake | BEAUTIFUL | BEAUTIFUL | 53.05 | 32.1 | 80.6 | 12.41 | 116.28 | 2 | 28000 | 2 | 12 | 12 | CDP | focused |
| BEAUTIFUL neon rain street | BEAUTIFUL | BEAUTIFUL | 0.83 | 1200 | 1200 | 0.83 | 0.83 | 1 | 28001 | 4 | 66 | 12 | CDP | focused |
| warm interior tavern | HIGH | OPERATIONAL | 38.89 | 63.7 | 168.1 | 5.95 | 158.73 | 4 | 20002 | 1 | 18 | 12 | CDP | focused |
| archeopunk city night | HIGH | OPERATIONAL | 0.83 | 1200 | 1200 | 0.83 | 0.83 | 1 | 20001 | 1 | 60 | 12 | CDP | focused |
| DEBUG light grid | DEBUG | DEBUG | 12.01 | 499.5 | 499.5 | 2 | 60.24 | 5 | 9000 | 0 | 12 | 12 | CDP | focused |
| material placement water/fire/smoke/stone/neon | HIGH | OPERATIONAL | 7.3 | 399.7 | 399.7 | 2.5 | 60.24 | 4 | 20002 | 4 | 24 | 12 | CDP | focused |
| 100 agents + light engine active | HIGH | OPERATIONAL | 15.92 | 183.3 | 199.8 | 5.01 | 60.24 | 6 | 20001 | 4 | 66 | 100 | CDP | focused |

## Notes

- Focused benchmark runner is local-only. Browser focus is verified with document.hasFocus and visibilityState.
- Focused browser was observed by the app.
- Light budget and dirty-signature cache are enabled for v1.1.1.
- Local focus attempt: focused_by_pid
- Focused browser verified by document.hasFocus().
