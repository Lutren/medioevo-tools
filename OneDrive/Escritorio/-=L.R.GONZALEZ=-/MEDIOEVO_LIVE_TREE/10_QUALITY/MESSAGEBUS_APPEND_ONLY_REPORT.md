# MESSAGEBUS APPEND ONLY REPORT

Fecha: 2026-05-12

## Estado

Estado: PASSED_LOCAL.

Archivo: `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\appendOnlyLog.ts`

Storage actual: `localStorage`

Storage key: `duat-telecom-core:messagebus:append-only:v1`

## Funciones implementadas

- `appendMessage(message)`
- `listMessages()`
- `getMessage(id)`
- `verifyLog()`
- `exportJsonl()`
- `importJsonl(jsonl)`
- `clearLocalLogForDevOnly()`

## Reglas aplicadas

- Rechaza IDs duplicados.
- Valida schema antes de persistir.
- Valida canal y kind permitido por canal.
- Recalcula hash antes de guardar.
- Mantiene `prev_hash` contra el ultimo mensaje del log.
- Exporta JSONL.
- Importa JSONL recalculando hash-chain local.
- `clearLocalLogForDevOnly()` queda marcado como herramienta de desarrollo, no operacional.

## Tests

| Test | Resultado |
|---|---|
| append guarda mensajes y verifica log | PASSED |
| append rechaza duplicado | PASSED |
| export JSONL genera lineas validas | PASSED |
| import JSONL recalcula cadena | PASSED |

## Riesgo residual

- Sigue siendo almacenamiento browser/localStorage.
- Las transiciones de estado legacy de `service.ts` aun sirven la UI mock; el ledger append-only ya existe, pero falta migrar toda mutacion operacional a eventos derivados.
- Siguiente capa recomendada: adaptador JSONL en disco y prueba de replay.
