# TEST REPORT v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

## Final QA

- `corepack pnpm --filter @workspace/duat-city run test`: PASS, 54 test files / 219 tests.
- `corepack pnpm --filter @workspace/duat-city run typecheck`: PASS.
- `corepack pnpm --filter @workspace/duat-city run build`: PASS.
- HTTP smoke `http://127.0.0.1:18519/duat-city/`: 200.

## Evidence

- Run dir: `qa_artifacts/release_validation/RUN_DUAT_PLAYABLE_SCENE_QA_v1_1_20260519/`.
- Test log: `FINAL_TEST.log`.
- Typecheck log: `FINAL_TYPECHECK.log`.
- Build log: `FINAL_BUILD.log`.
- HTTP smoke log: `FINAL_HTTP_SMOKE.log`.
- QA summary: `FINAL_QA_SUMMARY.json`.

## Added Coverage

- `sceneInteraction.test.ts`: material placement, erase, light placement, save/load, finite state.
- `vibeParserUsability.test.ts`: night/rain/neon, warm tavern, fog/reflection/water, archeopunk sunset, undo snapshot.
- `lightBehavior.test.ts`: fire/neon emission, water reflection, smoke scatter, wet reflectance.
- `performanceBenchmarkV11.test.ts`: benchmark schema and required scenarios.
- `rpgSceneExport.test.ts`: placed materials, lights, vibe config, hazards and quest hooks.

## Boundary QA

- Wabi execution flags remain disabled.
- No `publication_allowed=true`.
- No new copied production assets.
- No push, deploy, commit or cloud API.
- Local headed benchmark uses `127.0.0.1` and Edge CDP only.

## Residual Risk

The headed benchmark produced finite metrics in a visible Edge window, but frame
cadence was strongly throttled by the automated run. Treat the JSON as scenario
coverage and a benchmark harness proof, not as a final human-facing FPS ceiling.
