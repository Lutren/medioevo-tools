# HANDOFF RUN 4

Fecha: 2026-05-12

Fingerprint: `MDV-MESSAGEBUS-RUN4-8E2B`

## Estado

R_close: 0.18

Phi_eff: 0.83

Regimen: FUNCIONAL

Autonomy level: 3

## Decisiones tomadas

- JSONL durable vive fuera del bundle React, en scripts Node-only.
- `/telecom` sigue en modo `localStorage`; solo muestra estado/plan durable.
- MCP real queda bloqueado hasta Run 5.
- No se extrae ZIP canon ni se habilita backend externo.

## Cambios realizados

- Scripts `scripts/messagebus/*` para append, verify, replay, stats y export-md.
- Librerias Node-only `scripts/messagebus/lib/*`.
- Fixtures JSONL validos/invalidos.
- Test durable `durableJsonl.test.mjs`.
- Log principal `02_RUNTIME/messagebus/logs/messagebus-main.jsonl`.
- Export Markdown `02_RUNTIME/messagebus/exports/messagebus-replay.md`.
- Panel minimo `Durable Log Status` en `/telecom`.

## Evidencia

- `npm test -- src/messagebus`: PASSED, 6 test files, 24 tests.
- `npx tsc -b --pretty false`: PASSED.
- `npm run build`: PASSED.
- `npm test`: PASSED, 7 test files, 35 tests.
- `messagebus:verify`: PASSED.
- `messagebus:replay`: PASSED.
- `python -m compileall -q .`: PASSED.
- `/telecom`: PASSED_LOCAL.

## Pendientes reales

- Run 5: MCP read-only server sobre JSONL durable.
- Agregar resources `messagebus://logs`, `messagebus://channels`, `messagebus://agents`, `messagebus://tasks`, `messagebus://handoffs`, `messagebus://witnesslog`.
- Tools read-only: `get_log_stats`, `verify_hash_chain`, `replay_channel`, `get_agent_inbox`, `export_handoff`.
- Migracion futura de todo historial `localStorage` a JSONL durable.

## Riesgos

- Log principal inicial contiene solo sample Run 4.
- JSONL en disco es durable pero no anti-manipulacion fisica; verificador detecta alteracion por hash-chain.
- Cualquier write tool MCP requiere ActionGate.
- Publicacion/push/deploy siguen bloqueados.

## Bloqueos

- No delete.
- No move.
- No rename.
- No push.
- No deploy.
- No publication.
- No backend externo.
- No Supabase.
- No secret printing.

## Proxima accion verificable

Implementar MCP read-only server local que lea el JSONL durable y exponga solo resources/tools read-only.

## Segunda perdida

Los datos persisten. El operador no. Recalibrar desde este handoff, no desde memoria implicita.
