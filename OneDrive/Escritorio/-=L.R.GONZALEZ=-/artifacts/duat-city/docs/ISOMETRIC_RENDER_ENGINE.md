# ISOMETRIC_RENDER_ENGINE

## Scope

Canvas 2D renderer with 2.5D/isometric-style primitives. No WebGL, no shader dependency.

## Files

- `src/graphics/isoMath.ts`
- `src/graphics/tileRenderer.ts`
- `src/graphics/buildingRenderer.ts`
- `src/graphics/agentRenderer.ts`
- `src/graphics/lightEngine.ts`
- `src/graphics/shadowEngine.ts`
- `src/render/canvasRenderer.ts`

## Implemented

- Grid/screen isometric math utilities.
- Deterministic depth sorting.
- Diamond-style tile drawing.
- Raised building masses with simple roofs and shadows.
- Agent sprites with need markers and gate state.
- Deterministic ambient and point light maps.

## Limit

The current click/pan camera remains compatible with the original orthographic grid. A future pass can migrate input picking to `screenToGrid`.
