# CODEX Changelog v1.0

Fingerprint: `DUAT-v1.0-PIXEL-REALISM-LIGHT-PHYSICS`

## Added

- `Medioevo Pixel Realism Engine` modules under `src/pixelRealism`.
- Color theory pipeline under `src/color`.
- Logical light engine under `src/light`.
- Expanded material pixel/cell physics under `src/physicsField`.
- Deterministic VibeCoding scene authoring under `src/vibecoding`.
- Visual Engine, Light, Material and VibeCoding panels.
- Pixel realism metrics in OSIT and handoff.
- RPG export fields `visual_scene_profile` and `pixel_physics_profile`.
- RPG quest hooks for light, shadow, flooded passage, neon market, ruin crystal and reflection anomaly.
- v1.0 tests for color, dithering, light, materials, renderer, vibe parser, RPG visual export and integration.
- v1.0 screenshot set under `docs/screenshots/v1_0`.

## Preserved

- Existing city simulation.
- Existing quaternary timing gate.
- Existing OSIT, Agent Inspector, RPG export and Wabi design-only boundary.
- No new assets copied.
- No push, deploy, commit or public release.

## Boundary

The engine is physically inspired, not physically exact. It uses logical pixel/cell fields and Canvas 2D compositing, not path tracing, WebGPU or full screen-pixel physics.
