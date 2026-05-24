# DUAT_RENDER_STRATEGY_WEB_FIRST

## Target

- Web-first.
- Low tier: CPU/RAM friendly, Canvas 2D/2.5D, minimal allocations.
- High tier: optional WebGL/Three.js/WebGPU if benchmark proves value.
- Cloud optional only for precompute/enrichment, not required for play.

## Render modes

### Ciudad 3D

- Low tier: isometric/2.5D Canvas with billboards and height cues.
- High tier: Three.js/WebGL chunked city if FPS/memory allow.
- State source: same `WorldState`.

### Calabozos 2.5D

- Tile/chunk renderer.
- Portal culling and occlusion culling are high value.
- Light grid local per room/camera.

### Metroidvania 2D/2.5D

- Side-view tilemaps.
- Layers/parallax/pseudo-Z.
- Sprite normal maps for high tier.

## Efficiency techniques

- Frustum culling: active now at Canvas viewport level; formalize per chunk.
- Occlusion culling: add for dungeons/cities with walls/buildings.
- Portal culling: high priority for interiors.
- Chunk streaming: load/sim/render around camera.
- Asset streaming: atlas and lazy image decode.
- LOD: existing `lod-controller-v2.ts`; bind to agent count and budget.
- Impostors/billboards: keep as default for people/crowds.
- Instancing: high tier WebGL path.
- Object pooling: needed for particles/light cells/tasks overlays.
- Atlas textures: required for sprites/tiles.
- Virtual textures: only if WebGL high tier needs huge maps.
- Async loading: required for chunks/assets.
- Worker/off-thread simulation: P0 for scale.
- Fixed timestep: P0 for replay.
- Sparse updates: event-driven agents/objects outside camera.
- Camera-based activation: P0.

## Render architecture

```txt
DUAT_SIM_CORE -> RenderSnapshot -> RendererBackend

RendererBackend:
  - canvas-low
  - canvas-iso
  - webgl-high
  - godot-client-optional
```

React should own UI/HUD/inspectors, not the hot sim/render loop.

