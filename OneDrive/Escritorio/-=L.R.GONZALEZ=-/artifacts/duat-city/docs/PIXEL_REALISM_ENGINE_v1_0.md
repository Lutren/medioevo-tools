# Medioevo Pixel Realism Engine v1.0

Fingerprint: `DUAT-v1.0-PIXEL-REALISM-LIGHT-PHYSICS`

## Scope

This engine is a local Canvas 2D upgrade for DUAT City. It implements pixel-art realism through logical world cells, deterministic light/color passes, atmosphere, water reflection approximation, bloom, dithering and VibeCoding scene authoring.

Boundary: this is a physically inspired light approximation for pixel-art realism. It is not full physical simulation, not path tracing and not screen-pixel rigid-body physics.

## Runtime Layers

- `src/color/*`: color space conversion, palettes, harmonies, Kelvin temperature, tone mapping, color grade and deterministic ordered dithering.
- `src/light/*`: logical light grid, point/directional lights, opacity, soft shadows, bounce approximation, emissive sources, water reflection and light metrics.
- `src/physicsField/*`: material definitions and logical `PixelCell` state for minimal matter/light behavior.
- `src/pixelRealism/*`: render quality presets, pass order, atmosphere, bloom, reflections, dither, pixel scale and metrics.
- `src/vibecoding/*`: local deterministic keyword parser from scene text/presets to render configuration.
- `src/components/*Panel.tsx`: Visual Engine, Light, Material and VibeCoding controls.

## Quality Presets

- `LOW`: 80x45 internal grid, no bounce, no bloom, simple shadows.
- `MEDIUM`: 160x90 internal grid, one bounce, cheap bloom, low reflections.
- `HIGH`: 320x180 internal grid, two light passes, bloom, reflections and fog.
- `BEAUTIFUL`: screenshot-focused cinematic profile, debug off and UI hidden for capture.
- `DEBUG`: light grid, material/pixel field and Q-state overlays.

## Integration

`App.tsx` computes `PixelRealismRuntime` every frame from current city state and visual config. `MainCanvas` passes it into `renderCity`, which preserves the existing renderer and adds the new passes around it.

`OSITPanel` now reports light health, color health, pixel field health, render quality, active vibe scene and Q-state summary. `generateHandoff` includes `pixel_realism`.

## Boundaries

- No cloud calls.
- No external API calls.
- No copied assets.
- No public release, push, deploy or commit.
- Wabi execution remains disabled by policy.
