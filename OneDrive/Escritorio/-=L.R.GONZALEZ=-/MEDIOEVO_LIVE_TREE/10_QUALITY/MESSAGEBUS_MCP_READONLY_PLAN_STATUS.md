# MESSAGEBUS MCP READONLY PLAN STATUS

Fecha: 2026-05-12

Estado: PLAN_CREATED / SERVER_NOT_IMPLEMENTED.

## Artefacto

Plan tecnico creado en:

`03_SYSTEMS/MESSAGEBUS_MCP_READONLY_PLAN.md`

## Recursos definidos

- `medioevo://messagebus/latest`
- `medioevo://messagebus/channels`
- `medioevo://messagebus/handoffs/latest`
- `medioevo://messagebus/tasks/open`
- `medioevo://messagebus/witnesslog/recent`
- `medioevo://messagebus/security/p0`

## Herramientas futuras

- `create_message`: FUTURE / REQUIRES ACTIONGATE
- `ack_message`: FUTURE / REQUIRES ACTIONGATE
- `append_witness_event`: FUTURE / REQUIRES ACTIONGATE
- `create_handoff`: FUTURE / REQUIRES ACTIONGATE
- `claim_task`: FUTURE / REQUIRES ACTIONGATE
- `resolve_task`: FUTURE / REQUIRES ACTIONGATE

## Bloqueos

- No servidor MCP real en Run 3.
- No write tools sin ActionGate.
- No backend externo.
- No lectura de secretos ni ZIP expandido.

## Entrada recomendada a Run 4

Crear adaptador read-only que sirva recursos desde JSONL local verificado, sin exponer herramientas de escritura.
