# CLAUDIO_PUBLIC_AGENT_RUNTIME_WORKPACK_2026-05-15

Status: `READY_FOR_LOCAL_IMPLEMENTATION`

Parent blueprint:
`docs/developer/CLAUDIO_PUBLIC_AGENT_RUNTIME_BLUEPRINT_2026-05-15.md`

## Objetivo

Construir la primera capa verificable de `Claudio Public Agent Runtime` usando
patrones extraidos de Mercury Agent sin instalarlo ni copiar su codigo.

Este workpack es P0: solo lectura, dry-run, estado local, fixtures y tests.

## Ownership sugerido

No tocar codigo legacy de `-=MEDIOEVO=-\-=LIBROS\claudio` en este primer corte.
Ese arbol tiene capas mezcladas y trabajo concurrente.

Ruta preferida para el primer corte:

```txt
packages/open-dev/claudio-agent-runtime/
```

Si se decide no crear paquete nuevo, segunda opcion:

```txt
apps/local/wabi-sabi/
```

Pero en Wabi-Sabi hay varios archivos modificados/no trackeados; antes de
editar ahi hay que revisar ownership por archivo.

## Dependencias

Permitido:

- Python stdlib;
- imports internos ya existentes si el paquete queda dentro del workspace;
- fixtures JSON/JSONL locales.

No permitido en P0:

- instalar dependencias nuevas;
- copiar codigo de Mercury;
- SQLite obligatorio;
- red;
- Telegram/GitHub/Spotify;
- daemon/service install;
- acciones destructivas.

## Modulos P0

| modulo | salida minima | gate |
|---|---|---|
| `doctor` | JSON con estado de runtime, secrets presence-only, canales disabled | `APPROVE` |
| `permissions` | evalua acciones contra ActionGate sin ejecutar | `APPROVE` |
| `skills_registry` | lista metadata de `SKILL.md` sin cargar cuerpo completo | `APPROVE` |
| `memory_lite` | JSONL con tipos, confianza, fuente y boundary tags | `APPROVE` |
| `task_board` | tareas JSON con estado/evidencia/owner | `APPROVE` |
| `brief` | genera handoff corto desde estado local | `APPROVE` |

## Contratos de comandos

```powershell
python -m claudio_agent_runtime doctor --json
python -m claudio_agent_runtime permissions check fixtures\permission_local_write.json
python -m claudio_agent_runtime permissions check fixtures\permission_external_publish.json
python -m claudio_agent_runtime skills list --root fixtures\skills --json
python -m claudio_agent_runtime memory status --root fixtures\state --json
python -m claudio_agent_runtime tasks list --root fixtures\state --json
python -m claudio_agent_runtime brief --root fixtures\state
```

## Fixtures requeridos

```txt
fixtures/
  permission_local_write.json
  permission_external_publish.json
  permission_sensitive_path.json
  skills/
    release-guard/SKILL.md
    curator/SKILL.md
  state/
    memory/memory_lite.jsonl
    tasks/task_board.json
```

Resultados esperados:

| fixture | decision esperada |
|---|---|
| `permission_local_write.json` | `APPROVE` |
| `permission_external_publish.json` | `REVIEW` |
| `permission_sensitive_path.json` | `BLOCK` |

## Tests minimos

```powershell
python -m pytest packages\open-dev\claudio-agent-runtime\tests -q
```

Cobertura minima:

- `doctor` no falla sin `.env`;
- `doctor` no imprime valores de secretos;
- `permissions check` cubre `APPROVE`, `REVIEW`, `BLOCK`;
- `skills list` devuelve nombre/descripcion/gate/path;
- `skills list` no incluye el cuerpo completo de `SKILL.md`;
- `memory status` cuenta por tipo y no imprime entradas completas;
- `tasks list` muestra tareas sin ejecutar nada;
- `brief` genera proxima accion verificable.

## Criterios de cierre

- `py_compile` o `pytest` pasan.
- Secret scan focalizado de la ruta nueva devuelve `count_reported=0`.
- No hay dependencia nueva en `pyproject.toml` salvo metadata local.
- No se toca `-=MEDIOEVO=-\-=LIBROS\claudio`.
- No se toca RPG/TCG/libros completos.
- No se modifica configuracion global del host.
- `NEXT_SESSION_BRIEF` o handoff de docs apunta a la siguiente accion.

## Siguiente accion exacta

Crear `packages/open-dev/claudio-agent-runtime/` con:

```txt
README.md
pyproject.toml
claudio_agent_runtime/
  __init__.py
  __main__.py
  doctor.py
  permissions.py
  skills_registry.py
  memory_lite.py
  task_board.py
  brief.py
fixtures/
tests/
```

Mantener la implementacion stdlib-only. Si aparece necesidad de SQLite, dejarlo
como P1 y seguir con JSONL en P0.
