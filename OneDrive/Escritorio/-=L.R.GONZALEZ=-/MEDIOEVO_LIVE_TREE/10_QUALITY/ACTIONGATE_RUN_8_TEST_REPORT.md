# ACTIONGATE RUN 8 TEST REPORT

Fecha: 2026-05-12

Estado general: PASS

## Comandos ejecutados

| Comando | Resultado | Evidencia |
| --- | --- | --- |
| `npm test -- src/messagebus/actionGateSandbox.test.mjs` | PASS | 1 file, 16 tests |
| `npm test -- src/messagebus` | PASS | 10 files, 87 tests |
| `npm test` | PASS | 11 files, 98 tests |
| `npx tsc -b --pretty false` | PASS | sin errores |
| `npm run build` | PASS | Vite build generado |
| `npm run messagebus:mcp:smoke` | PASS | read-only true, writeToolsEnabled false |
| `npm run agents:bridge:smoke` | PASS | bridge READY, 6 agents |
| `npm run actiongate:smoke` | PASS | proposal-only, ledger separado |
| `npm run actiongate:sandbox:smoke` | PASS | sandbox executor, receipts, rollback |
| `npm audit --omit=dev` | PASS | 0 vulnerabilities |
| `npm audit --json` | NON_BLOCKING_DEV | 5 moderate dev vulnerabilities |
| `python -m compileall -q .` | PASS | sin errores |
| `pytest -q` | NOT_APPLICABLE | no Python tests ran |

## Tests unitarios Run 8

`src/messagebus/actionGateSandbox.test.mjs` valida:

- token manual fijo.
- token no secreto.
- token faltante bloqueado.
- token incorrecto bloqueado.
- sello alterado bloqueado.
- dry-run sin produccion.
- append solo sobre copia sandbox del MessageBus.
- create_task solo en archivos sandbox.
- update_handoff solo en markdown sandbox.
- rollback restaura copia sandbox.
- publish_release bloqueado.
- delete_or_move bloqueado.
- modify_dns bloqueado.
- path escape bloqueado.
- execution health READY.
- smoke sandbox aislado PASS.
- UI React sin imports Node-only.

## Smoke sandbox

`npm run actiongate:sandbox:smoke`:

- status: PASS.
- token: `APPROVE_RUN8_LOCAL_SANDBOX_ONLY`.
- token secreto: no.
- dry-run: `wouldExecuteInSandbox: true`.
- produccion: `wouldExecuteInProduction: false`.
- ejecuciones sandbox:
  - `append_message`
  - `create_task`
  - `update_handoff`
- bloqueados:
  - token faltante.
  - token incorrecto.
  - `publish_release`.
  - `delete_or_move`.
- rollback: `restored_sandbox_messagebus_copy`.
- main MessageBus mutation: `NOT_DETECTED`.

## MCP

`npm run messagebus:mcp:smoke`:

- readOnly: true.
- writeToolsEnabled: false.
- hashChainStatus: OK.
- totalEntries: 1.
- fileSizeBytes: 2883.

## Agent Bridge

`npm run agents:bridge:smoke`:

- bridgeStatus: READY.
- remoteNetworkEnabled: false.
- writeToolsEnabled: false.
- agentCount: 6.
- deploy intent bloqueado.
- security publication bloqueada.
- MessageBus reader opera read-only.

## ActionGate proposal smoke

`npm run actiongate:smoke`:

- status: PASS.
- proposals selladas.
- approval simulator no ejecuto acciones.
- execution plan inerte.
- ledger separado verificado.
- main MessageBus mutation: `NOT_DETECTED`.

## /telecom

Checks locales:

- `http://127.0.0.1:5173/telecom`: HTTP 200.
- `http://127.0.0.1:5174/telecom`: HTTP 200.

Estado UI:

- ActionGate Layer: READY.
- ActionGate Execution Sandbox: READY.
- Mode: operator-approved local sandbox.
- Production writes: disabled.
- Sandbox MessageBus: copy only.
- Receipts: sandbox receipts with rollback.

## Audit

Runtime/prod:

- `npm audit --omit=dev`: PASS.
- Prod vulnerabilities: 0.

Dev:

- `npm audit --json`: 5 moderate.
- Paquetes: `vite`, `vitest`, `vite-node`, `@vitest/mocker`, `esbuild`.
- Estado: no bloquea runtime/prod.

## MessageBus principal

Ruta:

`MEDIOEVO_LIVE_TREE/02_RUNTIME/messagebus/logs/messagebus-main.jsonl`

Antes y despues de Run 8:

- SHA256: `D9224126A73CC3F3322ADEF3BB028D51341D59BBD7F5141C2A9730EA9D9F9F5F`
- Size: `2883`

Confirmacion: no hubo mutacion del MessageBus principal.

## Runtime variable

El sandbox genero archivos runtime bajo:

`MEDIOEVO_LIVE_TREE/02_RUNTIME/actiongate/sandbox/`

No deben commitearse como artefacto estable.

## Resultado

Run 8 PASS.

La capa permite ejecucion limitada solo en sandbox local con token manual fijo y receipts, manteniendo bloqueada toda accion real de produccion.
