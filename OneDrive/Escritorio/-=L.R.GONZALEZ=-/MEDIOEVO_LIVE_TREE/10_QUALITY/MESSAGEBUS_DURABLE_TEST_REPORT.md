# MESSAGEBUS DURABLE TEST REPORT

Fecha: 2026-05-12

Estado final: PASSED_LOCAL.

## Comandos ejecutados

| Comando | Resultado |
|---|---|
| `npm test -- src/messagebus` | PASSED: 6 test files, 24 tests |
| `npx tsc -b --pretty false` | PASSED |
| `npm run build` | PASSED: 1600 modules transformed |
| `npm test` | PASSED: 7 test files, 35 tests |
| `npm run messagebus:append-sample` | PASSED: appended `msg-run4-jsonl-20260512100904` |
| `npm run messagebus:verify` | PASSED: `ok=true`, `totalEntries=1` |
| `npm run messagebus:replay` | PASSED: `totalEntries=1`, `#codex_runs=1` |
| `npm run messagebus:stats` | PASSED: `fileSizeBytes=2883` |
| `npm run messagebus:export-md` | PASSED: export generado |
| `python -m compileall -q .` | PASSED |
| `pytest -q` | NOT_APPLICABLE: no Python tests detected |
| `Invoke-WebRequest http://127.0.0.1:5174/telecom` | PASSED_LOCAL |
| `Invoke-WebRequest http://127.0.0.1:5174/src/ui/TelecomCore.tsx` | PASSED_LOCAL: contiene `Durable Log Status` y no imports Node-only |

## Tests nuevos

Archivo:

`C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\durableJsonl.test.mjs`

Cobertura:

- JSONL append crea archivo si no existe.
- Append agrega exactamente una linea valida.
- Replay reconstruye estado desde cero.
- Verificador acepta log valido.
- Verificador rechaza hash-chain rota.
- Verificador detecta duplicate id.
- Verificador detecta schema invalido.
- Export Markdown desde replay contiene `ESTADO` y `HANDOFF`.
- Export JSONL conserva orden.
- Build React no importa modulos Node-only.

## Artefactos de prueba

- `src/messagebus/fixtures/valid-log.jsonl`
- `src/messagebus/fixtures/invalid-hash-log.jsonl`
- `src/messagebus/fixtures/invalid-schema-log.jsonl`
- `src/messagebus/fixtures/duplicate-id-log.jsonl`

## Estado del log durable

- Ruta: `MEDIOEVO_LIVE_TREE/02_RUNTIME/messagebus/logs/messagebus-main.jsonl`
- Entradas: 1
- Last hash: `sha256-a3eb743da2b85b1096440c4b406b06f2e9b0141c69d103779a97dcc93c160791`
- Replay: PASSED.
- Hash-chain: PASSED.

## Errores

Ninguno en cierre Run 4.

## Limitaciones

- MCP real queda para Run 5.
- JSONL contiene entrada sample inicial; no se migro todo `localStorage`.
- No se habilitan write tools remotas.
