# TASKS RUN 4

Fecha: 2026-05-12

Fingerprint entrada esperado: `MDV-MESSAGEBUS-RUN3-2A91`

## P0

- Mantener bloqueo de push/deploy/publicacion hasta gate especifico.
- No extraer `MEDIOEVO_OSIT_v12_2_1_CARPETA_MAESTRA_RECONSTRUCTIVA.zip` sin expansion controlada read-only aprobada.

## P1

- Crear adaptador JSONL local en disco para `appendOnlyLog`.
- Crear replay test: export JSONL -> import JSONL -> `verifyLog().ok === true`.
- Migrar transiciones `ack/resolve/block` a eventos derivados append-only, sin sobrescribir mensajes base.
- Crear MCP server read-only minimo para los recursos definidos en `MESSAGEBUS_MCP_READONLY_PLAN.md`.

## P2

- Validar existencia de rutas en `evidence_refs` sin leer secretos.
- Agregar reporte de divergencia entre seed TypeScript y JSON seed.
- Crear fixture de ledger Run 3 con hash-chain SHA-256.

## Criterio de cierre Run 4

- `npm run build`: PASSED.
- `npm test`: PASSED.
- JSONL replay: PASSED.
- MCP read-only smoke local: PASSED si se implementa servidor; si no, `NOT_IMPLEMENTED` documentado.
