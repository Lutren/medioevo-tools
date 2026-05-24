# LIGHT BEHAVIOR QA v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

## Claim Boundary

The engine remains a physically inspired light approximation for pixel-art
realism. It is not path tracing, not full light transport and not exact physics.

## Behavior Improved

- Fire material cells emit warm light into the light grid.
- Neon material cells emit colored cyan light.
- Placed light sources are projected into both the grid light engine and the
  canvas light map.
- Water and wet material cells raise reflectance and receive approximate
  reflection energy.
- Smoke/fog material cells raise scatter and atmosphere visibility.
- Rain raises wetness on placed material cells.
- Night scenes keep ambient legibility instead of fully blacking out the map.
- Warm interior vibe applies warmer palette, torch/window profile and embers.

## QA Evidence

`lightBehavior.test.ts` verifies:

- fire emits light;
- neon emits colored light;
- water reflection changes grid output;
- smoke scatters;
- wet material reflectance increases.

## Remaining Weakness

The grid intentionally over-approximates active light cells at higher quality.
Future optimization should dirty-update only affected light regions and report
active cells after thresholding by visible contribution.
