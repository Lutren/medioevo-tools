# VIBECODING USABILITY v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

## Local Parser

The VibeCoding parser remains deterministic and local. It does not call AI,
cloud services, external APIs or MCP execution.

## New Usability Pass

The parser now handles:

- `hazlo de noche con lluvia y neon`;
- `mas calido, interior de taberna`;
- `mas niebla y reflejos en agua`;
- `menos debug, mas bonito`;
- `ciudad archeopunk al atardecer`;
- `ruina con luz cian y humo`;
- `mercado con fuego y lluvia`;
- `bosque nevado con reflejo`;
- `desierto con cielo limpio`.

## UI

`VibeCodingPanel` now shows a preview of the compiled config and an explanation
of parsed intent before apply. It also exposes Undo Vibe for the last applied
change.

## QA Evidence

`vibeParserUsability.test.ts` verifies night/rain/neon, warm tavern, fog/water
reflection, archeopunk sunset and undo snapshot behavior.
