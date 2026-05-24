# CODEX CHANGELOG v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

## Added

- `src/scene/` playable scene state, lighting and render overlay.
- `SceneInteractionPanel` with material/light tools, pause/play, step, weather,
  time, vibe preset, save/load and RPG export.
- VibeCoding preview, parsed intent and undo snapshot support.
- Headed Edge/CDP benchmark runner at `tools/run-headed-benchmark-v1_1.mjs`.
- v1.1 benchmark schema and tests.
- v1.1 visual screenshots and comparison report.

## Changed

- Light grid now consumes placed scene lights and emissive scene materials.
- Water/wet scene cells affect reflection approximation.
- Pixel realism metrics include playable scene material/light counts.
- RPG export includes placed materials, placed lights, vibe config and playable
  scene profile.
- OSIT panel reports playable scene cells/lights.

## Preserved

- Wabi execution disabled.
- No push, deploy, commit, cloud, MCP execution or new copied assets.
- Light/physics claims remain approximation-only.
