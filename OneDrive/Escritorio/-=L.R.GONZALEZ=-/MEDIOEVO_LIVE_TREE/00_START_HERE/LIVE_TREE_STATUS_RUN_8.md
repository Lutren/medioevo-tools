# LIVE TREE STATUS RUN 8

Fecha: 2026-05-12

Estado: PASS

## Resumen

Run 8 implemento el sandbox de ejecucion aprobado por operador para ActionGate.

El modo sigue cerrado para produccion:

- Escritura en produccion: disabled.
- MessageBus principal: no mutado.
- Deploy, push, DNS, publicacion, delete, move, rename: blocked.
- Token manual local: `APPROVE_RUN8_LOCAL_SANDBOX_ONLY`.
- Token secreto: no.
- Alcance del token: solo sandbox local.

## Leido

- `MEDIOEVO_LIVE_TREE/00_START_HERE/LIVE_TREE_STATUS_RUN_7.md`
- `MEDIOEVO_LIVE_TREE/03_SYSTEMS/ACTIONGATE_WRITE_PROPOSAL_LAYER.md`
- `MEDIOEVO_LIVE_TREE/10_QUALITY/ACTIONGATE_RUN_7_TEST_REPORT.md`
- `MEDIOEVO_LIVE_TREE/09_OPERACION/HANDOFF_RUN_7.md`
- `MEDIOEVO_LIVE_TREE/09_OPERACION/TASKS_RUN_8.md`
- `New project 3/scripts/actiongate/*`
- `New project 3/scripts/actiongate/lib/*`
- `New project 3/scripts/agents/`
- `New project 3/scripts/messagebus/lib/*`
- `New project 3/src/messagebus/actionGate.test.mjs`
- `New project 3/src/ui/TelecomCore.tsx`
- `New project 3/package.json`

## Creado

- `New project 3/scripts/actiongate/execution-sandbox-smoke.mjs`
- `New project 3/scripts/actiongate/lib/manualApprovalToken.mjs`
- `New project 3/scripts/actiongate/lib/dryRunExecutor.mjs`
- `New project 3/scripts/actiongate/lib/sandboxExecutor.mjs`
- `New project 3/scripts/actiongate/lib/sandboxFilesystem.mjs`
- `New project 3/scripts/actiongate/lib/sandboxMessageBus.mjs`
- `New project 3/scripts/actiongate/lib/executionReceipt.mjs`
- `New project 3/scripts/actiongate/lib/sandboxRollback.mjs`
- `New project 3/scripts/actiongate/lib/executionPolicy.mjs`
- `New project 3/scripts/actiongate/lib/executionHealth.mjs`
- `New project 3/src/messagebus/actionGateSandbox.test.mjs`
- `MEDIOEVO_LIVE_TREE/02_RUNTIME/actiongate/sandbox/`
- `MEDIOEVO_LIVE_TREE/02_RUNTIME/actiongate/sandbox/runs/`
- `MEDIOEVO_LIVE_TREE/02_RUNTIME/actiongate/sandbox/messagebus/`
- `MEDIOEVO_LIVE_TREE/02_RUNTIME/actiongate/sandbox/files/`
- `MEDIOEVO_LIVE_TREE/02_RUNTIME/actiongate/sandbox/receipts/`
- `MEDIOEVO_LIVE_TREE/02_RUNTIME/actiongate/sandbox/rollback/`

## Modificado

- `New project 3/package.json`
- `New project 3/src/ui/TelecomCore.tsx`
- `New project 3/src/styles.css`

## Capacidades

- Dry-run executor.
- Sandbox executor.
- Manual approval token local fijo.
- Sandbox filesystem aislado con path guard.
- Sandbox MessageBus copy.
- Sandbox proposal replay.
- Execution receipt.
- Rollback dentro del sandbox.
- Execution policy para bloquear produccion y tipos peligrosos.
- Execution health para UI y smoke.

## Propuestas ejecutables en sandbox

- `append_message`
- `create_task`
- `update_handoff`

## Propuestas bloqueadas en sandbox

- `publish_release`
- `modify_file` fuera de bajo riesgo aprobado.
- `delete_or_move`
- deploy, push, DNS, publicacion, delete, move, rename.
- shell arbitrario.
- creacion de credenciales.
- escritura externa.

## QA

- `npm test -- src/messagebus/actionGateSandbox.test.mjs`: PASS, 16 tests.
- `npm test -- src/messagebus`: PASS, 87 tests.
- `npm test`: PASS, 98 tests.
- `npx tsc -b --pretty false`: PASS.
- `npm run build`: PASS.
- `npm run messagebus:mcp:smoke`: PASS.
- `npm run agents:bridge:smoke`: PASS.
- `npm run actiongate:smoke`: PASS.
- `npm run actiongate:sandbox:smoke`: PASS.
- `npm audit --omit=dev`: PASS, 0 prod vulnerabilities.
- `python -m compileall -q .`: PASS.
- `pytest -q`: NOT_APPLICABLE, no Python tests found.

## MessageBus principal

- SHA256 antes y despues: `D9224126A73CC3F3322ADEF3BB028D51341D59BBD7F5141C2A9730EA9D9F9F5F`
- Size antes y despues: `2883`
- Mutacion detectada: no.

## /telecom

- `/telecom`: HTTP 200.
- UI muestra ActionGate Execution Sandbox.
- No importa `fs`, `path` ni `crypto` en React.

## Bloqueos

No hay bloqueo activo.

Se registro un fallo inicial de test de smoke aislado por una expectativa demasiado estricta sobre conteo de entradas sandbox. Fue corregido y revalidado.

## Proximo paso

Run 9: receipt review gate y sandbox hardening antes de cualquier executor real.
