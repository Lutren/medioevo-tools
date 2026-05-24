# CODEX FINAL HANDOFF v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

## Estado

DUAT v1.1 implements a playable local scene authoring loop on top of the v1.0
Pixel Realism Engine.

## Evidence

- Baseline: 49 files / 202 tests PASS; typecheck PASS; build PASS; HTTP 200.
- Final QA: 54 files / 219 tests PASS; typecheck PASS; build PASS; HTTP 200.
- Headed Edge/CDP benchmark generated `docs/PERFORMANCE_BENCHMARK_v1_1.json`.
- Screenshots generated under `docs/screenshots/v1_1/`.
- Final QA summary recorded in `qa_artifacts/release_validation/RUN_DUAT_PLAYABLE_SCENE_QA_v1_1_20260519/FINAL_QA_SUMMARY.json`.

## Important Caveat

The headed benchmark ran in visible Edge, but the automation context throttled
frame cadence. Treat the numbers as headed scenario coverage and finite metrics,
not final human-facing FPS. A manual focused headed run remains useful.

## Boundary

- Wabi disabled.
- No new copied assets.
- No cloud/API.
- Boundary scan false positives classified as local-only Edge CDP, local manifest fetch, and safety regex.
- No MCP execution.
- No push/deploy/commit.
- No exact-physics or path-tracing claim.

## Next Verifiable Action

Run a manual focused gameplay pass in the visible browser and record actual FPS
while interacting with material/light placement.
