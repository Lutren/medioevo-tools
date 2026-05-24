# NEXT_SESSION_BRIEF DUAT v0.8

## Estado

R_close: 0.16
Phi_eff: 0.84
Regimen: FUNCIONAL
Autonomy level: 4 local-only

## Decisiones tomadas

- v0.8 no copio assets nuevos.
- v0.8 no abrio sistemas grandes.
- Beautiful es el modo de captura visual con UI minima.
- Debug es el propietario de pixel/FibMob/chunk/physics overlays.
- Wabi sigue design-only, sin ejecucion real.

## Cambios realizados

- FPS sampler real in-app basado en `requestAnimationFrame`.
- PerformancePanel integrado en OSIT.
- Camera presets y controles Reset Camera / Follow Critical / Hide UI.
- `MainCanvas` usa layout effects para reducir capturas de primer frame vacio.
- Visual polish leve en agentes, edificios, sombras y overlays.
- Reportes v0.8 y screenshots generados.

## Evidencia

- Tests: 33 files / 150 tests passed.
- Typecheck: PASS.
- Build: PASS.
- HTTP smoke: 200.
- Screenshots: `docs/screenshots/v0_8/`.
- QA logs: `qa_artifacts/release_validation/RUN_DUAT_FPS_CAMERA_FRAMING_v0_8_20260519/`.

## Pendientes reales

- Aprobar segunda allowlist de assets para v0.9.
- Sustituir primero edificios/tiles debiles, no efectos decorativos.
- Agregar glyphs de actividad eat/rest/work/social.
- Benchmark CPU en navegador headed si se necesita medicion de rendimiento real de maquina.

## Riesgos

- Licencias/provenance de assets externos siguen REVIEW.
- Headless virtual-time puede distorsionar FPS; usarlo como evidencia UI, no profiler.
- Aun se siente prototipo sin sprites de edificios/agentes revisados.

## Bloqueos

- Publicacion/promocion de assets v0.7 sigue bloqueada hasta review.
- Wabi execution sigue bloqueado por diseno.

## Proxima accion verificable

Aprobar 5-10 assets de edificios/tiles/agentes para v0.9 y reemplazar solo esas siluetas con fallback procedural preservado.

## Segunda perdida

Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.
