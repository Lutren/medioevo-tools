# NEXT_SESSION_BRIEF DUAT v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

## Estado

Playable scene authoring is implemented and tested. The app now supports local
material/light placement, scene stepping, VibeCoding apply/undo, scene JSON
save/load and RPG export with visual/material/light data.

## Evidencia

- `docs/PERFORMANCE_BENCHMARK_v1_1.json`
- `docs/PERFORMANCE_BENCHMARK_REPORT_v1_1.md`
- `docs/screenshots/v1_1/`
- `docs/PLAYABLE_SCENE_QA_v1_1.md`
- `docs/LIGHT_BEHAVIOR_QA_v1_1.md`
- `docs/VIBE_CODING_USABILITY_v1_1.md`
- `docs/VISUAL_COMPARISON_v1_0_to_v1_1.md`

## Riesgos

- Headed FPS numbers are throttled by automation context.
- Visual quality is still procedural and needs own/legal art assets before a
  stronger reference match.

## Bloqueos

- No asset import without allowlist.
- Wabi execution stays disabled.
- No push/deploy/commit/cloud/MCP.

## Proxima accion verificable

Manual human-visible gameplay pass: place water, fire/smoke, neon and stone in
the browser while checking FPS and RPG export output.

## Segunda perdida

Los datos persisten. El operador no. Recalibrar desde este brief, no desde
memoria implicita.
