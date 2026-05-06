# L1 COMMS Diff Consumer v0.1

Status: `READ_ONLY_DIFF_PLAN_CONTRACT`

Consumer: `research/observacionismo-lab/l1_comms_diff_consumer.py`

Schema: `research/observacionismo-lab/schemas/l1_comms_diff_plan.schema.json`

## Objetivo

Conectar el mensaje COMMS del workpack L1 con un agente programador sin abrir
escritura automatica.

El consumidor lee un inbox JSONL, filtra mensajes con schema
`observacionismo.l1_programmer_workpack.comms_message.v0_1`, observa los
targets locales y produce planes de diff secos.

No aplica patches. No ejecuta shell. No publica. No usa red. No descarga. No
mueve ni borra archivos. La unica escritura opcional es un JSON de resultado si
se declara `--out`.

## Flujo

```text
L1 .obs
  -> ObservationEnvelope
  -> ActionGate
  -> Programmer Workpack
  -> COMMS append-only message
  -> read-only diff consumer
  -> dry diff plan
  -> future ActionGate humano antes de aplicar
```

## CLI

```powershell
python research\observacionismo-lab\l1_comms_diff_consumer.py .\COMMS\inbox\claudio-local-agent.jsonl --repo-root . --pretty
```

Salida a archivo local controlado:

```powershell
python research\observacionismo-lab\l1_comms_diff_consumer.py .\COMMS\inbox\claudio-local-agent.jsonl --repo-root . --out .\qa_artifacts\l1_diff_plan.json --pretty
```

## Estados

| Estado | Condicion | Accion permitida |
|---|---|---|
| `DIFF_PLAN_READY` | Workpack local de patch-plan, targets seguros y existentes. | Preparar propuesta manual. No aplicar. |
| `READ_ONLY_NO_DIFF` | Programa document-only sin diff requerido. | Registrar lectura. No aplicar. |
| `REVIEW_NOT_DIFFABLE` | Falta target, evidencia, ruta insegura o workpack invalido. | Revisar y corregir evidencia/gate. |
| `BLOCKED_BY_ACTION_GATE` | Accion externa o gate BLOCK. | Bloquear. |

## Contrato Duro

Todo plan debe mantener:

```json
{
  "dry_run": true,
  "applied": false,
  "may_apply_patch": false,
  "application_gate": {
    "status": "REVIEW"
  }
}
```

Operaciones prohibidas obligatorias:

```text
apply_patch
delete
download
external_network
git_push
login
move_files
publish
run_shell
store_credentials
```

## Observacion De Targets

Para cada ruta declarada en el workpack, el consumidor calcula:

- ruta relativa segura;
- pertenencia al repo;
- existencia;
- tipo archivo;
- marca de boundary privado;
- marca de path tipo secreto;
- sha256 si el archivo puede leerse;
- permiso de lectura.

Rutas absolutas, `..`, secretos, private boundary y targets inexistentes no son
diffables.

La pertenencia al repo se valida por `Path.resolve().relative_to()`, no por
prefijo de string. Esto bloquea escapes por rutas resueltas que solo comparten
un prefijo textual con el repo. Un target que existe pero no es archivo produce
`target_not_file` y queda en `REVIEW_NOT_DIFFABLE`.

## Relacion Con ActionGate

El consumidor nunca convierte `REVIEW` en `APPROVE`.

Aunque un plan sea `DIFF_PLAN_READY`, su `application_gate.status` permanece
`REVIEW`. Aplicar un patch real requiere otro paso separado con:

- gate humano explicito;
- rollback;
- diff concreto;
- pruebas de modulo;
- WitnessLog o COMMS append-only de resultado.

## Falsadores

Implementados en:

```text
research/observacionismo-lab/tests/test_l1_comms_diff_consumer.py
```

Falsan el contrato si:

1. el consumidor aplica o permite aplicar patch;
2. una accion externa no queda bloqueada;
3. un target inexistente produce plan listo;
4. un directorio target produce plan listo;
5. un sibling con prefijo parecido al repo pasa como `within_repo`;
6. un inbox sin mensajes genera acciones;
7. el validador acepta `may_apply_patch=true`;
8. el CLI escribe algo que no sea resultado seco;
9. el schema deja de exigir `application_gate.status=REVIEW`.

## Evidencia 2026-05-06

Validacion esperada despues de la conexion completa:

```text
python -m pytest research\observacionismo-lab\tests -q
34 passed
```

El consumidor fue probado contra COMMS temporal. No se escribio en `COMMS/`
real durante la validacion. El mensaje L1 previo al consumo tambien pasa
`core.agent_comms.validate_message`.
