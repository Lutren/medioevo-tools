# TEST REPORT v1.3.1

Fingerprint: DUAT-v1.3.1-AUDIO-GAMEFEEL-CONTINUITY

## Final QA

| Check | Resultado |
|---|---|
| Tests | PASS: 92 files / 292 tests |
| Typecheck | PASS |
| Build | PASS |
| HTTP smoke | PASS: HTTP 200 |
| Secret scan | high_confidence_secret_count=0 |
| Boundary scan | publication_allowed true property count=0 |
| Wabi scan | Wabi execution true property count=0 |
| Asset copy scan | new/external asset copy true property count=0 |

## Comandos

```txt
corepack pnpm --filter @workspace/duat-city run test
corepack pnpm --filter @workspace/duat-city run typecheck
corepack pnpm --filter @workspace/duat-city run build
Invoke-WebRequest http://127.0.0.1:18519/duat-city/
node tools/run-audio-gamefeel-benchmark-v1_3_1.mjs 160 docs/PERFORMANCE_BENCHMARK_v1_3_1.json
node tools/capture-screenshots-v1_3_1.mjs docs/screenshots/v1_3_1 18573 http://127.0.0.1:18519/duat-city/
```

## Logs

Run dir:

`qa_artifacts/release_validation/RUN_DUAT_AUDIO_GAMEFEEL_v1_3_1_20260520`

- `FINAL_TEST.log`
- `FINAL_TYPECHECK.log`
- `FINAL_BUILD.log`
- `FINAL_HTTP_SMOKE.log`
- `SECRET_SCAN.log`
- `BOUNDARY_SCAN.log`
