# SCREENSHOT REVIEW v0.8

Fingerprint: `DUAT-v0.8-FPS-CAMERA-FRAMING-VISUAL-POLISH`
Date: 2026-05-19

## Source Reviewed

- `docs/screenshots/v0_7/city-operational.png`
- `docs/screenshots/v0_7/agent-operational.png`
- `docs/screenshots/v0_7/rpg-operational.png`
- `docs/screenshots/v0_7/osit-operational.png`
- `docs/screenshots/v0_7/wabi-panel.png`
- `docs/screenshots/v0_7/osit-debug-pixel-field.png`
- `docs/screenshots/v0_7/city-debug-fibmob.png`
- `docs/screenshots/v0_7/city-beautiful.png`
- `docs/screenshots/v0_7/city-beautiful-night.png`
- `docs/VISUAL_QA_REPORT_v0_7.md`
- `docs/VISUAL_BENCHMARK_REPORT_v0_7.md`
- `docs/CODEX_FINAL_HANDOFF_v0_7.md`

## Findings by Screenshot

| Screenshot | Mode | Readability | City | Agent Life | RPG | Beautiful | Debug Noise | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `city-operational.png` | CITY / Operational | 3 | 3 | 2 | 1 | n/a | 2 | City exists but first viewport leaves too much unused space; right/left panels make the city feel secondary. |
| `agent-operational.png` | AGENT / Operational | 3 | 3 | 2 | 1 | n/a | 2 | Agent list is clear, but the canvas still reads as a technical map more than a lived routine view. |
| `rpg-operational.png` | RPG / Operational | 3 | 2 | 1 | 2 | n/a | 2 | Quest panel exists; map lacks strong landmark framing for RPG evaluation. |
| `osit-operational.png` | OSIT / Operational | 4 | 2 | 1 | 1 | n/a | 3 | Metrics are useful; operational overlays are acceptable but visually dense. |
| `wabi-panel.png` | OSIT / Wabi | 4 | 2 | 1 | 1 | n/a | 3 | Wabi disabled state is legible. Visual game quality is not the focus of this screenshot. |
| `osit-debug-pixel-field.png` | OSIT / Debug | 3 | 2 | 1 | 1 | n/a | 5 | Debug overlays dominate the field; good for QA, bad for presentation. |
| `city-debug-fibmob.png` | CITY / Debug | 3 | 2 | 1 | 1 | n/a | 5 | FibMob overlay is useful but too noisy outside Debug. |
| `city-beautiful.png` | CITY / Beautiful | 2 | 2 | 1 | 1 | 2 | 2 | Beautiful still showed left tool rail in v0.7 and did not feel like a capture mode. |
| `city-beautiful-night.png` | CITY / Beautiful Night | 2 | 2 | 1 | 1 | 2 | 2 | Night/lights direction is visible but camera scale and UI chrome reduce impact. |

## Camera and Scale Problems

- The active city cluster started too high/left and too small relative to the viewport.
- The tile field was visible, but the city composition did not guide the eye to buildings and agents.
- Building silhouettes were readable but still small. The next asset phase should prioritize buildings before decorative effects.

## Canvas / Resize Problems

- v0.7 had a confirmed empty-canvas capture risk after Beautiful resize.
- v0.8 first headless pass reproduced a similar early-capture condition for Beautiful/Debug before the render effect completed.
- Fix applied in v0.8: `MainCanvas` now uses `useLayoutEffect` for canvas sizing and rendering so the first visible paint is less likely to contain only background.

## Overlay Problems

- Debug overlays are valuable only as diagnostic evidence.
- Pixel field and FibMob should remain off in Beautiful and normal City/Agent/RPG modes.
- OSIT can show a reduced operational layer; Debug owns the full noise.

## Agent Legibility Problems

- Agent dots are readable, especially after v0.8 camera zoom.
- Life-sim state is still under-communicated: next visual work should add small eat/rest/work/social glyphs and interaction bubbles.

## Depth / Isometry Problems

- v0.7 looked partly like a flat technical board.
- v0.8 improves framing and soft shadows, but full 90s city-builder depth still needs reviewed sprites/building masses.

## Priority Ranking

1. Keep Beautiful as the screenshot/capture mode with minimal UI and no debug overlays.
2. Promote a second reviewed asset allowlist for building/tile sprites after owner license review.
3. Add life-sim activity glyphs without adding a new simulation system.
4. Keep FPS and render counters visible only in OSIT/Debug contexts.
5. Benchmark in a normal headed browser or DevTools if CPU precision is required.
