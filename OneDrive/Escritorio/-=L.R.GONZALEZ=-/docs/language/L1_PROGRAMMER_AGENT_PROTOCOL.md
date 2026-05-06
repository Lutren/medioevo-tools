# L1 Programmer Agent Protocol v0.1

Status: `DRY_WORKPACK_CONTRACT`

Adapter: `research/observacionismo-lab/l1_programmer_workpack.py`

Schema: `research/observacionismo-lab/schemas/l1_programmer_workpack.schema.json`

## Objetivo

Conectar L1 con un agente programador sin convertir `actuar` en escritura
automatica.

El resultado es un workpack seco: describe intencion, evidencia, gate, alcance,
riesgos y validaciones. No ejecuta patch, shell, red, login, publicacion, borrado
ni movimiento de archivos.

## Relacion Con Claudio No-LLM

Patrones existentes leidos:

- `tools/claudio_nollm_agent.py`
- `core.nollm_programmer.agent`
- `tests/test_nollm_programmer.py`
- `tools/observacionismo_workpack_materializer.py`

El protocolo v0.1 no importa esos modulos ni modifica Claudio. Solo crea un
artefacto compatible conceptualmente:

```text
L1 -> ObservationEnvelope -> ActionGate -> Programmer Workpack
```

## Workpack Minimo

```json
{
  "schema": "observacionismo.l1_programmer_workpack.v0_1",
  "source_packet_fingerprint": "OBS_LANGUAGE_L1_ENVELOPE_V01_2026-05-06_<hash>",
  "programmer_agent": {
    "recommended_agent": "claudio-local-agent",
    "mode": "dry_workpack_only",
    "may_execute": false
  },
  "status": "REVIEW_PATCH_PLAN_ONLY",
  "intent": "Proponer un patch local reversible",
  "observation_envelope": {},
  "action_gate": {},
  "proposed_scope": {
    "action": "edit_file:docs/example.md",
    "target_paths": ["docs/example.md"],
    "private_boundary_touched": false,
    "external_boundary_touched": false
  },
  "patch_policy": {
    "may_prepare_patch_plan": true,
    "may_apply_patch": false,
    "requires_action_gate": true,
    "rollback_required_before_apply": true,
    "no_auto_write": true
  }
}
```

## COMMS Opt-In

El CLI puede emitir un mensaje append-only a un inbox COMMS si, y solo si, se
declara `--comms-inbox`.

```powershell
python research\observacionismo-lab\l1_programmer_workpack.py research\observacionismo-lab\examples\gated_patch.obs --comms-inbox .\COMMS\inbox\claudio-local-agent.jsonl --pretty
```

Reglas:

- sin `--comms-inbox`, no hay escritura COMMS;
- el mensaje incluye `ObservationEnvelope`;
- el mensaje embebe el workpack seco;
- `routing.does_not_execute=true`;
- `routing.append_only=true`;
- el consumidor debe revisar `ActionGate`;
- `may_apply_patch=false` sigue siendo obligatorio;
- el mensaje debe pasar `core.agent_comms.validate_message`.

## Consumidor De Diff Read-Only

El siguiente paso seguro es leer el inbox COMMS y producir un plan de diff seco
con:

```text
research/observacionismo-lab/l1_comms_diff_consumer.py
```

Contrato:

- lee mensajes `observacionismo.l1_programmer_workpack.comms_message.v0_1`;
- observa targets locales y calcula sha256 cuando es seguro;
- produce schema `observacionismo.l1_comms_diff_plan.v0_1`;
- mantiene `dry_run=true`;
- mantiene `applied=false`;
- mantiene `may_apply_patch=false`;
- mantiene `application_gate.status=REVIEW`;
- bloquea acciones externas y rutas inseguras.

Documento canonico:

```text
docs/language/L1_COMMS_DIFF_CONSUMER.md
```

## Estados

| Estado | Significado | Escritura |
|---|---|---|
| `READY_READ_ONLY` | Programa document-only con evidencia y checks OK. | No escribe. |
| `REVIEW_PATCH_PLAN_ONLY` | Hay intencion de patch local con target. | Puede preparar plan, no aplicar. |
| `REVIEW_MISSING_EVIDENCE` | Falta evidencia declarada. | No escribe. |
| `HANDOFF_REVIEW` | Handoff a otro agente/control node. | No escribe. |
| `BLOCKED_BY_ACTION_GATE` | Accion externa o gate BLOCK. | No escribe. |

## Reglas Duras

- `patch_policy.may_apply_patch` siempre debe ser `false`.
- `patch_policy.no_auto_write` siempre debe ser `true`.
- `programmer_agent.may_execute` siempre debe ser `false`.
- Operaciones prohibidas siempre presentes:
  `apply_patch`, `delete`, `download`, `external_network`, `git_push`,
  `login`, `move_files`, `publish`, `run_shell`, `store_credentials`.
- External action produce `BLOCKED_BY_ACTION_GATE`.
- Missing evidence produce `REVIEW_MISSING_EVIDENCE`.
- Patch local produce `REVIEW_PATCH_PLAN_ONLY`, no escritura.

## Falsadores

Implementados en:

```text
research/observacionismo-lab/tests/test_l1_programmer_workpack.py
```

Falsan el protocolo si:

1. un workpack permite `may_apply_patch=true`;
2. una accion externa no queda `BLOCKED_BY_ACTION_GATE`;
3. falta de evidencia no queda `REVIEW_MISSING_EVIDENCE`;
4. patch local se aplica en lugar de producir plan seco;
5. el CLI escribe un workpack invalido.
6. el mensaje COMMS embebido permite `may_apply_patch=true`.
7. el CLI escribe COMMS sin `--comms-inbox`.
8. el consumidor COMMS genera un plan aplicable o con gate distinto de `REVIEW`.
9. un directorio target o sibling con prefijo parecido al repo produce `DIFF_PLAN_READY`.
10. el mensaje COMMS L1 no pasa el validador canonico `core.agent_comms`.

## Validacion

```powershell
python -m pytest research\observacionismo-lab\tests -q
python research\observacionismo-lab\l1_programmer_workpack.py research\observacionismo-lab\examples\gated_patch.obs --pretty
```

Resultado esperado del ejemplo `gated_patch.obs`:

```text
status=REVIEW_PATCH_PLAN_ONLY
may_prepare_patch_plan=true
may_apply_patch=false
target_paths=["docs/example.md"]
```

Smoke COMMS temporal:

```text
message_type=L1_PROGRAMMER_WORKPACK_READY
recipient=claudio-local-agent
routing.append_only=true
routing.does_not_execute=true
```

## Evidencia 2026-05-06

```text
python -m pytest research\observacionismo-lab\tests -q
34 passed

python -m pytest tests\test_observabit.py tests\test_nollm_programmer.py tests\test_observacionismo_workpack_materializer.py -q
19 passed
```

Smoke:

```text
gated_patch.obs -> OBS_L1_PROGRAMMER_WORKPACK_V01_2026-05-06_3373e2b1c810
status=REVIEW_PATCH_PLAN_ONLY
may_prepare_patch_plan=true
may_apply_patch=false
target_paths=docs/example.md
```
