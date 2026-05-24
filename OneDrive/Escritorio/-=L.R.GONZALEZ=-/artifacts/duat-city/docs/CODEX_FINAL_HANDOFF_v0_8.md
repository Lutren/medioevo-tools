# CODEX FINAL HANDOFF v0.8

Fingerprint: `DUAT-v0.8-FPS-CAMERA-FRAMING`
Date: 2026-05-19

## Brief

DUAT v0.8 closes the next visual QA loop: it adds a real in-app FPS sampler, an OSIT performance panel, camera presets, Beautiful capture mode hardening, and screenshot evidence for the improved framing. The work stays local-only and does not expand features or copy new assets.

## Evidence

- Screenshots: `docs/screenshots/v0_8/`
- Screenshot review: `docs/SCREENSHOT_REVIEW_v0_8.md`
- Visual QA report: `docs/VISUAL_QA_REPORT_v0_8.md`
- Performance sampler docs: `docs/PERFORMANCE_SAMPLER_v0_8.md`
- Camera docs: `docs/CAMERA_FRAMING_v0_8.md`
- Benchmark artifact: `docs/PERFORMANCE_BENCHMARK_v0_8.json`
- QA logs: `../../qa_artifacts/release_validation/RUN_DUAT_FPS_CAMERA_FRAMING_v0_8_20260519/`

## Final QA

- `corepack pnpm --filter @workspace/duat-city run test`: PASS, 33 files / 150 tests.
- `corepack pnpm --filter @workspace/duat-city run typecheck`: PASS.
- `corepack pnpm --filter @workspace/duat-city run build`: PASS.
- HTTP smoke `http://127.0.0.1:18519/duat-city/`: 200.
- Strict secret-value scan: PASS, values not printed.
- Asset boundary scan: PASS, no v0.8 reviewed-assets folder, v0.7 reviewed asset count remains 8 and `publication_allowed=false`.

## State Estimate

- R_est: 0.16
- Phi_eff_est: 0.84
- Regime: FUNCIONAL
- ActionGate: APPROVE_LOCAL for v0.8 local code/docs/tests; REVIEW_REQUIRED for any additional asset migration or public promotion.

## Disabled State

- Wabi MCP execution remains disabled.
- `execution_allowed=false`
- `sandbox_execution_allowed=false`
- `real_apply_allowed=false`
- No deploy, push, commit, cloud or external API was used.

## Next Action

v0.9 should approve a second asset allowlist focused on building/tile sprites, then replace the weakest procedural building silhouettes while keeping the fallback renderer.
