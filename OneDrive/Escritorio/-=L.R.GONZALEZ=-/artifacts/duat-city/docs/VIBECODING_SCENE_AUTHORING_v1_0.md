# VibeCoding Scene Authoring v1.0

VibeCoding is a local deterministic scene compiler in `src/vibecoding`.

## Purpose

It converts text such as:

`haz una calle lluviosa de noche con luces neon cian y ambar, charcos reflectantes, humo saliendo del mercado, agentes caminando lento`

into a `VibeSceneConfig` with time of day, weather, palette, light profile, fog, wetness, particles, camera preset, density, mood and materials.

## Presets

- `sunny_castle_lake`
- `neon_rain_street`
- `warm_interior_tavern`
- `winter_tree_reflection`
- `jungle_waterfall_ruin`
- `desert_skyline`
- `archeopunk_city_night`
- `observatory_light_burst`
- `eye_color_study`
- `wheatfield_cloudscape`

## UI

`src/components/VibeCodingPanel.tsx` adds prompt textarea, preset dropdown, compile, apply and copy JSON controls. The panel states that parsing is local deterministic and uses no cloud.

## Boundary

No AI execution, no cloud, no external API and no MCP execution.
