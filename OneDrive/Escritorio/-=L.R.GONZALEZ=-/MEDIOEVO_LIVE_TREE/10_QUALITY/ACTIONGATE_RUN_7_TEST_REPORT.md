# ACTIONGATE RUN 7 TEST REPORT

Fecha: 2026-05-12

Estado final: PASSED_LOCAL.

## Comandos ejecutados

| Comando | Resultado |
|---|---|
| `npm test -- src/messagebus` | PASSED: 9 test files, 71 tests |
| `npm test` | PASSED en reintento largo: 10 test files, 82 tests |
| `npx tsc -b --pretty false` | PASSED |
| `npm run build` | PASSED: 1600 modules transformed |
| `npm run messagebus:mcp:smoke` | PASSED: `ok=true`, resources 7, tools 8 |
| `npm run agents:bridge:smoke` | PASSED: `ok=true`, agents 6 |
| `npm run actiongate:smoke` | PASSED: `ok=true`, ledger 8 entries |
| `npm audit --omit=dev` | PASSED: 0 prod vulnerabilities |
| `npm audit --json` | REVIEW: 5 moderate dev vulnerabilities |
| `python -m compileall -q .` | PASSED en `MEDIOEVO_LIVE_TREE` |
| `pytest -q` | NOT_APPLICABLE: no Python tests detected under `MEDIOEVO_LIVE_TREE` |
| `Invoke-WebRequest http://127.0.0.1:5174/telecom` | PASSED_LOCAL: status 200 |

## Tests nuevos

Archivo:

`C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\actionGate.test.mjs`

Cobertura:

- Proposal schema acepta `append_message` valido.
- Proposal schema acepta `create_task` valido.
- Proposal schema acepta `update_handoff` valido.
- Proposal schema acepta `publish_release` valido.
- `delete_or_move` queda `BLOCKED`.
- `deploy_without_gate` queda `BLOCKED`.
- `print_secret` queda `BLOCKED`.
- `modify_dns` queda `BLOCKED`.
- Seal verifica propuesta intacta.
- Seal falla con propuesta alterada.
- Fixture tampered falla validacion.
- Approval simulator no ejecuta accion.
- Execution plan queda `executionStatus: not_executed`.
- ActionGate ledger separado crea hash-chain propio.
- ActionGate ledger no modifica MessageBus principal.
- Agent Bridge genera propuesta para accion de escritura.
- Agent Bridge bloquea accion destructiva.
- Smoke ActionGate pasa sobre ledger aislado.
- React no importa modulos Node-only ActionGate.
- `/telecom` contiene textos de estado ActionGate.

## Smoke ActionGate

Script:

`npm run actiongate:smoke`

Resultado:

- `ok=true`
- `status=PASS`
- MCP read-only: `true`
- MCP hash-chain: `OK`
- Bridge: `READY`
- Proposals creadas: 5
- Decisions simuladas: approve + reject
- Execution plan: `wouldExecute=false`, `executionStatus=not_executed`
- Ledger: `ok=true`, `totalEntries=8`
- Safety: `deployExecuted=false`, `pushExecuted=false`, `deleteMoveRenameExecuted=false`, `externalNetworkWriteExecuted=false`

## Estado MCP

- MCP read-only: READY.
- Write tools: disabled.
- Resources: 7.
- Tools: 8.
- Hash-chain MessageBus principal: OK.
- Main log entries: 1.
- Last hash: `sha256-a3eb743da2b85b1096440c4b406b06f2e9b0141c69d103779a97dcc93c160791`.

## Estado Agent Bridge

- Agent Bridge: READY.
- Agent count: 6.
- Agents:
  `codex-agent`, `publisher-agent`, `canon-auditor-agent`, `security-gate-agent`, `ui-agent`, `messagebus-reader-agent`.
- `append a new handoff message` genera propuesta `append_message`.
- `delete old zip files` genera propuesta `delete_or_move` bloqueada.
- Ejecucion: disabled.

## Estado /telecom

- Ruta local: `http://127.0.0.1:5174/telecom`.
- HTTP status: 200.
- Panel agregado: `ActionGate Write Proposal Layer`.
- Node-only imports en React: NOT_DETECTED.

## Audit

- `npm audit --omit=dev`: 0 prod vulnerabilities.
- `npm audit --json`: 5 moderate dev vulnerabilities en Vite/Vitest/esbuild chain.
- Decision: no bloquea Run 7 porque runtime/prod = 0 y el upgrade requerido es semver major de dev tooling.

## Confirmacion de no mutacion del MessageBus principal

Archivo:

`MEDIOEVO_LIVE_TREE/02_RUNTIME/messagebus/logs/messagebus-main.jsonl`

Antes y despues:

- SHA256: `D9224126A73CC3F3322ADEF3BB028D51341D59BBD7F5141C2A9730EA9D9F9F5F`
- Size: `2883`

Resultado: mutation NOT_DETECTED.

## Estado final

- Proposal schema: READY.
- Proposal builder: READY.
- Proposal validator: READY.
- Proposal seal: READY.
- Policy: READY.
- Approval simulator: READY.
- Execution plan generator: READY.
- ActionGate ledger separado: READY.
- delete/move/rename/deploy_without_gate: BLOCKED.
- MessageBus principal: unchanged.
- Build: PASS.
- Tests: PASS.
- Prod audit: PASS.
