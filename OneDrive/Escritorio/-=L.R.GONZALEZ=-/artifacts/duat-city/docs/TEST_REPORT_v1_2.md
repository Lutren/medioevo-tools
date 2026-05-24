# TEST_REPORT_v1_2

Fingerprint: DUAT-v1.2-ASSET-AWARE-PIXEL-GAME-ENGINE

## Final QA

- `corepack pnpm --filter @workspace/duat-city run test`: PASS, 71 files / 260 tests.
- `corepack pnpm --filter @workspace/duat-city run typecheck`: PASS after rerun.
- `corepack pnpm --filter @workspace/duat-city run build`: PASS after rerun.
- HTTP smoke `http://127.0.0.1:18519/duat-city/`: 200.
- Secret scan focalizado `artifacts/duat-city`: `count_reported=0`.
- Boundary scan: copied v1.2 assets `0`, Wabi false flags present, no actual `publication_allowed=true`, no external API calls in v1.2 modules.

## Logs

Run dir:

`qa_artifacts/release_validation/RUN_DUAT_ASSET_AWARE_PIXEL_ENGINE_v1_2_20260519/`

Key files:

- `BASELINE_TEST.log`
- `BASELINE_TYPECHECK.log`
- `BASELINE_BUILD.log`
- `HTTP_SMOKE.log`
- `FINAL_TEST_RERUN.log`
- `FINAL_TYPECHECK_RERUN.log`
- `FINAL_BUILD_RERUN.log`
- `FINAL_HTTP_SMOKE.log`
- `SECRET_SCAN_FOCUSED_COUNT_ONLY.log`
- `BOUNDARY_SCAN.log`
