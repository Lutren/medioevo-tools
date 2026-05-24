# PLAYABLE SCENE QA v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

## Scope

DUAT v1.1 turns the Pixel Realism Engine into a usable local scene loop. The
new scene layer is deterministic, local-only and serializable. It does not call
AI, cloud APIs, MCP execution or external services.

## Implemented Interaction Loop

- Click-select city tile/building/agent remains available through the City tool.
- Scene tools add material cells, light sources, selection and erase.
- Materials supported: water, fire, smoke, stone, wood and neon.
- Lights supported: torch, window, neon, fire, magic, signal and ruin anomaly.
- Scene pause/play and one-step advance are exposed in `SceneInteractionPanel`.
- Time of day and weather can be changed directly.
- Vibe presets can be applied to the playable scene.
- Scene JSON can be saved and loaded locally.
- RPG scene JSON export includes visual, material and light data.

## QA Result

- `sceneInteraction.test.ts`: place material, erase material, place light,
  save/load scene and no-NaN stepping pass.
- Interaction state affects render overlays, pixel realism metrics and RPG
  export.
- Pixel/cell physics remains a logical cell approximation, not screen-pixel
  rigid-body physics.

## Boundary

- Wabi execution remains disabled.
- No assets copied.
- No cloud/API.
- No push, deploy or commit.
