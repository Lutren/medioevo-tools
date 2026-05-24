# Test Report v1.3.2

Final commands:
- `corepack pnpm --filter @workspace/duat-city run test`
- `corepack pnpm --filter @workspace/duat-city run typecheck`
- `corepack pnpm --filter @workspace/duat-city run build`
- HTTP smoke: `http://127.0.0.1:18519/duat-city/`

Results:
- tests: PASS, 100 files / 303 tests
- typecheck: PASS
- build: PASS
- HTTP smoke: 200

Logs:
- `qa_artifacts/release_validation/RUN_DUAT_LOVABLE_ISO_EXTRACTION_v1_3_2_20260520/FINAL_TEST.log`
- `qa_artifacts/release_validation/RUN_DUAT_LOVABLE_ISO_EXTRACTION_v1_3_2_20260520/FINAL_TYPECHECK.log`
- `qa_artifacts/release_validation/RUN_DUAT_LOVABLE_ISO_EXTRACTION_v1_3_2_20260520/FINAL_BUILD.log`
- `qa_artifacts/release_validation/RUN_DUAT_LOVABLE_ISO_EXTRACTION_v1_3_2_20260520/FINAL_HTTP_SMOKE.log`

Boundary scan:
- no Wabi true flags detected.
- no cloud/push/deploy/commit/MCP true flags detected.
- boundary phrase matches in older docs are textual report lines, not active true assignments.
