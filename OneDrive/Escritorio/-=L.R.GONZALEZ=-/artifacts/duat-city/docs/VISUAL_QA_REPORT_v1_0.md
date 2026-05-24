# Visual QA Report v1.0

Fingerprint: `DUAT-v1.0-PIXEL-REALISM-LIGHT-PHYSICS`

## Method

QA used the local dev server at `http://127.0.0.1:18519/duat-city/` and Microsoft Edge headless screenshot capture. No cloud browser, no external API and no new assets were used.

The Browser plugin was present, but the Node REPL tool required by that plugin was not exposed in this session. Edge headless was used as the local fallback.

## Screenshots

Stored in `docs/screenshots/v1_0/`:

- `beautiful_sunny_castle_lake.png`
- `beautiful_neon_rain_street.png`
- `warm_interior_tavern.png`
- `winter_tree_reflection.png`
- `jungle_waterfall_ruin.png`
- `desert_skyline.png`
- `archeopunk_city_night.png`
- `debug_light_grid.png`
- `debug_pixel_field.png`
- `vibe_coding_panel.png`
- `SCREENSHOT_CAPTURE_REPORT.json`

## Comparison to v0.9

v0.9 had simulation, OSIT UI, Agent Inspector, DEBUG overlay, RPG export, pixel field and Wabi design-only integration. v1.0 adds a dedicated pixel realism pipeline: color theory, light grid, material definitions, atmospheric passes, water reflection, bloom/dither, visual controls and deterministic VibeCoding scene authoring.

## Current Visual Reading

The result approaches the target direction: isometric/2.5D city, darker cinematic lighting, rain/neon atmosphere, debug light grid and pixel field overlays. It remains procedural and geometry-first because no new reviewed assets were imported.

## Weak Points

- Building silhouettes remain simple procedural geometry.
- No licensed sprite sheet or environment art was added.
- Light is approximate and screen-space/cell-space, not physically exact.
- Real headed FPS was not measured; only build/test/screenshot capture was verified.

## Performance Notes

The render path keeps logical internal grids at 80x45, 160x90 or 320x180 and does not simulate every screen pixel. Tests verify finite metrics and no NaN in the pixel realism runtime.
