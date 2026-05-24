# NEXT_SESSION_BRIEF MEDIOEVO/DUAT ENGINE EXTENSIONS

## Estado

R_close: 0.14
Phi_eff: 0.88
Regimen: FUNCIONAL
Autonomy level: 4

## Decisiones tomadas

- `artifacts/duat-city` queda como arbol canonico vivo del MEDIOEVO Engine / DUAT Agent City Engine / GlomoRender.
- `E:\Medioevo_RPG` queda como motor Godot privado complementario, no rival ni destino de copia cruda.
- EML activo en `src/core/eml.ts` usa forma sigmoidal acotada, coherente con `docs/THEORY.md`.
- `Agent.skills` se implementa como `string[]`; la persistencia JSON conserva el campo porque serializa `CityState` completo y ya tiene test.
- "Desvariando" queda definido como heuristica de juego testeable por R alto, gate BLOCK, necesidades en cero o bucles fallidos/bloqueados.
- La QA visual del teatro queda cubierta por script local Edge/CDP sin dependencias nuevas porque el browser automation directo no estaba disponible en esta sesion.

## Cambios realizados

- Canon/stale docs: `docs/ENGINE_CANON.md`, stale `LEER_STALE.md`, workbench FIBMOB doc y `00_CAMINO_UNICO_WORKBENCH.md`.
- Engine code: lineage/origin story, theater profile, academy skill packs, psychologist repair, city context, theater render/building support, EML sigmoidal.
- Tests: lineage, theater, academy/persistence, psychologist repair, city context, physics determinism, EML and hard-coded role count regressions.
- RPG bridge doc: `docs/MEDIOEVO_RPG_ENGINE_EXPORT_v2.md` now states current live schema is `medioevo-rpg/world/v3`.
- Frontend QA: Build Tool moved above the game-mode director; compact/mobile CSS now stacks panels and keeps the canvas visible.
- Visual evidence: `tools/run-theater-visual-qa-2026-05-22.mjs` plus screenshots/report under `docs/screenshots/engine-extensions-2026-05-22/`.

## Evidencia

- `npm test`: PASS, 112 files / 329 tests.
- `npm run typecheck`: PASS.
- `npm run build`: PASS.
- `npx vitest run --reporter=dot`: PASS, 112 files / 329 tests after visual QA fixes.
- `node tools\run-theater-visual-qa-2026-05-22.mjs`: PASS, theater button visible, selectable, placeable and non-overflowing on desktop/mobile.
- Godot headless private validation: 24 `Validate*.tscn` scenes passed.
- Vite dev smoke: `http://127.0.0.1:5175/` returns HTTP 200.

## Pendientes reales

- Optional deeper Godot adapter if the RPG is expected to directly import `medioevo-rpg/world/v3` JSON instead of consuming its current WorldPulse bridge.
- Story bible completion remains intentionally blocked in the private RPG validation with `TODO=245`; this is a content-completion marker, not a failed validator.

## Riesgos

- The workspace parent has many unrelated dirty/untracked files. Continue path-scoped.
- Dev server is running locally on `127.0.0.1:5175`; stop it when no longer needed.
- Visual QA uses installed Microsoft Edge through CDP; if Edge path changes, rerun or adjust the local QA script.

## Bloqueos

- Publication/deploy/push/distribution remains BLOCK.
- Raw ZIP or stale runtime import remains BLOCK.

## Proxima accion verificable

Decide only if needed whether Godot should consume `medioevo-rpg/world/v3` through a direct importer; otherwise keep the verified WorldPulse bridge as the live private path.

## Segunda perdida

Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.
