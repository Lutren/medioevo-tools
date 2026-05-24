# PERFORMANCE_BENCHMARK_REPORT_v1_2

Fingerprint: DUAT-v1.2-ASSET-AWARE-PIXEL-GAME-ENGINE

- Browser mode: CDP
- Focus status: focused
- Focused browser available: True
- Duration per scenario: 1000 ms
- v1.1.1 avg FPS baseline: 8.71
- v1.2 avg FPS measured: 11.44
- v1.1.1 worst p95 frame ms: 77120.1
- v1.2 worst p95 frame ms: 19200.9

## Scenario Results

| Scenario | Quality | View | avg FPS | p95 ms | dropped | active light cells | active material cells | focus |
|---|---|---|---:|---:|---:|---:|---:|---|
| LOW 80x45 baseline | LOW | OPERATIONAL | 0.1 | 19200.9 | 2 | 1800 | 0 | focused |
| MEDIUM 160x90 | MEDIUM | OPERATIONAL | 1 | 1000 | 1 | 7200 | 0 | focused |
| HIGH 320x180 | HIGH | OPERATIONAL | 1 | 1000 | 1 | 20000 | 0 | focused |
| BEAUTIFUL sunny/castle/lake | BEAUTIFUL | BEAUTIFUL | 11.06 | 316.4 | 3 | 28000 | 2 | focused |
| BEAUTIFUL neon rain street | BEAUTIFUL | BEAUTIFUL | 51.64 | 33.8 | 3 | 28001 | 4 | focused |
| warm interior tavern | HIGH | OPERATIONAL | 1 | 1000 | 1 | 20002 | 1 | focused |
| archeopunk city night | HIGH | OPERATIONAL | 11.01 | 249.7 | 4 | 20001 | 1 | focused |
| DEBUG light grid | DEBUG | DEBUG | 23.35 | 149.8 | 6 | 9000 | 0 | focused |
| material placement water/fire/smoke/stone/neon | HIGH | OPERATIONAL | 7.51 | 316.4 | 4 | 20002 | 4 | focused |
| 100 agents + light engine active | HIGH | OPERATIONAL | 6.77 | 316.4 | 4 | 20001 | 4 | focused |

## Notes

- Measured the v1.2 codebase using the existing local focused benchmark protocol.
- The app was served from localhost and measured through local Edge/CDP; no MCP, cloud, external API, push, deploy or commit.
- FPS remains limited by canvas/postprocess/light-cell cost in HIGH/BEAUTIFUL; v1.2 adds cache boundaries and procedural fallback but does not claim full renderer rewrite.
