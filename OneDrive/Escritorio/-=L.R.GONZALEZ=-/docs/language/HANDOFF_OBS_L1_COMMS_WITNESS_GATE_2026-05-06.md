# Handoff OBS L1 COMMS Witness Gate 2026-05-06

Status: `LOCAL_REVIEW_ONLY`

Fingerprint: `OBS_L1_COMMS_WITNESS_GATE_FIX_2026-05-06_363b70fb`

## Resumen

Se congelo la especificacion v0.1 del lenguaje observacionista y se conecto
L1 con `ObservationEnvelope`, `ActionGate`, workpack seco para agente
programador, COMMS append-only y consumidor de diff read-only.

El carril no habilita escritura automatica. `actuar` sigue siendo propuesta
gated. Cualquier patch real requiere otro `ActionGate` explicito, rollback,
diff concreto y pruebas.

## Avance Documentado

Artefactos de especificacion:

- `docs/language/OBS_LANGUAGE_V0_1.md`
- `docs/language/L1_TO_OBSERVATION_ENVELOPE.md`
- `docs/language/L1_PROGRAMMER_AGENT_PROTOCOL.md`
- `docs/language/L1_COMMS_DIFF_CONSUMER.md`

Artefactos de laboratorio:

- `research/observacionismo-lab/l1_to_envelope.py`
- `research/observacionismo-lab/l1_programmer_workpack.py`
- `research/observacionismo-lab/l1_comms_diff_consumer.py`
- `research/observacionismo-lab/schemas/l1_programmer_workpack.schema.json`
- `research/observacionismo-lab/schemas/l1_comms_diff_plan.schema.json`
- `research/observacionismo-lab/examples/*.obs`
- `research/observacionismo-lab/tests/test_l1_to_envelope.py`
- `research/observacionismo-lab/tests/test_l1_programmer_workpack.py`
- `research/observacionismo-lab/tests/test_l1_comms_diff_consumer.py`

Correccion de gate/WitnessLog:

- `tools/release/curador_automation.py`
- `tests/release/test_curador_automation.py`
- `qa_artifacts/witness_log/curador_seto_witnesslog.jsonl`

## Contrato Actual

Flujo canonico:

```text
L1 .obs
  -> ObservationEnvelope
  -> ActionGate
  -> Programmer Workpack
  -> COMMS append-only message
  -> Read-only diff consumer
  -> Dry diff plan
  -> future human ActionGate before apply
```

Reglas duras:

- `programmer_agent.may_execute=false`
- `patch_policy.may_apply_patch=false`
- `patch_policy.no_auto_write=true`
- `diff_plan.dry_run=true`
- `diff_plan.applied=false`
- `diff_plan.may_apply_patch=false`
- `diff_plan.application_gate.status=REVIEW`
- `WitnessLog.action_gate` solo usa `APPROVE`, `REVIEW` o `BLOCK`
- `APPROVE_LOCAL` puede existir solo como marcador local dentro de `summary`

## Riesgos Resueltos

1. Mensaje COMMS L1 validado solo por validador interno.
   - Resuelto con test contra `core.agent_comms.validate_message`.

2. Consumidor COMMS diff usaba pertenencia al repo por prefijo textual.
   - Resuelto con `Path.resolve().relative_to()`.

3. Target existente pero no archivo podia quedar listo sin propuesta aplicable.
   - Resuelto con blocker `target_not_file`.

4. `COMMS/tools/validate_seto_comms.py` fallaba por tail de WitnessLog con
   `action_gate=APPROVE_LOCAL`.
   - Resuelto sin editar historia: se agrego evento append-only
     `curador_witness_action_gate_normalized`.
   - `curador_automation.py absorb` ahora escribe `action_gate=REVIEW` y
     conserva `APPROVE_LOCAL` solo en `summary.local_gate`.

## Evidencia

Validaciones ejecutadas:

```text
python -m pytest research\observacionismo-lab\tests -q
34 passed

python -m pytest tests\test_agent_comms.py tests\test_nollm_programmer.py tests\test_observacionismo_workpack_materializer.py -q
19 passed

python -m pytest tests\release\test_curador_automation.py -q
11 passed

python COMMS\tools\validate_seto_comms.py --json
PASS, errors=[]
```

Secret scans focalizados:

```text
python tools\release\scan_secrets.py --path docs\language --json
count_reported=0

python tools\release\scan_secrets.py --path research\observacionismo-lab --json
count_reported=0
```

Observacion:

- `scan_secrets.py --path tools\release\curador_automation.py` y el test
  asociado reportan `denylist path` por politica de tooling de release, no por
  valor secreto impreso.

WitnessLog tail:

```text
event_type=curador_witness_action_gate_normalized
event_hash=363b70fbf9c09ec25c72ff055781267f5bead4103a3ed62f549c7fef6eb81d9f
action_gate=REVIEW
hash_match=true
```

## Estado De Git Observado

No hay staging accidental:

```text
git diff --cached --name-status
<empty>
```

El carril L1 aparece como nuevo/no stageado:

```text
docs/language/
research/observacionismo-lab/examples/
research/observacionismo-lab/l1_comms_diff_consumer.py
research/observacionismo-lab/l1_programmer_workpack.py
research/observacionismo-lab/l1_to_envelope.py
research/observacionismo-lab/schemas/
research/observacionismo-lab/tests/test_l1_comms_diff_consumer.py
research/observacionismo-lab/tests/test_l1_programmer_workpack.py
research/observacionismo-lab/tests/test_l1_to_envelope.py
```

## Limites

No se hizo:

- publicacion externa;
- push;
- deploy;
- login;
- red externa;
- descarga;
- borrado;
- movimiento de archivos privados;
- cambios en pesos, alias o modelos;
- mezcla con RPG/TCG privado;
- aplicacion real de patches desde L1.

## Handoff

Para el siguiente agente:

1. Tratar `docs/language/OBS_LANGUAGE_V0_1.md` como especificacion v0.1
   congelada.
2. Consumir L1 con:

```powershell
python research\observacionismo-lab\l1_programmer_workpack.py research\observacionismo-lab\examples\gated_patch.obs --pretty
```

3. Si se usa COMMS, hacerlo solo con `--comms-inbox` explicito y append-only.
4. Consumir COMMS con:

```powershell
python research\observacionismo-lab\l1_comms_diff_consumer.py .\COMMS\inbox\claudio-local-agent.jsonl --repo-root . --pretty
```

5. No aplicar diff generado por L1. El output es plan seco.
6. Antes de cualquier escritura real, exigir:

```text
ActionGate APPROVE especifico
rollback
diff concreto
test focal
WitnessLog/COMMS de resultado
```

Siguiente paso seguro:

- Conectar el consumidor read-only con el agente programador No-LLM en modo
  `diff_review`, manteniendo `application_gate=REVIEW`.

Bloqueado por gate:

- `apply-gated` sobre planes derivados de L1;
- publicacion;
- red;
- cuentas externas;
- descargas;
- limpieza destructiva;
- private game/TCG.

## Wabi-Sabi

Wabi-Sabi se mantiene como nodo sensorial-cognitivo de control
observacionista. No es cerebro central, AGI completa ni autoridad absoluta.
Su rol en este carril es revisar evidencia, gates, R residual y coherencia
antes de compilar handoff o instrucciones correctivas.
