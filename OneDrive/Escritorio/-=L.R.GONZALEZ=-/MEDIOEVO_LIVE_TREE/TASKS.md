# TASKS

## P0

- Revisar `10_QUALITY/SECRET_SCAN_REPORT.md` por allowlist de target antes de cualquier publicacion.
- Mantener bloqueado push/deploy/publicacion mientras existan hallazgos enmascarados de secret scan.

## P1

- Migrar MEDIOEVO MessageBus de `localStorage` a JSONL/SQLite local append-only.
- Crear validador de schema/canales/hash-chain para `AgentMessage` y `WitnessEvent`.
- Revisar `08_CLEANUP/UNKNOWN_REVIEW.md`.
- Subir cobertura de candidatos `DELETE_AFTER_COVERAGE` solo con hash, destino claro y no-secretos.

## P2

- Crear MCP read-only local para listar canales, bulletin, handoffs y P0.
- Afinar fichas de `01_SOURCE_CARDS` para los 20 candidatos de mayor valor.
# Run 3 cierre / Run 4 entrada

- [ ] P1 Crear adaptador JSONL local en disco para `appendOnlyLog`.
- [ ] P1 Crear replay test: export JSONL -> import JSONL -> `verifyLog().ok === true`.
- [ ] P1 Migrar `ack/resolve/block` legacy a eventos derivados append-only.
- [ ] P1 Crear MCP read-only local para `medioevo://messagebus/*`.
- [ ] P2 Validar `evidence_refs` sin imprimir secretos.
- [ ] P2 Crear fixture de ledger Run 3 con hash-chain SHA-256.

# Run 4 cierre / Run 5 entrada

- [ ] P1 Crear MCP read-only server local sobre `messagebus-main.jsonl`.
- [ ] P1 Exponer resource `messagebus://logs`.
- [ ] P1 Exponer resource `messagebus://channels`.
- [ ] P1 Exponer resource `messagebus://agents`.
- [ ] P1 Exponer resource `messagebus://tasks`.
- [ ] P1 Exponer resource `messagebus://handoffs`.
- [ ] P1 Exponer resource `messagebus://witnesslog`.
- [ ] P1 Tools read-only: `get_log_stats`, `verify_hash_chain`, `replay_channel`, `get_agent_inbox`, `export_handoff`.
- [ ] P2 Diseñar migracion de historial browser `localStorage` hacia JSONL durable.
