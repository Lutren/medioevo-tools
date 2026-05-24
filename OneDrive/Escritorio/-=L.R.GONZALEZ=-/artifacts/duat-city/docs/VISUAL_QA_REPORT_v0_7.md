# VISUAL QA REPORT v0.7

Fingerprint: `DUAT-VISUAL-QA-ASSET-ALLOWLIST-v0.7`
Date: 2026-05-19

## Method

- Local URL checked: `http://127.0.0.1:18519/duat-city/`
- Browser path: Microsoft Edge headless.
- Screenshot set written to `artifacts/duat-city/docs/screenshots/v0_7/`.
- A real defect was found during QA: `Beautiful` mode could capture an empty canvas after layout resize. Fixed in `src/components/MainCanvas.tsx` by forcing a redraw after canvas resize.

## Screenshot Evidence

- `screenshots/v0_7/city-operational.png`
- `screenshots/v0_7/agent-operational.png`
- `screenshots/v0_7/rpg-operational.png`
- `screenshots/v0_7/osit-operational.png`
- `screenshots/v0_7/wabi-panel.png`
- `screenshots/v0_7/osit-debug-pixel-field.png`
- `screenshots/v0_7/city-debug-fibmob.png`
- `screenshots/v0_7/city-beautiful.png`
- `screenshots/v0_7/city-beautiful-night.png`

## Findings

What works:
- The city is readable as a tile/isometric field with visible roads, buildings and agents.
- OSIT mode exposes R, Phi, combined metrics, pixel-field QA and handoff without leaving the local app.
- Wabi panel clearly reports `DESIGN ONLY`, `execution=false`, `real_apply=false`, and sandbox disabled.
- Debug overlays show pixel/cell field and FibMob state, and they can be separated from Beautiful/Operational modes.

What is weak:
- The city still reads more like a technical prototype than a 90s city-builder game.
- Agents are legible as colored units, but the life-sim layer is not visually rich yet: no clear routine animation, object interaction pose, or relationship bubble in the QA screenshots.
- Building silhouettes are functional but still too abstract; approved icon assets help as overlays, not as full replacement sprites.
- The map starts visually small in the upper-left region. A better camera preset or fit-to-city control should be next.
- Beautiful mode hides technical right/bottom panels, but the left tool rail remains visible. This is acceptable for v0.7 QA, but not a full presentation mode.

## Scores

- readability: 3/5
- city_feel: 3/5
- agent_life_feel: 2/5
- rpg_builder_feel: 2/5
- medioevo_identity: 3/5
- performance_feel: 4/5

## Prioritized Recommendations

1. Improve default camera framing so the city occupies the first viewport.
2. Replace selected procedural building masses with reviewed tile/building sprites after owner license review.
3. Add compact agent activity glyphs for eat/rest/work/social to make the Sims layer visible.
4. Split Beautiful into a true presentation mode that hides the left rail too.
5. Keep Debug overlays off by default; they are useful but visually invasive.
