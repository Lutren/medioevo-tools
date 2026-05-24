# CODEX FINAL HANDOFF v0.7

Fingerprint: `DUAT-VISUAL-QA-ASSET-ALLOWLIST-v0.7`
Date: 2026-05-19

## Brief

DUAT v0.7 focused on validation instead of feature expansion. The app now has browser screenshot evidence, a repeatable visual benchmark artifact, a minimal reviewed asset allowlist/copy lane, atlas fallback integration, RPG visual export refs, and Wabi v0.7 design-only workpack drafts.

## Evidence

- Screenshots: `docs/screenshots/v0_7/`
- Benchmark JSON: `docs/VISUAL_BENCHMARK_v0_7.json`
- Allowlist: `public/asset-manifest/asset_allowlist_v0_7.json`
- Reviewed assets manifest: `public/reviewed-assets/v0_7/REVIEWED_ASSETS_MANIFEST.json`
- Tests: v0.7 added 6 test files; suite result after additions: 28 files / 137 tests in focused run.

## State Estimate

- R_est: 0.18
- Phi_eff_est: 0.82
- Regime: FUNCIONAL
- ActionGate: APPROVE_LOCAL for local review artifacts; REVIEW_REQUIRED for any public asset use.

## Next Action

Run a browser FPS sampler from inside the app and tune default camera framing so the first viewport reads like a city, not a sparse technical map.
