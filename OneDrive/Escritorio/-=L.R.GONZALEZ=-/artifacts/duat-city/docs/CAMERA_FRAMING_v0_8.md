# CAMERA FRAMING v0.8

Fingerprint: `DUAT-v0.8-FPS-CAMERA-FRAMING-VISUAL-POLISH`
Date: 2026-05-19

## Scope

v0.8 adds reusable camera framing functions and mode presets so the first frame reads as a composed city view instead of a sparse technical grid.

## Files

- `src/render/cameraPresets.ts`
- `src/render/useCameraController.ts`
- `src/components/Toolbar.tsx`
- `src/components/MainCanvas.tsx`
- `src/App.tsx`

## Presets

- `CITY`: medium city framing with operational overlays available.
- `AGENT`: closer framing; follows selected agent or the most critical agent.
- `RPG`: wider landmark-oriented framing.
- `OSIT`: medium operational framing with metrics.
- `BEAUTIFUL`: wide 2.5D view, minimal UI, lights/shadows active, debug overlays disabled.
- `DEBUG`: technical view with overlays, chunk/physics/pixel/FibMob diagnostics enabled.

## Hardening

- All camera outputs are finite and zoom-clamped.
- Resize events update viewport state only when dimensions change.
- `MainCanvas` uses layout effects for resize/render to reduce first-paint empty canvas risk.
- Toolbar exposes `Reset Camera`, `Follow Critical`, and `Hide UI`.

## Evidence

- `docs/screenshots/v0_8/v0_8_city_operational.png`
- `docs/screenshots/v0_8/v0_8_city_beautiful.png`
- `docs/screenshots/v0_8/v0_8_agent_follow.png`
- Tests: `src/tests/camera.test.ts`, `src/tests/beautifulMode.test.ts`, `src/tests/visualPolishRegression.test.ts`
