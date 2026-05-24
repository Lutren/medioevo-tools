# CODEX CHANGELOG v0.7

Fingerprint: `DUAT-VISUAL-QA-ASSET-ALLOWLIST-v0.7`
Date: 2026-05-19

## Added

- Visual benchmark runner: `src/bench/visualBenchmark.ts`, `src/bench/runVisualBenchmark.ts`.
- Reviewed asset manifest loading and sprite resolution.
- v0.7 tests for asset allowlist, asset atlas, benchmark, pixel-field QA, RPG visual export and Wabi workpacks.
- Screenshot evidence under `docs/screenshots/v0_7/`.
- v0.7 reports for visual QA, benchmark, allowlist, copy, pixel-field QA and final handoff.

## Changed

- `MainCanvas` redraws after canvas resize; this fixed blank captures in Beautiful mode.
- `App` loads reviewed asset manifest and passes sprite resolver into the renderer.
- `canvasRenderer`, `buildingRenderer`, and `agentRenderer` can draw reviewed sprites when available and fall back procedurally.
- RPG export v2 now includes reviewed asset refs, visual style profile, tile/agent atlas refs, light profile and screenshot refs.
- Wabi workpacks include v0.7 design-only drafts and keep `execution_allowed=false`, `sandbox_execution_allowed=false`, `real_apply_allowed=false`.

## Preserved

- No deploy, push, commit, cloud, MCP execution, external API, or public release.
- No original asset source was modified.
- Reviewed assets remain internal and `publication_allowed=false`.
