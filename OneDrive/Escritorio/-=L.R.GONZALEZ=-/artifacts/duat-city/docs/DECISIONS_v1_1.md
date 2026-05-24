# DECISIONS v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

- Implement v1.1 as a playable local scene layer on top of the existing DUAT city and Pixel Realism Engine.
- Keep all scene authoring deterministic and local; VibeCoding remains keyword/parser based with no AI/API/cloud calls.
- Use procedural material/light overlays and generated QA screenshots only; no copied production assets.
- Use local Edge DevTools Protocol on `127.0.0.1` for the visible benchmark harness because Browser MCP execution is disallowed by the task boundary.
- Preserve the claim boundary: light and material behavior is a physically inspired approximation for pixel-art realism, not exact physics or path tracing.
- Keep Wabi execution disabled and leave push/deploy/commit/publication out of scope.
