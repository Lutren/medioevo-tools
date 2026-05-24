# ENGINE_AND_SIM_AUDIT

## CERTEZA

- `artifacts/duat-city` es el motor visual web-first real.
- Stack: Vite + React + Canvas 2D/iso, con tests Vitest.
- No hay proyecto Godot activo encontrado en rutas no protegidas auditadas.
- GEODIA Smallville ya tiene simulacion CPU-only sintetica y replay verifier.
- El renderer actual usa Canvas y rango visible por camara; no hay pipeline WebGL/WebGPU principal.

## Simulacion

Fortalezas:
- `tickEngine` existe y cierra ciclo buildings -> tasks -> agents -> physics field -> relationships -> R/Phi_eff -> events -> witness.
- `computeGlobalR` usa guardas contra division por cero.
- Fisica tiene guardas de NaN y distancia minima.
- Se corrigio aleatoriedad de sim/RPG para usar random determinista o inyectable.

Riesgos:
- `tickEngine` aun corre dentro de flujo React/App, no en worker.
- `quaternaryAdapter` mantiene sensor bank global de modulo; replay completo intercalado no es puro.
- Witness IDs usan contador global en `core/witnesslog.ts`; pendiente para replay 100%.

## Render

Fortalezas:
- `canvasRenderer.ts` cullea por viewport/camara.
- `lightBudget.ts` define presets por calidad.
- `lightPropagation.ts` tiene grid local, opacidad, fuentes, bounce opcional y fog.
- `isoPerformanceBudget.ts` limita sprites y luces dinamicas.

Riesgos:
- `graphics/lightEngine.ts`, `lightPropagation.ts` y `vermeerIsoLighting.ts` no estan unificados.
- Sprites/agentes son mayormente procedurales y no tienen normal/depth maps.
- No hay chunk streaming formal con worker/offscreen.
- El loop de render/sim depende demasiado de React state para alto conteo de agentes.

## Audio

Fortalezas:
- Audio procedural se activa solo con gesto/enable.

Riesgos:
- `proceduralSynth.disable()` no cierra `AudioContext` ni desconecta nodos pendientes.
- Faltan pruebas de liberacion de recursos.

## QA ejecutado

- `npm run typecheck`: PASS.
- `npm run test -- src/tests/engine.test.ts src/tests/rpgExport.test.ts src/tests/rpgWorldV2.test.ts`: PASS, 20 tests.
- `rg -n "Math.random" src`: queda solo `src/components/ui/sidebar.tsx`, placeholder visual no-core.

