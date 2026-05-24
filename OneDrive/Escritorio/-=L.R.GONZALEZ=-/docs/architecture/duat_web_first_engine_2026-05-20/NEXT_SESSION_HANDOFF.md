# NEXT_SESSION_HANDOFF DUAT WEB-FIRST ENGINE

## Estado

- Ruta principal recomendada: C HIBRIDA.
- Ruta fallback: B CUSTOM WEB ENGINE.
- Godot queda como cliente opcional bajo REVIEW.
- DUAT City ya tiene parche local para random determinista/injectable en sim/RPG.

## Evidencia

- `npm run typecheck`: PASS.
- `npm run test -- src/tests/engine.test.ts src/tests/rpgExport.test.ts src/tests/rpgWorldV2.test.ts`: PASS, 20 tests.
- `rg -n "Math.random" src`: solo queda placeholder UI en sidebar.
- ZIPs relevantes inspeccionados por metadata, sin extraccion.

## Pendientes reales

1. Mover quaternary sensor bank a estado/runtime inyectado.
2. Cambiar witnesslog counter global a replay hash/state-local.
3. Extraer `DUAT_SIM_CORE` fuera de React.
4. Crear `RenderSnapshot` y backend renderer.
5. Unificar light engines bajo `LightingBackend`.
6. Crear benchmark GLOMO.
7. Crear sprite-lighting benchmark.

## Riesgos

- Adopcion cruda de zips: BLOCK.
- Publicacion/deploy/push: BLOCK.
- Cloud sin ProviderGate/cache: REVIEW/BLOCK.
- Material protegido RPG/canon: BLOCK fuera de lectura local segura.

## Proxima accion verificable

Implementar replay hash v0.1 y eliminar estado global de `witnesslog`/`quaternaryAdapter` para que un replay completo, incluido witness/quaternary, sea reproducible.

