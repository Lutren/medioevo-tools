# TASKS RUN 5

Fecha: 2026-05-12

Fingerprint entrada esperado: `MDV-MESSAGEBUS-RUN4-8E2B`

## Objetivo

Crear MCP read-only server sobre JSONL durable.

## Resources

- `messagebus://logs`
- `messagebus://channels`
- `messagebus://agents`
- `messagebus://tasks`
- `messagebus://handoffs`
- `messagebus://witnesslog`

## Tools read-only

- `get_log_stats`
- `verify_hash_chain`
- `replay_channel`
- `get_agent_inbox`
- `export_handoff`

## P0

- No tools de escritura.
- No backend externo.
- No Supabase.
- No lectura de secretos.
- No push/deploy/publicacion.

## P1

- Crear servidor MCP local que use `scripts/messagebus/lib/*`.
- Smoke test de resources sobre `messagebus-main.jsonl`.
- Verificar que `messagebus:verify` sigue pasando antes y despues.
- Documentar ActionGate para futuras write tools.

## P2

- Agregar resource para artifact registry.
- Agregar export `messagebus://bulletin/latest`.
- Diseñar migracion de `localStorage` browser a JSONL durable.

## Criterio de cierre

- MCP read-only smoke: PASSED.
- `npm test`: PASSED.
- `npm run build`: PASSED.
- `messagebus:verify`: PASSED.
- Handoff Run 5 generado.
