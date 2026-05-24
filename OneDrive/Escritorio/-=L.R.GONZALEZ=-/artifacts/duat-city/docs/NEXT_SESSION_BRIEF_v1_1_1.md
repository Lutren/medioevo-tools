# NEXT SESSION BRIEF v1.1.1

Fingerprint: DUAT-v1.1.1-FOCUSED-FPS-CLOSURE

## Estado

DUAT v1.1.1 closes the focused FPS benchmark gap with a local Edge/CDP
focused run, in-app fallback runner, light budgets, dirty-region helpers and
playable QA sequence.

## Evidence

- Tests: 58 files / 232 tests PASS.
- Typecheck: PASS.
- Build: PASS.
- HTTP smoke: 200.
- Focused benchmark: `docs/PERFORMANCE_BENCHMARK_v1_1_1.json`.
- Screenshots: `docs/screenshots/v1_1_1/`.

## Residual Risk

HIGH and BEAUTIFUL still do not sustain 30 FPS in the CDP run. The next pass
should cache/offscreen postprocess passes and reduce full-canvas work.

## NextAction

Optimize canvas postprocess with offscreen cached layers, then rerun the
in-app focused 30s benchmark manually with the browser actively focused.

## Segunda perdida

Los datos persisten. El operador no. Recalibrar desde este brief, no desde
memoria implicita.
