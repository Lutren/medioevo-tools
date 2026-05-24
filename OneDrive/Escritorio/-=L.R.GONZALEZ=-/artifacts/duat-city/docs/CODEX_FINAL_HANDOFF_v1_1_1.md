# CODEX FINAL HANDOFF v1.1.1

Fingerprint: DUAT-v1.1.1-FOCUSED-FPS-CLOSURE

## Estado

v1.1.1 converts the v1.1 benchmark gap into a reproducible local closure:
focused Edge/CDP benchmark, in-app focused runner, light budget optimization,
dirty-region helpers, playable QA sequence and final QA evidence.

## Evidence

- Focused benchmark JSON: `docs/PERFORMANCE_BENCHMARK_v1_1_1.json`.
- Benchmark report: `docs/PERFORMANCE_BENCHMARK_REPORT_v1_1_1.md`.
- Light optimization report: `docs/LIGHT_OPTIMIZATION_REPORT_v1_1_1.md`.
- Playable QA report: `docs/PLAYABLE_INTERACTION_QA_v1_1_1.md`.
- Test report: `docs/TEST_REPORT_v1_1_1.md`.
- Screenshots: `docs/screenshots/v1_1_1/`.
- Run dir: `qa_artifacts/release_validation/RUN_DUAT_FOCUSED_FPS_CLOSURE_v1_1_1_20260519/`.

## Final QA

- Tests PASS: 58 files / 232 tests.
- Typecheck PASS.
- Build PASS.
- HTTP smoke 200.
- Secret scan focalizado: count-only, no values printed, non-blocking.
- Boundary scan: Wabi disabled, no cloud/API, no MCP execution, no push/deploy/commit, no new public assets copied.

## Known Limitation

The browser focus was observed by the app, but CDP/rAF cadence is still uneven.
The optimized engine caps light cells and improves boundedness, but HIGH and
BEAUTIFUL remain below the 30 FPS target in automated runs.

## NextAction

Optimize postprocess/canvas work with offscreen cached layers and rerun a
manual owner-controlled 30s focused benchmark.
