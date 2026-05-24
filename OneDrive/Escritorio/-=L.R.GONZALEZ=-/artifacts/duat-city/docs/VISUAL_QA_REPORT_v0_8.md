# VISUAL QA REPORT v0.8

Fingerprint: `DUAT-v0.8-FPS-CAMERA-FRAMING-VISUAL-POLISH`
Date: 2026-05-19

## Method

- Local URL: `http://127.0.0.1:18519/duat-city/`
- Capture tool: Microsoft Edge headless with explicit compositor/virtual-time wait for stable canvas capture.
- Screenshots: `docs/screenshots/v0_8/`
- v0.7 comparison source: `docs/screenshots/v0_7/`

## Screenshot Evidence

- `screenshots/v0_8/v0_8_city_operational.png`
- `screenshots/v0_8/v0_8_city_beautiful.png`
- `screenshots/v0_8/v0_8_agent_follow.png`
- `screenshots/v0_8/v0_8_rpg_builder.png`
- `screenshots/v0_8/v0_8_osit_performance.png`
- `screenshots/v0_8/v0_8_debug_overlays.png`

## Findings

What improved:

- The city cluster now starts centered and larger in the first viewport.
- Beautiful mode now hides the main technical panels and left tool rail.
- Debug overlays are visually isolated to Debug instead of leaking into Beautiful.
- Pixel/FibMob noise stays out of Beautiful.
- Performance metrics are visible in OSIT through the in-app FPS sampler panel.
- Agent follow framing is closer and makes agent labels more readable.

What still looks prototype-like:

- Buildings remain mostly procedural masses with reviewed icon overlays, not full sprite buildings.
- Agent life simulation is present in data but visually thin; routines need compact activity glyphs.
- The map still uses a dark technical palette; this is good for OSIT but not enough for a final SimCity/Sims tone.
- Edge headless virtual-time timing produced conservative FPS panel values; CPU-quality benchmarking remains owner-review work.

## Scores

- readability: 4/5
- city_feel: 3/5
- agent_life_feel: 2/5
- rpg_builder_feel: 3/5
- medioevo_identity: 3/5
- performance_feel: 4/5

## v0.7 vs v0.8

- Framing improved: yes. The city occupies the center instead of the upper-left.
- Beautiful mode improved: yes. It now behaves as a capture view with minimal UI.
- Legibility improved: yes for agents/camera; partial for buildings.
- Prototype vs game: improved but still prototype. The next visible jump requires reviewed building/tile sprites.

## Remaining Problems

1. Building visual identity is the main weak point.
2. Agent routine/life-sim information needs visual glyphs.
3. Performance panel should be interpreted cautiously in headless virtual-time captures.
4. A headed browser benchmark remains useful for CPU estimates.
