# TEST REPORT ENGINE EXTENSIONS 2026-05-22

## Scope

`artifacts/duat-city` Fase 1/Fase 2/Fase 3 continuation:

- Canon declaration and stale-runtime marker.
- Canonical sigmoidal EML.
- Agent lineage/origin story, theater profiles, academy skill packs, psychologist repair cycle.
- City climate/geography context.
- Physics determinism test.
- Private Godot RPG validation through headless scenes.
- Vite local smoke after frontend build-surface change.
- Browser visual QA for the `theater` toolbar/building surface on desktop and mobile.

## Results

| Command | Result |
|---|---|
| `npm test` before feature work | PASS, 106 test files / 314 tests |
| `npm run typecheck` before feature work | PASS |
| `npm run build` before feature work | PASS, Vite 5.4.21, 249 modules, built in 19.90s |
| `npx vitest run src/tests/eml.test.ts` | PASS, 1 file / 8 tests |
| `npm run typecheck` after EML | PASS |
| `npx vitest run src/tests/agentLineageGenerator.test.ts src/tests/theaterAgentProfile.test.ts src/tests/academySkills.test.ts src/tests/psychologistRepair.test.ts` | PASS, 4 files / 10 tests |
| `npm run typecheck` final | PASS |
| `npx vitest run src/tests/agentLineageGenerator.test.ts src/tests/theaterAgentProfile.test.ts src/tests/academySkills.test.ts src/tests/psychologistRepair.test.ts src/tests/cityContext.test.ts src/tests/physicsDeterminism.test.ts src/tests/city.test.ts src/tests/handoff.test.ts src/tests/eml.test.ts` | PASS, 9 files / 40 tests |
| `npm test` final | PASS, 112 test files / 329 tests |
| `npm run build` final | PASS, Vite 5.4.21, 254 modules, built in 5.21s |
| `E:\Medioevo_RPG\tools\godot\Godot_v4.3-stable_win64_console.exe --headless --path E:\Medioevo_RPG res://tools/campaign/Validate*.tscn` loop | PASS, 24 scenes / 24 exit code 0 |
| `Invoke-WebRequest http://127.0.0.1:5175/` | PASS, HTTP 200, content length 2142 |
| `npm run typecheck` after theater visual QA fixes | PASS |
| `node tools\run-theater-visual-qa-2026-05-22.mjs` | PASS, Edge/CDP headless, all 11 checks true |
| `npx vitest run --reporter=dot` after visual QA fixes | PASS, 112 test files / 329 tests, 147.54s |
| `npm run build` after visual QA fixes | PASS, Vite 5.4.21, 254 modules, built in 1m 54s |
| `Invoke-WebRequest http://127.0.0.1:5175/` after visual QA fixes | PASS, HTTP 200, content length 2158 |

## Browser Visual QA Notes

The visual QA initially found two real frontend regressions:

- Desktop: the Build Tool was too low in the left rail because `GameModeDirectorPanel` rendered before it, leaving the new `THR Theater` button below the first viewport.
- Mobile: `.canvas-area` collapsed to width `0` because fixed side panel widths exceeded the 390px viewport.

Fixes:

- `src/components/Toolbar.tsx` now renders the City Build Tool above the game-mode director.
- `src/styles.css` adds responsive layout rules so the panels stack and the canvas remains visible on compact screens.
- `tools/run-theater-visual-qa-2026-05-22.mjs` runs deterministic local visual QA through Edge/CDP without adding dependencies.

Evidence:

- `docs/screenshots/engine-extensions-2026-05-22/THEATER_VISUAL_QA_REPORT.json`
- `docs/screenshots/engine-extensions-2026-05-22/theater-desktop-initial.png`
- `docs/screenshots/engine-extensions-2026-05-22/theater-tool-selected.png`
- `docs/screenshots/engine-extensions-2026-05-22/theater-after-placement.png`
- `docs/screenshots/engine-extensions-2026-05-22/theater-mobile.png`

## Godot Notes

Godot output included `WORLDPULSE_BRIDGE_VALIDATION_OK`, `TECHNOLOGY_INTEGRATION_VALIDATION_OK`, `FULL_GAME_COMPLETION_LEDGER_VALIDATION_OK`, and expected `STORY_BIBLE_COMPLETION_BLOCKED_OK TODO=245` with exit code 0.

No publish, deploy, push, release package, or public distribution was executed.
