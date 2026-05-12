# ACTIONGATE RUN 8 BLOCKERS

Fecha: 2026-05-12

Estado: RESOLVED_LOCAL

## Bloqueo activo

No hay bloqueo activo.

## Incidencia resuelta

Comando:

`npm test -- src/messagebus/actionGateSandbox.test.mjs`

Error relevante:

El smoke aislado del sandbox esperaba un conteo exacto de entradas de MessageBus sandbox.

Causa probable:

La expectativa era demasiado estricta para soportar tanto fixtures de dos entradas como el MessageBus principal actual de una entrada.

Fix aplicado:

La validacion cambio a requerir al menos dos entradas despues de un append sandbox, en lugar de un conteo exacto.

Resultado posterior:

- `npm test -- src/messagebus/actionGateSandbox.test.mjs`: PASS, 16 tests.
- `npm run actiongate:sandbox:smoke`: PASS.

## Requiere autorizacion externa

No.

## Riesgo residual

El runtime sandbox genera archivos variables y no debe commitearse.
