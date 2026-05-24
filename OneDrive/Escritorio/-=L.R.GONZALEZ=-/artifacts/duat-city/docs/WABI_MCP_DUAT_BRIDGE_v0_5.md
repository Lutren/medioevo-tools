# WABI_MCP_DUAT_BRIDGE_v0_5

## v0.4 Status Preserved

- `gated_write_enabled=false`
- `execution_allowed=false`
- `real_apply_allowed=false`
- scheduler/execute-local-workpack no ejecutan
- no cloud, push, deploy, commit ni publicacion

## v0.5 Intent

Agregar un bridge de diseño integrable para DUAT City, sin activar ejecucion real.

## Runtime Status

```json
{
  "version": "v0.5-design",
  "mode": "LOCALHOST_ONLY_READ_PREPARE_SANDBOX_OPT_IN_DESIGN",
  "gated_write_enabled": false,
  "execution_allowed": false,
  "sandbox_execution_allowed": false,
  "real_apply_allowed": false,
  "external_clients_allowed": false
}
```

## Workpack Drafts

`createWorkpackDraftFromCity(state)` genera:

- archivos sugeridos
- tareas propuestas
- riesgos
- tests a correr
- rollback plan

No ejecuta comandos ni aplica parches.

## Sandbox Policy

`createSandboxExecutionDesign(state)` devuelve una politica futura:

- sandbox root
- allowlist
- denylist
- comandos vacios
- disabled by default
- requiere opt-in futuro explicito

## UI

`WabiPanel` muestra estado design-only y permite descargar:

- workpack draft JSON
- Wabi handoff JSON

Ambos son artefactos de preparacion, no ejecucion.

## Tests

- `wabiBridge.test.ts`
- `integrationV05.test.ts`
