# MEDIOEVO_RPG_ENGINE_EXPORT v2/v3

Estado: `v2` queda como contrato historico. El exportador vivo en
`src/rpg/worldExport.ts` emite `schema: medioevo-rpg/world/v3`.

Schema historico: `medioevo-rpg/world/v2`
Schema actual: `medioevo-rpg/world/v3`

## Relacion Con Godot RPG

`duat-city` exporta estado de ciudad, perfiles de fisica, escena visual,
materiales pixel, resumen de campo, rutas de agentes y handoff hacia el RPG.
El proyecto Godot privado `E:\Medioevo_RPG` consume su propio puente vivo por
`WorldPulseBridge` (`medioevo.WorldPulseBridge.v1`) y mantiene la validacion
headless en `tools/campaign/Validate*.tscn`.

Estos motores son complementarios:

- `duat-city`: simulacion web/TS, ciudad, agentes, fisica y export RPG.
- `E:\Medioevo_RPG`: juego Godot privado, runtime jugable y puente WorldPulse.

No se debe copiar runtime completo entre ambos. La integracion se mantiene por
contratos, manifests y validaciones.

## Campos Agregados En v2

- `map_tiles`
- `districts`
- `landmarks`
- `NPC schedules`
- `faction_control`
- `danger_zones`
- `light_zones`
- `environmental_hazards`
- `visual_asset_manifest_refs`
- `physics_field_summary`
- `suggested_scenes`

## Campos Agregados En v3

- `visual_scene_profile`
- `pixel_physics_profile`
- `art_direction_profile`
- `audio_gamefeel_profile`
- `style_tokens`
- `material_field_summary`
- `light_field_summary`
- `vibe_command_history`
- `agent_routes`
- `interaction_points`
- `playable_scene_profile`
- `game_os_profile`
- `language_profile`
- `brain_runtime_profile`
- `osit_formula_profile`
- `cosmology_profile`
- `rpg_metroidvania_bridge`
- `handoff`

## Hazard Hooks

Quests can now emerge from:

- fire outbreak
- flooded district
- blocked route
- ruin anomaly
- food shortage
- low trust/social conflict
- signal anomaly

## Tests

- `src/tests/rpgWorldV2.test.ts`
- `src/tests/rpgExportV3.test.ts`
- existing RPG export tests updated to current v3 schema
- `src/tests/rpgExport.test.ts`
- `src/tests/rpgVisualExport.test.ts`
- `src/tests/rpgVisualSceneExport.test.ts`
- `src/tests/rpgSceneExport.test.ts`
- `src/tests/rpgPhysicsExport.test.ts`
- `src/tests/rpgAudioGameFeelExport.test.ts`
- `src/tests/rpgMetroidvaniaBridge.test.ts`
