# TEST_REPORT v1.0

## Baseline

- `corepack pnpm --filter @workspace/duat-city run test`: 42 files / 177 tests passed.
- `corepack pnpm --filter @workspace/duat-city run typecheck`: passed.
- `corepack pnpm --filter @workspace/duat-city run build`: passed.
- HTTP smoke `http://127.0.0.1:18519/duat-city/`: 200.

## Final

- `corepack pnpm --filter @workspace/duat-city run test`: 49 files / 202 tests passed.
- `corepack pnpm --filter @workspace/duat-city run typecheck`: passed.
- `corepack pnpm --filter @workspace/duat-city run build`: passed.
- HTTP smoke `http://127.0.0.1:18519/duat-city/`: 200.

## New Test Coverage

- Color conversions, Kelvin temperature, palettes and tone mapping.
- Deterministic ordered dithering and palette quantization.
- Logical light grid, opacity, colored light and finite reflection metrics.
- Material rules for fire, water, smoke, wet stone and full material definition coverage.
- Pixel renderer pass order, quality presets and finite runtime metrics.
- VibeCoding prompt parser and no-cloud/no-API behavior.
- RPG visual scene export and pixel physics profile.
- OSIT/handoff pixel realism integration.

## Evidence Path

`qa_artifacts/release_validation/RUN_DUAT_PIXEL_REALISM_ENGINE_v1_0_20260519`
