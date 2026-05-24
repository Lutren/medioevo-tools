# TEST REPORT v1.1.1

Fingerprint: DUAT-v1.1.1-FOCUSED-FPS-CLOSURE

## Final QA

- `corepack pnpm --filter @workspace/duat-city run test`: PASS, 58 files / 232 tests.
- `corepack pnpm --filter @workspace/duat-city run typecheck`: PASS.
- `corepack pnpm --filter @workspace/duat-city run build`: PASS.
- HTTP smoke `http://127.0.0.1:18519/duat-city/`: 200.

## Added Tests

- `focusedBenchmarkRunner.test.ts`
- `lightBudget.test.ts`
- `dirtyRegions.test.ts`
- `playableInteractionQa.test.ts`

## QA Artifacts

- Run dir: `qa_artifacts/release_validation/RUN_DUAT_FOCUSED_FPS_CLOSURE_v1_1_1_20260519/`
- Benchmark JSON: `docs/PERFORMANCE_BENCHMARK_v1_1_1.json`
- Screenshots: `docs/screenshots/v1_1_1/`
- Boundary scan: `BOUNDARY_SCAN.json`
- Secret scan: `SECRET_SCAN_FOCUSED.json`

## Boundary

- Wabi disabled.
- No cloud/API.
- No MCP execution.
- No push/deploy/commit.
- No new assets copied into public. Screenshots are QA artifacts under docs.
