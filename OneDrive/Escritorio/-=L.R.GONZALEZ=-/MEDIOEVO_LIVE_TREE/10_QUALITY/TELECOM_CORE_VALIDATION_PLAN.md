# TELECOM CORE VALIDATION PLAN

## Validacion Run 2

1. Verificar que Run 1 existe y que no hay archivos solicitados ausentes.
2. Verificar que `03_SYSTEMS` contiene arquitectura MessageBus.
3. Verificar que React/Vite build pasa.
4. Verificar que tests de MessageBus pasan.
5. Verificar ruta `/telecom` en navegador local.
6. Registrar que no hubo delete/move/rename/deploy/publication.

## Validacion Run 3

1. Crear validador de schema para `AgentMessage`.
2. Crear validador de canal permitido.
3. Crear validador hash-chain para `WitnessEvent`.
4. Migrar seed a JSONL/SQLite local.
5. Agregar export/import deterministicos.
6. Crear MCP read-only local para:
   - listar canales;
   - leer bulletin;
   - leer handoffs abiertos;
   - leer P0.
7. Solo despues, evaluar tools MCP con approval para ack/resolve.

## Criterios de aceptacion futuros

- `npm test`: pasa.
- `npm run build`: pasa.
- `python -m compileall -q .`: pasa para `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: pasa si existe suite Python; si no existe, reportar `NOT_APPLICABLE`.
- Browser local muestra `/telecom` no blanco y con paneles requeridos.
- No hay cambios destructivos.
