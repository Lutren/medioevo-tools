# ACTIONGATE OPERATOR-APPROVED EXECUTION SANDBOX

Fecha: 2026-05-12

## Proposito

Run 8 agrega una capa de ejecucion limitada para ActionGate, pero solo dentro de un sandbox local aislado.

La capa no habilita escritura en produccion. No ejecuta deploy, push, DNS, publicacion, delete, move, rename ni comandos shell arbitrarios.

## Token manual local

Token fijo:

`APPROVE_RUN8_LOCAL_SANDBOX_ONLY`

Este token:

- No es secreto.
- No es credencial.
- No autoriza produccion.
- Solo habilita ejecucion en sandbox local.
- Requiere propuesta sellada e integra.
- Requiere decision `approved_simulated`.

## Dry-run executor

`dryRunExecutor.mjs` genera una vista previa de ejecucion en sandbox:

- `wouldExecuteInSandbox`
- `wouldExecuteInProduction: false`
- plan inerte de ActionGate
- policy result
- stop conditions

No modifica archivos.

## Sandbox executor

`sandboxExecutor.mjs` ejecuta solo propuestas permitidas dentro de:

`MEDIOEVO_LIVE_TREE/02_RUNTIME/actiongate/sandbox/`

Subrutas:

- `runs/`
- `messagebus/`
- `files/`
- `receipts/`
- `rollback/`

Tipos permitidos:

- `append_message`
- `create_task`
- `update_handoff`

Tipos bloqueados:

- `publish_release`
- `delete_or_move`
- operaciones destructivas.
- escritura externa.
- shell arbitrario.

## Sandbox filesystem

`sandboxFilesystem.mjs` crea y valida las rutas del sandbox.

Toda ruta de escritura pasa por `assertSandboxPath`. Si una ruta intenta escapar del sandbox, se bloquea.

## Sandbox MessageBus copy

`sandboxMessageBus.mjs` copia el log principal a una ruta sandbox antes de operar.

La ejecucion de `append_message` usa la copia sandbox, no:

`MEDIOEVO_LIVE_TREE/02_RUNTIME/messagebus/logs/messagebus-main.jsonl`

El MessageBus principal conserva:

- SHA256: `D9224126A73CC3F3322ADEF3BB028D51341D59BBD7F5141C2A9730EA9D9F9F5F`
- Size: `2883`

## Execution receipt

`executionReceipt.mjs` genera recibos verificables por ejecucion sandbox.

Campos principales:

- `receiptId`
- `runId`
- `proposalId`
- `decisionId`
- `sandboxOnly: true`
- `productionMutation: false`
- `actionExecutedInProduction: false`
- `sandboxMessageBusCopy`
- `sandboxFiles`
- `rollback`
- `receiptHash`

## Rollback sandbox

`sandboxRollback.mjs` crea snapshots dentro del sandbox antes de ejecutar.

El rollback solo restaura copias sandbox. Si detecta la ruta del MessageBus principal como objetivo de rollback, se niega a operar.

## Execution policy

`executionPolicy.mjs` bloquea cualquier ejecucion que no cumpla:

- sello ActionGate valido.
- policy ActionGate no bloqueada.
- `riskLevel: low`.
- decision `approved_simulated`.
- token manual local exacto.
- tipo permitido por sandbox.

Resultado:

- `ALLOW_SANDBOX_EXECUTION`
- `BLOCK_SANDBOX_EXECUTION`

## Health

`executionHealth.mjs` reporta:

- estado READY/BLOCKED.
- modo operator-approved local sandbox.
- escritura en produccion disabled.
- token manual local.
- subrutas del sandbox.
- tipos permitidos y bloqueados.
- conteos de runs, copies, files, receipts y rollback.

## Integracion UI

`/telecom` muestra:

- ActionGate Execution Sandbox: READY.
- Modo: operator-approved local sandbox.
- Approval token: local fixed phrase, not secret.
- Production writes: disabled.
- Sandbox MessageBus: copy only.
- Receipts y rollback.
- Next: receipt review before real executor.

React no importa modulos Node-only.

## Que no hace todavia

- No ejecuta acciones reales en produccion.
- No modifica el MessageBus principal.
- No publica.
- No despliega.
- No hace push.
- No toca DNS.
- No borra, mueve ni renombra fuentes originales.
- No crea credenciales.
- No usa tokens reales.

## Como prepara Run 9

Run 9 debe revisar receipts, endurecer el sandbox y crear un gate de revision manual antes de considerar cualquier executor real futuro.

La ejecucion real, si alguna vez existe, debe quedar separada de Run 8 y seguir bloqueando deploy, delete, move, DNS y publicacion automatica.
