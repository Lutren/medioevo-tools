# DUAT_OPERATOR_SHELL_V0_1_SPEC_2026-05-15

Status: `SPEC_LOCAL_ONLY`

Kernel P0 implementado:
`packages/open-dev/claudio-agent-runtime`

Blueprint base:
`docs/developer/CLAUDIO_PUBLIC_AGENT_RUNTIME_BLUEPRINT_2026-05-15.md`

## Decision

`DUAT Operator Shell` es la capa humana/producto. `claudio-agent-runtime` es el
kernel tecnico P0.

No se reemplaza Claudio, BRAIN_OS, COMMS ni DUAT. Se crea una superficie clara
para operar agentes persistentes con permisos, memoria, skills, handoff y
evidencia sin exponer canon privado.

## Frontera

Permitido en v0.1:

- runtime local;
- permisos dry-run;
- skills `SKILL.md` con progressive disclosure;
- memoria JSONL local;
- task board JSON;
- briefs y fingerprints;
- tests y fixtures sinteticos.

Review requerido:

- SQLite/FTS;
- provider fallback real;
- subagentes concurrentes;
- scheduler persistente;
- daemon/servicio;
- Telegram, GitHub, Spotify o canales externos;
- cualquier publicacion.

Bloqueado:

- secretos;
- libros completos;
- RPG/TCG;
- DUAT/GEODIA privado;
- prompts privados crudos;
- datasets no revisados;
- acciones destructivas o externas sin gate.

## Layout recomendado

Para entorno generico:

```txt
~/.duat/
  duat.yaml
  permissions.yaml
  providers.yaml
  budget.json
  skills/
  memory/
    witnesslog.jsonl
    memory_lite.jsonl
    handoffs/
  tasks/
    task-board.json
    locks.json
  agents/
    active-agents.json
  logs/
```

Para MEDIOEVO local, no ocultar estado:

```txt
C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\00_START_HERE\LIVE_STATE\
  duat_operator_shell\
    permissions.yaml
    memory_lite.jsonl
    task-board.json
    locks.json
    NEXT_SESSION_BRIEF.md
    SESSION_FINGERPRINT.json
```

`~/.duat` puede existir para configuracion generica, pero la version viva del
workspace debe tener espejo humano-visible en BRAIN_OS/COMMS.

## Skills OSIT

Formato recomendado:

```yaml
---
name: actiongate-review
description: Reviews proposed actions before execution using OSIT gates.
version: 0.1.0
gate: REVIEW_EXTERNAL
allowed-tools:
  - read_file
  - list_dir
  - git_diff
osit:
  max_R: 0.35
  requires_source_cards: true
  requires_handoff: true
  reversible_only_by_default: true
  output_schema:
    - ESTADO
    - CERTEZA
    - INFERENCIA
    - INCOGNITA
    - ACCION
    - HANDOFF
---
```

Regla: el loader de v0.1 solo lista metadata. La carga completa del cuerpo
ocurre bajo demanda.

## Modulos v0.1

| modulo | estado | fuente |
|---|---|---|
| `doctor` | implementado P0 | `claudio-agent-runtime` |
| `GhostGate plan` | implementado P1 read-only | filtra herramientas de plan |
| `permissions check` | implementado P0 | `claudio-agent-runtime` |
| `skills list/inspect` | implementado P0 | `claudio-agent-runtime` |
| `memory status/search` | implementado P0 | `claudio-agent-runtime` |
| `tasks list/add` | implementado P0 | `claudio-agent-runtime` |
| `brief` | implementado P0 | `claudio-agent-runtime` |
| `WitnessLog` | implementado P0 | JSONL append-only opcional por comando |
| `ActionGate execute` | implementado P1 limitado | solo `write_file` local reversible con rollback |
| `SQLite/FTS memory` | REVIEW P1/P2 | no obligatorio |
| subagentes + locks | REVIEW P1/P2 | despues de TaskBoard |
| daemon/scheduler | REVIEW P2 | despues de host gate |

## CLI objetivo

Comandos P0 actuales:

```powershell
python -m claudio_agent_runtime doctor --json
python -m claudio_agent_runtime ghostgate tools --json
python -m claudio_agent_runtime ghostgate check fixtures\ghostgate_plan_allowed.json --json
python -m claudio_agent_runtime permissions check fixtures\permission_local_write.json --json
python -m claudio_agent_runtime execute write fixtures\execute_write_approved.json --root <temp-root> --json
python -m claudio_agent_runtime rollback restore <rollback-id> --root <temp-root> --json
python -m claudio_agent_runtime skills list --root fixtures\skills --json
python -m claudio_agent_runtime memory status --root fixtures\state --json
python -m claudio_agent_runtime tasks list --root fixtures\state --json
python -m claudio_agent_runtime brief --root fixtures\state
python -m claudio_agent_runtime witness status --root fixtures\state --json
```

Todos los comandos P0 aceptan `--witness-root <state-root>` para registrar un
evento JSONL redactado sin guardar el output completo.

Alias futuro:

```txt
duat doctor
duat gate check <payload.json>
duat skills
duat memory status
duat tasks
duat handoff
```

## Presupuesto

Mercury usa token budget. DUAT Operator Shell debe medir dos presupuestos:

- costo operacional: tokens, pasos, llamadas, tiempo;
- costo epistemico: `R_est`, `Phi_eff_est`, evidencia faltante, jamming.

P0 solo reporta estado. P1 debe calcular `R/Phi` desde evidencia local.

## Plan/Execute

Modo v0.1 recomendado:

- `plan`: lectura, propuesta, riesgos, no escritura;
- `execute`: escritura local reversible solo si `ActionGate=APPROVE`;
- `halt`: detener subagentes/scheduler futuros;
- `handoff`: cerrar con evidencia.

Traduccion OSIT:

```txt
GhostGate -> formula plan y bloqueos.
ActionGate -> autoriza o detiene accion concreta.
Executor -> ejecuta solo local/reversible.
WitnessLog -> registra resultado.
Handoff -> permite continuidad.
```

## Prompt de implementacion externo seguro

```text
Build a local-first DUAT Operator Shell for persistent AI agents with evidence,
gates, memory, skills, handoff and controlled execution.

Do not include private canon, raw prompts, secrets, unpublished books, private
datasets, RPG/TCG material, commercial automation internals or external actions.

Implement first:
1. runtime folder with configurable state root;
2. permission manifest with folder scopes and shell policy;
3. ActionGate before write, shell, git, network or publish action;
4. SKILL.md loader with progressive disclosure;
5. memory JSONL with source/evidence/boundary tags;
6. task board with status/evidence/owner;
7. Handoff generator after each task;
8. doctor/status commands;
9. tests and fixtures.
```

## Criterios de avance

P0 queda cerrado cuando:

- `claudio-agent-runtime` tests pasan;
- secret scan focalizado pasa;
- smoke de `doctor`, `permissions`, `skills`, `memory`, `tasks`, `brief` pasa;
- no hay dependencias nuevas;
- no hay canales externos.

P1 puede abrirse con:

- `R/Phi` calculado desde task board/memory/evidence.

P2 sigue bloqueado para shell, git write, red, canales externos, scheduler,
daemon y subagentes hasta que haya gates y pruebas especificas.
