# MESSAGEBUS VALIDATOR TEST REPORT

Fecha: 2026-05-12

## Resultado

Estado: PASSED_LOCAL.

## Validadores implementados

- `src/messagebus/messageTypes.ts`
- `src/messagebus/messageSchema.ts`
- `src/messagebus/messageValidator.ts`
- `src/messagebus/channelRegistry.ts`

## Reglas cubiertas

- `id` presente.
- `thread_id` presente.
- `channel_id` permitido.
- `from_agent` permitido.
- `to_agents` valido y no vacio.
- `kind`, `priority`, `status` permitidos.
- `title` y `body` no vacios.
- `R_estimado` entre 0 y 1.
- `Phi_eff` entre 0 y 1 cuando existe.
- `certeza`, `inferencia`, `incognita`, `bloqueo`, `evidence_refs`, `artifact_refs`, `witness_event_ids`, `ack_by` como arrays.
- `created_at` y `updated_at` ISO validos.
- `hash` presente.
- `MessageKind` permitido por canal.

## Tests

| Test | Resultado |
|---|---|
| mensaje valido pasa | PASSED |
| mensaje sin title falla | PASSED |
| canal invalido falla | PASSED |
| kind no permitido para canal falla | PASSED |

## Comandos

- `npm test -- src/messagebus`: PASSED, 5 test files, 15 tests.
- `npm test`: PASSED, 6 test files, 26 tests.
- `npm run build`: PASSED.

## Riesgo residual

- El validador comprueba estructura y registry; no verifica existencia real de rutas en `evidence_refs`.
- La inspeccion de rutas secret-like debe quedar en un gate adicional antes de backend/MCP write tools.
