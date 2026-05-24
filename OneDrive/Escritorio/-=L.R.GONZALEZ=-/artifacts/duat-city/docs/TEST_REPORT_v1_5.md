# TEST REPORT v1.5

Fingerprint: DUAT-v1.5-FULL-LOCAL-REVIEW

## Summary
- Overall: PASS
- Tests: 106 files / 313 tests PASS
- Typecheck: PASS
- Build: PASS
- Windows app build: PASS
- Smoke: PASS

## Commands
| Status | Command | Evidence |
|---|---|---|
| PASS | `python tools\release\pending_review.py --write --quiet` | pending_review date=2026-05-20 active_dedup=32 claudio_open=0 |
| PASS | `node tools\scan-local-review-v1_5.mjs docs\asset_manifest_v1_5.json <roots>` | filesSeen=8638; relevantFiles=4095; zipEntriesIncluded=4445 |
| PASS | `corepack pnpm --filter @workspace/duat-city run test` | 106 test files / 313 tests passed |
| PASS | `corepack pnpm --filter @workspace/duat-city run typecheck` | tsc -p tsconfig.json --noEmit |
| PASS | `corepack pnpm --filter @workspace/duat-city run build` | vite build completed; 249 modules transformed |
| PASS | `corepack pnpm --filter @workspace/duat-city run winapp:build` | DUATCity.exe sha256=12731EC7C6CF0E1D662C3DB87C17D717DFFD89BD9DE0F03C31821D0A11E0969E |
| PASS | `corepack pnpm --filter @workspace/duat-city run winapp:smoke` | httpStatus=200; jsAssetStatus=200 |
| PASS | `node tools\run-winapp-benchmark-v1_4.mjs docs\PERFORMANCE_BENCHMARK_v1_5.json ...` | minAppAvgFps=59.9; threshold=30 |
| PASS | `node tools\run-winapp-qa-v1_5.mjs docs\v1_5_winapp_qa ...` | screenshots=8; allNonblank=true; proceduralPreviewConfirmed=true |
| PASS | `node --check tools\scan-local-review-v1_5.mjs && node --check tools\run-winapp-qa-v1_5.mjs` | syntax checks passed |

## Benchmark
| Scenario | app avg FPS | app p95 frame ms | dropped frames | Status |
|---|---:|---:|---:|---|
| high_iso3d_operational | 59.9 | 16.7 | 1 | PASS |
| beautiful_vermeer_city | 60.18 | 16.8 | 0 | PASS |
| debug_osit_formula_lab | 60.16 | 16.7 | 0 | PASS |

## Visual QA
- Status: PASS
- Screenshots: 8
- All nonblank: true
- Directory: C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\artifacts\duat-city\docs\v1_5_winapp_qa\screenshots

## Audio QA
- Status: PASS
- Browser audio available: true
- Procedural preview: true
- Cue count: 22
- Human audible confirmation: false

## Asset Review
- Files seen: 8638
- Relevant files: 4095
- Zip files seen: 20
- Zip entries included: 4445
- Classification counts: {"reference_only":7211,"allowlist":823,"reject":46,"adapt":475}
