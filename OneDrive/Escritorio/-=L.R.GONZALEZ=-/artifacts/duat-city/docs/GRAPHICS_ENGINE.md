# GRAPHICS_ENGINE

## Scope

Motor grafico CPU-friendly sobre Canvas 2D. No usa WebGL ni Three.js. El renderer existente se conserva y se extiende con budget, chunks, overlays y metricas.

## Layers

1. terrain/tile base
2. roads/buildings
3. R/Phi_eff heatmap
4. FibMob overlay
5. agents
6. particles/effects
7. selection/UI overlays

## Sparse Chunks

- Chunk size default: `8x8` tiles.
- Un chunk es dirty si cambia tile, building, R/Phi_eff o si un agente cruza chunk.
- Pan/zoom fuerte puede forzar FULL render.

## FibMob Procedural

`mobiusField(tile.id, k)` alimenta:

- rareza visual
- variacion de color
- anomalía en ruins
- overlay de saturacion cuando `mu=0`

Esto es procedural/visual, no una afirmacion fisica.

## EML Graphics Budget

`computeGraphicsBudget(R, Phi_eff, cameraZoom, physicsR, tick)` devuelve:

- detalle de tile/agente
- particulas on/off
- sombras on/off
- heatmap on/off
- modo `FULL` o `DIRTY`
- direccion `EXPAND/HOLD/COMPRESS`
- razon determinista

Reglas:

- `R > 0.60` o `R_physics > 0.60`: `COMPRESS`
- `Phi_eff > 0.75` y `R < 0.20`: `EXPAND`
- tick FibMob comprimido (`muK(tick)=0`): `COMPRESS`

## Particles

Particulas baratas para task completion, BLOCK alert y ruin anomaly. Maximo teorico: 300. En `COMPRESS`, se deshabilitan.

## Tests

- `graphicsBudget.test.ts`
- `integrationV05.test.ts`
