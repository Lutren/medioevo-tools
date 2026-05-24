# PERFORMANCE BENCHMARK v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

Visible headed browser benchmark executed locally with Microsoft Edge and CDP automation. No MCP execution, cloud, external API, push, deploy or commit.

- URL: http://127.0.0.1:18519/duat-city/?benchmark=v1_1&durationMs=1000
- Duration per scenario: 1000 ms
- Browser visible: true
- Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0

| Scenario | Quality | avg FPS | p95 frame ms | min FPS | max FPS | dropped | active light cells | active material cells | particles | agents | pixel field |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| LOW 80x45 | LOW | 3.12 | 349.8 | 2.86 | 3.53 | 4 | 3600 | 345 | 12 | 12 | 80x45 |
| MEDIUM 160x90 | MEDIUM | 1.77 | 599.5 | 1.67 | 1.88 | 2 | 14400 | 345 | 12 | 12 | 160x90 |
| HIGH 320x180 | HIGH | 0.46 | 2164.9 | 0.46 | 0.46 | 1 | 57600 | 345 | 12 | 12 | 320x180 |
| BEAUTIFUL | BEAUTIFUL | 0.4 | 2481.3 | 0.4 | 0.4 | 1 | 57600 | 347 | 12 | 12 | 320x180 |
| DEBUG light grid | DEBUG | 3.2 | 333.1 | 3 | 3.53 | 4 | 14400 | 345 | 12 | 12 | 160x90 |
| neon rain street | HIGH | 0.63 | 1598.7 | 0.63 | 0.63 | 1 | 57601 | 349 | 66 | 12 | 320x180 |
| warm interior tavern | HIGH | 0.55 | 1815.3 | 0.55 | 0.55 | 1 | 57602 | 349 | 27 | 12 | 320x180 |
| archeopunk city night | HIGH | 0.61 | 1632 | 0.61 | 0.61 | 1 | 57601 | 346 | 60 | 12 | 320x180 |
| 50 agents | MEDIUM | 2.47 | 449.6 | 2.22 | 2.61 | 3 | 14400 | 339 | 12 | 50 | 160x90 |
| 100 agents | MEDIUM | 2.31 | 449.6 | 2.22 | 2.4 | 3 | 14400 | 331 | 12 | 100 | 160x90 |

## Notes

- Visible headed browser run via local Edge/CDP, no MCP execution.
- requestAnimationFrame frame deltas measured in the app page; timeout fallback resolves if the visible window is focus-throttled.

## Interpretation

The benchmark executed in a visible Edge window, but the frame cadence is strongly
throttled in this automation context. Treat these numbers as headed-run evidence
and scenario coverage, not as a final user-facing FPS ceiling. A manual focused
headed run is still needed for true gameplay FPS.
