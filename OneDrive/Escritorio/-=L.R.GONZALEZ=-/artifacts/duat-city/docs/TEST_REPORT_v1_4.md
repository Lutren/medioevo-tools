# Test Report v1.4

Baseline:
- tests: PASS, 104 files / 309 tests.
- typecheck: PASS.
- build: PASS.
- HTTP smoke: 200.

New focused tests:
- `ositFormulaRegistry.test.ts`: PASS.
- `duatOSITFullInventory.test.ts`: PASS.
- `rpgOSITIntegration.test.ts`: PASS.
- `performanceBenchmarkV14.test.ts`: PASS.
- `audioHeadedQaV14.test.ts`: PASS.
- `brainRuntime.test.ts`: PASS.

Benchmark:
- `docs/PERFORMANCE_BENCHMARK_v1_4.json`
- fallback mode: Edge/CDP/headless-frame-sampler with internal app FPS snapshot reset.
- headed FPS verified: false.
- focused benchmark runner timeout: documented.
- static render benchmark: High 34.69 FPS external / 32.48 FPS app, Beautiful 50.2 FPS external / 49.1 FPS app, Debug 54.8 FPS external / 53.73 FPS app.

Audio QA:
- `docs/AUDIO_HEADED_QA_v1_4.json`
- headed attempt: timed out in local Edge/CDP automation.
- fallback mode: Edge/CDP/headless-fallback.
- audio off by default: true.
- browser audio available: true.
- Enable and Preview clicked: true.
- procedural preview confirmed: true, 6 cues.
- human audible confirmation: false.

Final full QA:
- tests: PASS, 105 files / 310 tests.
- typecheck: PASS.
- build: PASS.
- HTTP smoke: 200.
- post-benchmark schema test after refreshing `PERFORMANCE_BENCHMARK_v1_4.json`: PASS, 1 file / 1 test.
- focused v1.4 regression tests: PASS, 3 files / 3 tests.
- secret scan: count-only; no values printed.
- boundary scan: no `unknown_code_executed=true`, no `publication_allowed=true`, no Wabi true assignments, no cloud/push/deploy/commit/MCP true markers, no v1.4 public asset copies.

Run dir:
- `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\RUN_DUAT_OSIT_OBSERVACIONISMO_FULL_v1_4_20260520\`

Residual QA gate:
- ActionGate remains `REVIEW` because real headed FPS and audible audio were not verified in this automated pass.
