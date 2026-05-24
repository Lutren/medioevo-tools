# CLAUDIO_PUBLIC_AGENT_RUNTIME_BLUEPRINT_2026-05-15

Status: `BLUEPRINT_APPROVED_FOR_LOCAL_PLANNING`

ActionGate:

- `APPROVE`: documentacion, interfaces, tests locales, stubs sin red y sin secretos.
- `REVIEW`: instalar Mercury, copiar codigo externo, adoptar dependencias, activar Telegram/GitHub/Spotify, publicar paquete.
- `BLOCK`: exponer Observacionismo privado, DUAT/GEODIA interno, libros completos, RPG/TCG, secretos o acciones externas no aprobadas.

Fuente detonante: `docs/intake/MERCURY_AGENT_SOURCE_CARD_2026-05-15.md`.

## Decision

La mejor accion no es importar Mercury Agent. La mejor accion es usarlo como
patron de producto para extraer una superficie publica-segura de Claudio:

`Claudio Public Agent Runtime`

Promesa publica:

1. permiso antes de actuar;
2. memoria con evidencia y limites;
3. skills cargadas bajo demanda;
4. continuidad local verificable.

Esto mantiene la ventaja propia de MEDIOEVO: `ActionGate`,
`ObservationEnvelope`, `R/Phi/Jamming`, curaduria, handoff y frontera
publico/privado.

## Producto minimo

Un runtime local-first con CLI y estado persistente, sin canal externo por
defecto:

```txt
claudio doctor
claudio status
claudio permissions list
claudio permissions check <action>
claudio action-gate evaluate <payload.json>
claudio skills list
claudio skills inspect <name>
claudio memory status
claudio memory search <query>
claudio tasks list
claudio tasks add <task.json>
claudio brief
```

No debe ejecutar publicaciones, pushes, mensajes externos, pagos, browser auth,
Telegram, GitHub write, Spotify ni limpieza destructiva en el MVP.

## Capas

| capa | responsabilidad | fuente local sugerida |
|---|---|---|
| CLI publica | comandos pequenos, JSON estable, salida humana | nuevo wrapper o extension controlada de Wabi-Sabi |
| Permission UX | scopes por carpeta, dry-run, aprobacion por accion | `ActionGate` + manifiesto local |
| ActionGate adapter | `APPROVE/REVIEW/BLOCK` con razones | `packages/open-dev/obsai-core/obsai_core/gate.py` |
| Tool registry | herramientas, lecturas, escrituras, validacion | `apps/local/wabi-sabi/wabi_sabi/core/tool_registry.py` |
| Skill registry | `SKILL.md`, nombre/descripcion al inicio, cuerpo bajo demanda | `tools/harness/skills`, Codex skills, OSIT skill registry |
| MemoryLite | memoria compacta con evidencia y expiracion | JSONL primero; SQLite/FTS opcional despues |
| TaskBoard | tareas, locks, evidencia, estado | nuevo modulo publico-seguro |
| Scheduler | tareas locales reversibles | `REVIEW` hasta que TaskBoard y ActionGate pasen |
| Watchdog | PID/log/status local | `REVIEW` si se instala como servicio |
| Handoff | `NEXT_SESSION_BRIEF`, fingerprint y witness | BRAIN_OS/COMMS |

## Estado persistente

El runtime publico puede tener una raiz de datos configurable. Regla:
no esconder el estado operacional importante cuando se corre dentro de MEDIOEVO.

```txt
CLAUDIO_STATE_ROOT/
  config/
    permissions.yaml
    runtime.yaml
  skills/
    <skill-name>/SKILL.md
  memory/
    memory_lite.jsonl
    profile_summary.md
  tasks/
    task_board.json
    locks.json
  schedules/
    schedules.yaml
  witness/
    witness_log.jsonl
  logs/
    claudio-runtime.log
  handoff/
    NEXT_SESSION_BRIEF.md
    SESSION_FINGERPRINT.json
```

Para MEDIOEVO local:

- estado humano visible: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\00_START_HERE\LIVE_STATE`
- coordinacion/agentes: `COMMS`
- evidencias tecnicas: `qa_artifacts`, `runtime`, `docs/ops`

Para paquete publico generico:

- usar `CLAUDIO_STATE_ROOT` si existe;
- si no existe, usar una ruta de usuario documentada;
- nunca guardar secretos en docs, logs, witness o memoria.

## Contratos minimos

### Permission request

```json
{
  "schema_version": "claudio.permission_request.v0.1",
  "action": "write_file",
  "target": "docs/example.md",
  "scope": "workspace",
  "risk_tags": ["local", "reversible"],
  "evidence": ["dry_run=true"]
}
```

Resultado:

```json
{
  "decision": "APPROVE",
  "reason": "local reversible write inside declared workspace",
  "required_review": false
}
```

### Memory item

```json
{
  "schema_version": "claudio.memory_lite.v0.1",
  "type": "decision",
  "summary": "Mercury is reference only, not runtime dependency.",
  "source": "docs/intake/MERCURY_AGENT_SOURCE_CARD_2026-05-15.md",
  "confidence": 0.95,
  "durability": "active",
  "boundary_tags": ["public_safe", "external_reference"],
  "expires_at": null
}
```

### Skill manifest view

Startup carga solo:

```json
{
  "name": "release-guard",
  "description": "Check public release gates before packaging or external action.",
  "gate": "REVIEW_EXTERNAL",
  "path": "skills/release-guard/SKILL.md"
}
```

La instruccion completa se carga solo al invocar la skill.

## Permisos

| accion | MVP decision | comentario |
|---|---|---|
| leer arbol del workspace | `APPROVE` | sin imprimir secretos |
| escribir docs nuevos | `APPROVE` | dentro de workspace y con evidencia |
| editar codigo existente | `REVIEW` si hay dirty worktree; `APPROVE` solo path-owned |
| ejecutar tests locales | `APPROVE` | comandos allowlist |
| instalar dependencias | `REVIEW` | ficha y prueba aislada |
| red / fetch externo | `REVIEW` | registrar fuente |
| Telegram/GitHub write/Spotify | `REVIEW` | credenciales y canal externo |
| push/deploy/publicacion | `REVIEW` | host gate + humano |
| borrar/mover volumen | `BLOCK` sin gate exacto | cleanup contract |
| tocar RPG/TCG/libros completos/secretos | `BLOCK` | frontera dura |

## Comandos P0

### `claudio doctor`

Debe reportar:

- `state_root`: presente/ausente;
- `permissions_manifest`: presente/ausente;
- `action_gate`: modulo disponible;
- `skills_registry`: cantidad y errores de schema;
- `memory_lite`: presente/ausente y cantidad;
- `task_board`: presente/ausente;
- `host_gate`: `UNKNOWN|APPROVE|REVIEW|BLOCK`;
- `secrets`: solo presencia/ausencia, nunca valores;
- `external_channels`: disabled por defecto.

### `claudio status`

Debe reportar:

- regimen actual si hay R/Phi;
- pendientes abiertos;
- ultima evidencia;
- proxima accion verificable;
- publication gate.

### `claudio permissions check`

Debe evaluar una accion sin ejecutarla. Salida JSON estable con
`decision`, `reason`, `risk_tags`, `review_required`, `blocked`.

### `claudio skills list`

Debe listar `name`, `description`, `gate`, `path`, `loaded=false`.
No debe cargar todos los cuerpos `SKILL.md` en el prompt.

### `claudio memory status`

Debe reportar conteos por tipo y estado de aprendizaje. No debe volcar memoria
privada completa por defecto.

### `claudio tasks list`

Debe listar tareas persistentes con estado, prioridad, evidencia y owner.

## Aceptacion P0

- No hay dependencias nuevas.
- No hay acciones externas.
- No hay copia de codigo de Mercury.
- Secret scan focalizado sobre artefactos nuevos: `count_reported=0`.
- Si hay codigo: tests locales pasan o se registra `KNOWN_FAILURE`.
- `doctor` funciona sin proveedores configurados.
- `permissions check` puede devolver `APPROVE`, `REVIEW` y `BLOCK` con fixtures.
- `skills list` carga metadatos sin cargar el cuerpo completo.
- `memory status` no imprime secretos ni conversaciones completas.
- `tasks list` no requiere red ni DB externa.

## Orden de implementacion

1. Crear workpack P0 con ownership de archivos y tests.
2. Implementar CLI read-only: `doctor`, `status`, `permissions check`.
3. Agregar `skills list/inspect` con progressive disclosure.
4. Agregar `memory status/search` con JSONL, sin SQLite todavia.
5. Agregar `tasks list/add` con TaskBoard JSON y locks simples.
6. Solo despues evaluar scheduler/watchdog local.
7. Solo con review reabrir canales externos.

## No hacer todavia

- No `npm install`, no `pip install`, no vendor.
- No servicio Windows.
- No Telegram.
- No GitHub write.
- No daemon persistente.
- No memoria autonoma invisible sobre material privado.
- No publish, push, deploy, Gumroad ni redes.

## Primer workpack recomendado

Archivo: `docs/developer/CLAUDIO_PUBLIC_AGENT_RUNTIME_WORKPACK_2026-05-15.md`

Objetivo: implementar solo la capa P0 read-only/dry-run, con fixtures y tests,
usando contratos locales existentes antes de crear otro runtime paralelo.

