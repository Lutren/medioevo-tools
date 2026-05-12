# NEXT_SESSION_BRIEF MEDIOEVO/OSIT LIVE TREE

## Estado

R_close: 0.18
Phi_eff: 0.83
Regimen: FUNCIONAL
Autonomy level: 3

## Decisiones tomadas

- Run 4 creo persistencia durable JSONL en disco para `MEDIOEVO MessageBus`.
- El acceso a disco vive solo en scripts Node-only bajo `scripts/messagebus`.
- React `/telecom` sigue en `localStorage`; no importa `fs`, `path`, `crypto` ni scripts Node-only.
- MCP queda para Run 5 como servidor read-only sobre JSONL durable.

## Cambios realizados

- Se crearon scripts `messagebus:append-sample`, `messagebus:verify`, `messagebus:replay`, `messagebus:stats`, `messagebus:export-md`.
- Se creo `02_RUNTIME/messagebus/logs/messagebus-main.jsonl`.
- Se creo export `02_RUNTIME/messagebus/exports/messagebus-replay.md`.
- Se agregaron fixtures validos/invalidos y test `durableJsonl.test.mjs`.
- `/telecom` recibio seccion minima `Durable Log Status`.

## Evidencia

- `npm test -- src/messagebus`: PASSED, 6 test files, 24 tests.
- `npx tsc -b --pretty false`: PASSED.
- `npm run build`: PASSED.
- `npm test`: PASSED, 7 test files, 35 tests.
- `messagebus:verify`: PASSED.
- `messagebus:replay`: PASSED.
- `messagebus:stats`: PASSED.
- `messagebus:export-md`: PASSED.
- `python -m compileall -q .`: PASSED en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: NOT_APPLICABLE; no hay suite Python en `MEDIOEVO_LIVE_TREE`.
- `http://127.0.0.1:5174/telecom`: PASSED_LOCAL.
- `src/ui/TelecomCore.tsx` servido por Vite contiene `Durable Log Status` y no contiene imports Node-only.

## Pendientes reales

- Crear servidor MCP read-only local sobre JSONL durable.
- Migrar `localStorage` browser hacia JSONL durable si se decide consolidar historial.
- Migrar `ack/resolve/block` legacy a eventos derivados append-only.
- Verificar `evidence_refs` sin imprimir secretos.

## Riesgos

- Secret scan Run 1 mantiene bloqueados push/deploy/publicacion.
- ZIP reconstructivo sigue sin revision profunda.
- El log JSONL principal contiene solo muestra Run 4 inicial.
- JSONL durable detecta alteraciones por hash-chain, pero no impide manipulacion fisica del archivo.
- Seed UI/runtime puede divergir si no se consolida con JSONL.

## Bloqueos

- No delete.
- No move.
- No rename.
- No deploy.
- No publication.
- No secret printing.
- No Supabase ni credenciales.

## Proxima accion verificable

Implementar MCP read-only server local que lea `messagebus-main.jsonl` y exponga solo resources/tools read-only.

## Segunda perdida

Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.
