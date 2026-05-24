# PLAYABLE INTERACTION QA v1.1.1

Fingerprint: DUAT-v1.1.1-FOCUSED-FPS-CLOSURE

## Sequence

The local QA sequence is available from the Playable Scene panel as
`Run QA Sequence`.

It executes:

1. apply `neon_rain_street`;
2. place water;
3. place fire;
4. place smoke;
5. place stone;
6. place neon;
7. erase one placed cell;
8. switch to night;
9. switch visual mode toward Beautiful;
10. export scene JSON;
11. export RPG scene JSON.

## Verified

- Controls are wired through the playable scene state.
- Materials affect scene metrics and render overlays.
- Fire and neon contribute emissive cells/lights.
- RPG export includes placed materials, placed lights and vibe config.
- Tests verify no NaN in the QA sequence.
- Wabi execution flags remain false.

## Evidence

- `src/tests/playableInteractionQa.test.ts`: PASS.
- Screenshot: `docs/screenshots/v1_1_1/material_interaction_water_fire_smoke_neon.png`.
- RPG screenshot: `docs/screenshots/v1_1_1/rpg_scene_export_visual_profile.png`.
