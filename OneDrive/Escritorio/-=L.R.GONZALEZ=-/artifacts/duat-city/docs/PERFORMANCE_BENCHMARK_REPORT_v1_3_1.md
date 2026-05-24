# PERFORMANCE BENCHMARK v1.3.1

Fingerprint: DUAT-v1.3.1-AUDIO-GAMEFEEL-CONTINUITY

Benchmark local reproducible ejecutado con:

```txt
node tools/run-audio-gamefeel-benchmark-v1_3_1.mjs 160 docs/PERFORMANCE_BENCHMARK_v1_3_1.json
```

El benchmark mide el costo de mapping de cues y game-feel, no reproduccion real por AudioContext. Browser audio queda off-by-default hasta gesto humano.

| Scenario | avg map ms | p95 map ms | cues | R_audio | Phi_audio |
|---|---:|---:|---:|---:|---:|
| baseline city silent/off | 0.438 | 2.382 | 1 | 0.024 | 1.000 |
| fire plus smoke material cue stack | 0.540 | 1.437 | 5 | 0.177 | 0.953 |
| neon rain street cues | 1.613 | 2.156 | 10 | 0.302 | 0.884 |
| agent needs and R cue budget | 1.391 | 2.625 | 23 | 0.495 | 0.778 |
| RPG gate transition cue set | 0.566 | 2.238 | 4 | 0.121 | 0.983 |
| metroidvania gate and ruin anomaly | 0.774 | 3.453 | 5 | 0.195 | 0.943 |

## Resultado

- JSON: `docs/PERFORMANCE_BENCHMARK_v1_3_1.json`
- Escenarios: 6
- Iteraciones por escenario: 160
- Audio de navegador usado: false
- Resultado: todos los campos finitos.

## Nota de rendimiento

La presion mas alta aparece en `agent_stress` por 23 cues. El presupuesto de `src/pixelRealism/gameFeelPerformance.ts` capea cues y pulsos por preset para no arrastrar el render.
