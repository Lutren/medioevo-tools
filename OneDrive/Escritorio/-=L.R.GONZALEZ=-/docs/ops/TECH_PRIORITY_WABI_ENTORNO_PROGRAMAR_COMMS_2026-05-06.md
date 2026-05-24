# Prioridad Tecnologica: Wabi, Entorno, Programacion Y COMMS

Fecha: 2026-05-06
Estado: `IMPLEMENTACION_LOCAL_READ_ONLY / HOST_BLOCK`

Actualizacion de producto: se implemento el primer corte de
`Wabi-Sabi Operational Control Plane v0.2` en
`apps/local/wabi-sabi`. Incluye `EnvironmentSnapshot`, `CommsBridge` read-only,
CLI `wabi env-status`, CLI `wabi comms-state`, artefactos JSON en
`runtime/outputs`, eventos append-only y tests focales. No se habilito append
COMMS, publicacion, modelos pesados ni programacion multiarchivo.

Actualizacion posterior: se implemento `DecisionLogAdapter` con CLI
`wabi decide` y `wabi decision-log`. La decision queda en artefacto JSON,
ledger append-only, TaskManager compatible `obsai.task_manager.v1` y WitnessLog
SQLite. Bajo host `BLOCK`, registra estado `BLOCKED/P1` sin ejecutar acciones
externas ni append COMMS.

Actualizacion COMMS: se implemento `comms-append-plan`, que genera el mensaje
COMMS `seto-observation-v1` desde el ultimo DecisionRecord y lo deja como
workpack. Bajo host `BLOCK`, `append_allowed=false` y `append_performed=false`;
no se escribe outbox real.

Actualizacion programacion: se implemento `programmer-workpack`, un workpack
multiarchivo `PLAN_ONLY`. Bajo host `BLOCK`, queda `application_gate=BLOCK`,
`patches=[]` y no aplica cambios.

Evidencia post-implementacion:

```powershell
python -m pytest tests -q
.\wabi.cmd env-status --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd comms-state --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

Resultado inicial: `53 passed in 3.25s`; snapshot real con
`pending.active_dedup=15`, `host=JAMMING/BLOCK`, `COMMS agent_count=12`,
`COMMS validator=PASS` y `decision.recommended_mode=A0_LOCAL_REVIEW_ONLY`.

Evidencia DecisionLog:

```powershell
python -m pytest tests -q
.\wabi.cmd decide "continuar pendientes locales sin cruzar gates" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd decision-log --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

Resultado posterior: `55 passed in 2.95s`; record hash
`F41DFD0587BC3ECF0F496F2E07E908062401EA7344A5E88FDCA67DF041934FA6`,
`witness_verified=true`, `pending.active_dedup=3`,
`recommended_mode=A0_LOCAL_REVIEW_ONLY`.

Evidencia COMMS plan: `56 passed in 3.29s`,
`wabi_comms_append_plan_20260506-123143.json`, COMMS validator `PASS`,
outbox real de Wabi no creado.

Evidencia programmer workpack: `57 passed in 3.78s`,
`wabi_programmer_workpack_20260506-123540.json`,
`workpack_hash=6C2D3EDE1D59D003A2AB307A181D5EEB7505DBA3AE5B39AF8D25B7BD21D6FC63`,
`mode=PLAN_ONLY`, `application_gate=BLOCK`, `patches=[]`.

## Decision Ejecutiva

La tecnologia que mas ayuda primero no es un modelo, un daemon ni una UI. Es
`Wabi-Sabi como plano de control operacional`, conectado a:

1. `entorno`: host gate, pending review, blueprint policy y estado de recursos;
2. `COMMS`: mensajes append-only, agentes, handoffs y WitnessLog;
3. `programar`: workpacks y parches acotados bajo ActionGate;
4. `Matrix/Mission Control`: lectura visual posterior, no fuente primaria.

La implementacion prioritaria debe ser:

```text
Wabi-Sabi Operational Control Plane v0.2
  -> EnvironmentSnapshot
  -> COMMSBridge read/write append-only
  -> DecisionLog adapter sobre TaskManager/WitnessLog
  -> Programmer dry workpack / scoped patch gate
```

En el gate actual `JAMMING/BLOCK`, la accion correcta es documentar y preparar
el workpack. No conviene abrir codigo nuevo hasta que host baje de `BLOCK`.

## Evidencia De Entrada

Comandos ejecutados en este pase:

```powershell
python tools\release\pending_review.py --write --quiet
python tools\host_observacionista.py --no-write
python COMMS\tools\validate_seto_comms.py --json
.\wabi.cmd auto /status --json
```

Resultados vigentes:

| verificacion | resultado |
|---|---|
| `pending_review` raiz | `active_dedup=15`, `claudio_open=0` |
| host observacionista | `JAMMING/BLOCK`, `lambda_sat=1.0`, dominante `r_cpu` |
| COMMS validator | `PASS`, `errors=[]`, `warnings=[]`, `outbox_messages=43` |
| Wabi status | `ok=true`, `Auto provider=codex-cli`, `Orden=codex,dry-run`, `Planos=OK`, `Planos fuentes=7`, `Ollama=OPCIONAL/APAGADO` |
| documentos activos inventariados | `673` Markdown activos fuera de archives/vendors/builds |
| docs relevantes por keywords | `454` Markdown con Wabi/COMMS/programacion/gates/entorno |

Nota de continuidad: `CLAUDE.md` no existe dentro de `claudio/`; existe
`claudio/CLAUDE.md.backup` y el `CLAUDE.md` activo se encontro en
`-=MEDIOEVO=-\-=LIBROS\CLAUDE.md`.

## Documentos Y Sistemas Leidos

Gobierno y seguridad:

- `AGENTS.md`
- `docs/control/AUDIT_REPO_TREE.md`
- `PRODUCT_MAP.md`
- `VISIBILITY_MATRIX.md`
- `RISK_REGISTER.md`
- `docs/security/SECRET_SCAN_REPORT.md`
- `DUPLICATES_AND_DEAD_CODE.md`
- `docs/release/RELEASE_READINESS_SCORE.md`
- `CORE_MODULE_INVENTORY.md`
- `IMPLEMENTATION_PLAN.md`
- `TASKS.md`
- `NEXT_SESSION_BRIEF.md`

Wabi-Sabi:

- `apps/local/wabi-sabi/README.md`
- `apps/local/wabi-sabi/docs/ARCHITECTURE.md`
- `apps/local/wabi-sabi/docs/USAGE.md`
- `apps/local/wabi-sabi/docs/CONVERSATIONAL_BLUEPRINTS_2026-05-06.md`
- `apps/local/wabi-sabi/REPORT_WABI_SABI_LOCAL_AGENTS.md`
- `docs/ops/WABI_SABI_QWEN_BLUEPRINT_WORKPACK_2026-05-06.md`
- `docs/ops/WABI_OSIT_BRIDGE_FROM_ESTADO_2026-05-06.md`
- `docs/ops/OSIT_RESOURCE_OPTIMIZER_RUNTIME_SPEC_2026-05-06.md`
- `docs/ops/QWEN_BLUEPRINT_LOCAL_INDEX_2026-05-06.md`

COMMS, L1 y coordinacion:

- `COMMS/README.md`
- `docs/developer/CURADOR_SETO_GLOBAL_OPERATING_CONTRACT_2026-05-05.md`
- `docs/language/L1_PROGRAMMER_AGENT_PROTOCOL.md`
- `docs/language/L1_COMMS_DIFF_CONSUMER.md`
- `docs/observacionismo/COMMS_L1_ACTIONGATE_BRIDGE_V0_1.md`
- `COMMS/handoffs/2026-05-06-agent-city-coordination.md`
- `COMMS/handoffs/2026-05-05-claudio-local-agent-seto.md`
- `COMMS/agents_state/claudio-local-agent.json`
- `COMMS/agents_state/claudio-local-autonomy.json`
- `COMMS/agents_state/wabi-sabi-sentido-comun.json`

Matrix, Harness y Mission Control:

- `docs/matrix/01_architecture.md`
- `docs/matrix/05_delegation_protocol.md`
- `docs/matrix/11_mission_control_bridge.md`
- `docs/ops/MISSION_CONTROL_COMMS_LOCAL_VIEW_WORKPACK_2026-05-06.md`
- `docs/ops/MISSION_CONTROL_COMMS_STATE_2026-05-06.md`
- `-=MEDIOEVO=-/-=LIBROS/claudio/.agents/harness/claudio_harness_manifest.json`
- `-=MEDIOEVO=-/-=LIBROS/claudio/.agents/skills/claudio-observacionismo-harness/SKILL.md`

## Lectura Por Carril

### Wabi-Sabi

Estado observado: ya es funcional, local-first y sin nube obligatoria. Tiene:

- CLI `wabi`;
- modo `auto`;
- ventana persistente;
- respuesta local inmediata;
- Codex CLI read-only en background;
- fallback `dry-run`;
- `ActionGate`;
- `ObservationEnvelope`;
- `BridgeExecutor`;
- `WitnessLog` SQLite con hash-chain;
- `ProviderOrchestrator`;
- `BlueprintPolicyLoader`;
- `JobStore`;
- programacion acotada con `--apply --target`.

Valor: es el punto donde pueden converger entorno, comunicacion y programacion.

Riesgo: si se convierte en agente autonomo amplio antes de tener snapshot de
entorno y ledger comun, puede duplicar decisiones o saltar gates.

Conclusion: Wabi debe ir primero, pero como `control plane`, no como modelo ni
como UI.

### Entorno

Estado observado: el host esta `JAMMING/BLOCK`. La telemetria existe, pero esta
dispersa entre:

- `host_observacionista`;
- `pending_review`;
- Wabi blueprint policy;
- COMMS agents state;
- Qwen health/gate reports;
- Mission Control state docs.

Valor: sin entorno consolidado, cualquier decision de programacion o modelo es
fragil.

Riesgo: si se implementa como dashboard antes que como API/JSON local, se crea
superficie visual sin contrato.

Conclusion: el primer modulo dentro de Wabi debe ser `EnvironmentSnapshot`.

### COMMS

Estado observado: COMMS valida `PASS`, tiene schemas, inbox/outbox/topics,
handoffs y agentes. Mission Control ya puede leer COMMS localmente.

Valor: es el bus de coordinacion real entre agentes. Evita que cada agente
actue desde su memoria privada.

Riesgo: si Wabi escribe COMMS sin envelope o sin separar `REVIEW/BLOCK`, se
rompe el contrato append-only.

Conclusion: COMMS no necesita reemplazo; necesita un bridge desde Wabi que lea
estado y escriba solo mensajes append-only con `ObservationEnvelope`.

### Programacion

Estado observado: hay tres niveles:

- Wabi `--apply --target` para `.py` acotado;
- L1 Programmer Workpack, que nunca aplica patch;
- Claudio No-LLM, con evidencia lista pero `wide` degradado por host gate.

Valor: programar es el actuador de mayor impacto.

Riesgo: bajo host `BLOCK`, programar amplio es la ruta con mas blast radius.

Conclusion: no debe ser lo primero de forma aislada. Debe ser el cuarto paso:
despues de snapshot, COMMS y ledger.

## Matriz De Decision

Escala: 1 bajo, 5 alto.

| tecnologia | impacto transversal | readiness | riesgo bajo host BLOCK | desbloquea otras capas | prioridad |
|---|---:|---:|---:|---:|---:|
| Wabi-Sabi control plane | 5 | 5 | 4 | 5 | 1 |
| EnvironmentSnapshot en Wabi | 5 | 4 | 5 | 5 | 2 |
| COMMSBridge Wabi append-only | 5 | 4 | 4 | 5 | 3 |
| DecisionLog adapter sobre TaskManager/WitnessLog | 4 | 3 | 4 | 5 | 4 |
| Programmer dry workpack/scoped patch | 5 | 4 | 2 | 4 | 5 |
| Mission Control UI | 3 | 4 | 3 | 3 | 6 |
| Qwen/Ollama modelo local | 3 | 2 | 1 | 2 | 7 |
| Symphony/daemon/harness externo | 3 | 2 | 1 | 2 | 8 |

Lectura: Wabi ya existe y tiene la mayor superficie util; el trabajo que mas
ayuda primero es convertirlo en el coordinador que ve entorno, COMMS y tareas
antes de programar.

## Primera Implementacion Recomendada

Nombre de workpack:

```text
WABI_ENV_COMMS_CONTROL_PLANE_V0_2
```

Objetivo:

```text
Hacer que Wabi-Sabi pueda responder "que conviene hacer ahora" leyendo estado
real del entorno, COMMS y pending, sin usar modelos pesados ni ejecutar cambios.
```

Alcance tecnico:

1. `EnvironmentSnapshot`
   - lee `qa_artifacts/pending/pending_review_latest.json`;
   - lee `claudio/runtime/host_observacionista/latest_report.json`;
   - lee `COMMS/agents_state/*.json`;
   - llama o consume resultado de `COMMS/tools/validate_seto_comms.py`;
   - incorpora `ProviderOrchestrator.status()`;
   - produce JSON en `apps/local/wabi-sabi/runtime/outputs`.

2. `COMMSBridge`
   - lectura de agentes, gates, may_touch y must_not_touch;
   - validator COMMS desde Wabi-Sabi;
   - plan de append COMMS queda implementado como workpack;
   - escritura append-only real queda bloqueada por gate;
   - ningun append si `ActionGate=BLOCK`.

3. `DecisionLogAdapter`
   - consumidor real para el wrapper antes diferido;
   - registra decision, evidencia, gate, snapshot hash y siguiente accion;
   - se apoya en TaskManager compatible y `WitnessLog`;
   - no reemplaza `DECISIONS.md`, lo vuelve consultable por runtime.

4. `ProgrammerWorkpack`
   - Wabi compila una propuesta seca;
   - no aplica patch salvo `--apply --target` explicito y ruta segura;
   - para multiarchivo, produce workpack `REVIEW`, no escritura.

Validacion minima cuando host no este `BLOCK`:

```powershell
cd apps\local\wabi-sabi
python -m compileall -q wabi_sabi tests
python -m pytest -q
.\wabi.cmd auto /status --json
.\wabi.cmd bridge-plan "clasifica pendientes y genera siguiente accion" --json
python ..\..\COMMS\tools\validate_seto_comms.py --json
```

## Orden De Ejecucion

### Paso 0 - Cerrado bajo host BLOCK

- Mantener bloqueadas acciones externas, modelos pesados, daemons,
  publicacion, append COMMS y programacion amplia.
- No ejecutar Qwen pesado, aliases Ollama, benchmarks, daemon ni programacion
  amplia.
- Usar este reporte y los artefactos Wabi como handoff.

### Paso 1 - Cerrado localmente

- Definido e implementado `wabi.environment_snapshot.v0_2`.
- Definido e implementado `wabi.comms_state.v0_2`.
- Runtime real tocado solo en `apps/local/wabi-sabi/runtime/outputs` y
  `runtime/logs`.

### Paso 2 - Cerrado localmente

- Implementado `EnvironmentSnapshot` y tests.
- Comando disponible: `wabi env-status --json`.
- No escribe COMMS.

### Paso 3 - Cerrado localmente como read-only

- Implementado `COMMSBridge` read-only.
- Validado contra COMMS validator.
- Comando disponible: `wabi comms-state --json`.

### Paso 4 - Cerrado localmente como DecisionLog read-only

- Implementado `DecisionLogAdapter`.
- Comando disponible:
  `wabi decide "que tecnologia implementar primero" --json`.
- Append COMMS opt-in queda pendiente y bloqueado hasta gate/rollback claro.

### Paso 5 - Solo con rollback y tests

- Preparado `comms-append-plan`; append real espera gate.
- Preparado `programmer-workpack` multiarchivo como `PLAN_ONLY`.
- Mantener multiarchivo como `REVIEW_PATCH_PLAN_ONLY`.

## Que No Va Primero

- Qwen/Ollama: host actual lo bloquea; ademas la documentacion dice que Ollama
  es backend opcional, no arquitectura.
- Symphony/daemon: requiere preflight y variables externas; no es base actual.
- Mission Control UI: ya lee COMMS; antes de UI falta contrato unificado de
  decision.
- Publicacion/redes/Gumroad/GitHub: no resuelve la capacidad interna y esta
  gated.
- Dashboard nuevo: duplica Mission Control y aumenta superficie sin resolver
  decisiones.

## Criterio De Cierre

La tecnologia queda lista para implementar cuando exista una prueba local que
demuestre:

```text
prompt amplio
  -> Wabi lee entorno
  -> Wabi lee COMMS
  -> Wabi clasifica riesgo
  -> Wabi registra decision
  -> Wabi produce workpack
  -> no escribe codigo sin gate
  -> COMMS validator PASS
```

Resultado esperado:

```text
Wabi-Sabi deja de ser solo CLI/agente local y se vuelve el sistema operativo de
decision para entorno, comunicacion y programacion.
```
