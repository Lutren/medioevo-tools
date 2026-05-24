# VISUAL COMPARISON v1.0 to v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

## Screenshot Sets

v1.0 source:

- `docs/screenshots/v1_0/`

v1.1 new captures:

- `docs/screenshots/v1_1/city_beautiful.png`
- `docs/screenshots/v1_1/neon_rain.png`
- `docs/screenshots/v1_1/tavern_interior.png`
- `docs/screenshots/v1_1/water_reflection.png`
- `docs/screenshots/v1_1/fire_smoke.png`
- `docs/screenshots/v1_1/debug_light_grid.png`
- `docs/screenshots/v1_1/material_placement.png`
- `docs/screenshots/v1_1/vibe_coding_panel.png`

## Answers

Se ve mas como pixel-art realista: si, especialmente en escenas nocturnas,
rain/neon y overlays de material/light. Sigue siendo procedural.

Se ve mas jugable: si. v1.1 muestra panel de interaccion, materiales colocados,
luces colocadas, debug de escena y export RPG local.

La luz se comporta mejor: si. Fire/neon/light placements entran al light grid;
water/wet surfaces suben reflectance; smoke/fog dispersa.

Que falta para parecerse a referencias: sprites propios de edificios/agentes,
tiles isometricos dedicados, animaciones de agua/lluvia mas ricas y una pass de
occlusion/roof lighting mas especifica por asset.

Assets prioritarios despues:

- tile atlas isometrico legal/propio para road, water, brick, wood, ruin;
- agent sprite strip simple;
- window/neon/fire sprites pequeños;
- rain/smoke particles dedicados;
- UI icons propios para material/light tools.

## Boundary

No assets were copied for v1.1. Screenshots are generated QA artifacts.
