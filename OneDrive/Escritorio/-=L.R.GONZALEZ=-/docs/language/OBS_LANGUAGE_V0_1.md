# Observacionista Language v0.1

Status: `LOCAL_RESEARCH_DRAFT_FROZEN_V0_1`

Date: `2026-05-06`

## Proposito

El lenguaje observacionista es una capa verificable entre teoria, agente,
ActionGate, DUAT abstracto y codigo operativo. Su funcion es reducir R o
aumentar evidencia antes de que otro sistema actue.

No es otro Python. No compite con Python, TypeScript, Godot, NASM ni motores
de juego. Es un IR minimo para declarar observacion, evidencia, verificacion,
propuesta de accion y handoff.

## No-Proposito

- No es lenguaje general.
- No tiene macros complejas.
- No ejecuta red.
- No publica.
- No borra.
- No descarga.
- No automatiza login.
- No escribe patches automaticamente.
- No reemplaza DUAT privado.
- No importa ZIP/TXT crudos de Downloads como canon.
- No toca RPG/TCG privado.

## Inventario Tecnico Encontrado

| Area | Archivo | Estado |
|---|---|---|
| L0 bit VM | `research/observacionismo-lab/obs_bit_machine.py` | VM local de 8 opcodes: `NOP`, `OBS`, `ZERO`, `ONE`, `XOR`, `AND`, `OUT`, `HALT`. |
| L1 IR | `research/observacionismo-lab/obs_l1_ir.py` | Parser de cinco verbos: `OBSERVAR`, `DOCUMENTAR`, `VERIFICAR`, `ACTUAR`, `HANDOFF`. |
| Tests L0/L1 | `research/observacionismo-lab/tests` | Prueban ensamblado, inferencia XOR, checks y handoff. |
| Adaptador v0.1 | `research/observacionismo-lab/l1_to_envelope.py` | Nuevo adaptador L1 -> `ObservationEnvelope` -> `ActionGate`. |
| Workpack programador | `research/observacionismo-lab/l1_programmer_workpack.py` | Nuevo adaptador L1 packet -> workpack seco para agente programador. |
| Schema workpack | `research/observacionismo-lab/schemas/l1_programmer_workpack.schema.json` | Contrato estatico: `may_execute=false`, `may_apply_patch=false`, `no_auto_write=true`. |
| COMMS opt-in | `l1_programmer_workpack.py --comms-inbox` | Emite mensaje append-only con `ObservationEnvelope` y workpack seco, solo si se solicita; pasa `core.agent_comms.validate_message`. |
| Consumidor COMMS diff | `research/observacionismo-lab/l1_comms_diff_consumer.py` | Lee workpacks COMMS y produce planes de diff secos, sin aplicar patches. |
| Schema diff plan | `research/observacionismo-lab/schemas/l1_comms_diff_plan.schema.json` | Contrato estatico: `dry_run=true`, `applied=false`, `may_apply_patch=false`, `application_gate.status=REVIEW`. |
| Ejemplos | `research/observacionismo-lab/examples/*.obs` | Cinco programas pequenos con evidencia, gate, handoff y falsadores. |
| Claudio ObservaBit | `-=MEDIOEVO=-/-=LIBROS/claudio/core/observabit.py` | Bytecode compacto de control: `opcode3 evidence1 write1 gate2 handoff1`. |
| Compiler Claudio | `-=MEDIOEVO=-/-=LIBROS/claudio/tools/observabit_compile.py` | Compila IR de Claudio a ObservaBit sin llamar modelos ni modificar pesos. |
| COMMS schemas | `COMMS/schemas/*.schema.json` | `ObservationEnvelope`, `ActionGate`, `WitnessLog`. |
| obsai-core | `packages/open-dev/obsai-core` | Gate/residue/evidence primitives para capa publica-safe. |

## Capas

### L0: maquina de bits/bytecode

L0 es el bytecode auditable.

Forma estable del laboratorio:

```text
opcode3 x3 y2
```

OpCodes:

| Opcode | Nombre | Funcion |
|---:|---|---|
| 0 | `NOP` | No-op. |
| 1 | `OBS` | Observa bit de memoria. |
| 2 | `ZERO` | Escribe 0 local en memoria VM. |
| 3 | `ONE` | Escribe 1 local en memoria VM. |
| 4 | `XOR` | Opera XOR local. |
| 5 | `AND` | Opera AND local. |
| 6 | `OUT` | Documenta salida. |
| 7 | `HALT` | Cierra ejecucion local. |

Bytecode estable de ejemplo:

```text
OBS 0 / XOR 0 1 / OUT 0 / HALT
[32, 129, 192, 224]
```

Claudio ObservaBit usa otra forma compatible de control:

```text
opcode3 evidence1 write1 gate2 handoff1
```

Ese formato no reemplaza L0 del laboratorio; sirve como control compacto para
Claudio/Qwen/host gate.

### L1: IR observacionista

Verbos canonicos v0.1:

| Verbo | Sentido | Efecto |
|---|---|---|
| `observar` | Leer estado o input. | Debe crear rastro observable. |
| `documentar` | Emitir evidencia o artefacto. | Debe aumentar evidencia. |
| `verificar` | Evaluar falsador/check. | Debe reducir R o generar REVIEW. |
| `actuar` | Proponer accion. | Nunca ejecuta accion externa por si sola. |
| `handoff` | Cerrar y transferir estado. | Debe producir snapshot/handoff. |

Forma aceptada por el laboratorio:

```text
OBSERVAR bit 0
ACTUAR xor 0 1
DOCUMENTAR bit 0
VERIFICAR output == [1]
HANDOFF
```

Metadata minima en comentarios:

```text
# claim: ...
# evidence: ...
# falsifier: ...
# risk: ...
# action: ...
# gate: APPROVE|REVIEW|BLOCK
# handoff: ...
```

La metadata no agrega macros. Solo documenta claim/evidencia/gate para el
adaptador.

### L2: DSL humano compacto

L2 todavia no es parser general. En v0.1 es solo forma humana compacta para
escribir L1 con comentarios de claim/evidencia. Cualquier expansion futura debe
compilar a L1 y mantener falsadores.

## Tipos De Evidencia

- `source_path`: archivo local, contrato, schema o handoff.
- `sha256`: hash del script L1.
- `bytecode`: L0 producido.
- `assembly`: ensamblado legible.
- `checks`: resultados de `VERIFICAR`.
- `falsifiers`: condiciones que invalidan el claim.
- `risk_flags`: faltas de evidencia, accion externa, write intent, handoff.

## Gates

Estados:

- `APPROVE`: programa local, evidencia declarada, checks pasan, sin accion de
  escritura ni externa.
- `REVIEW`: falta evidencia, hay write intent local, handoff, o checks fallan.
- `BLOCK`: accion externa, publicacion, red, descarga, login, borrado,
  private boundary o gate humano `BLOCK`.

Regla:

```text
ACTUAR nunca ejecuta. ACTUAR solo propone y deriva ActionGate.
```

## Relacion Con ActionGate

`research/observacionismo-lab/l1_to_envelope.py` compila un programa L1 a:

```json
{
  "type": "ObservationEnvelope",
  "claim": "...",
  "evidence": ["..."],
  "risk": "...",
  "residue": "...",
  "action": "...",
  "gate_required": true,
  "handoff": {}
}
```

Luego deriva un `ActionGate` local:

- missing evidence -> `REVIEW`;
- write intent -> `REVIEW`;
- handoff -> `REVIEW`;
- external action -> `BLOCK`;
- valid document-only -> `APPROVE`.

## Relacion Con DUAT

DUAT queda como interfaz abstracta. L1 puede describir observaciones,
evidencia, falsadores y handoffs hacia DUAT, pero no toca DUAT privado ni
absorbe implementaciones internas.

## Relacion Con Agente Programador

El agente programador puede consumir:

- `ObservationEnvelope`;
- `ActionGate`;
- bytecode/assembly;
- falsadores;
- risk flags;
- handoff target.

El adaptador `l1_programmer_workpack.py` produce un workpack seco con:

- `may_prepare_patch_plan`;
- `may_apply_patch=false`;
- `no_auto_write=true`;
- `forbidden_operations`;
- validacion del workpack.

No debe tratar L1 como permiso de escritura. Cualquier patch real requiere otro
ActionGate explicito, rollback y pruebas.

## Wabi-Sabi

Wabi-Sabi no es cerebro central ni AGI completa. En este lenguaje opera como
nodo sensorial-cognitivo de control: observa, deconstruye, recompila, traduce,
delegada, revisa gates y compila output final. No actua sin ActionGate.

## Reglas De Seguridad

1. Cada instruccion debe reducir R o aumentar evidencia.
2. Web, red, publicacion, login, descarga y borrado son `BLOCK` por defecto.
3. Escritura local es `REVIEW` salvo gate explicito futuro.
4. Falta de evidencia es `REVIEW`.
5. `HANDOFF` cierra el programa; no hay pasos posteriores.
6. L1 no crea autoridad sobre sistema, usuario o developer.
7. El bytecode y el envelope deben ser reproducibles y hasheables.
8. No usar el lenguaje para esconder acciones externas dentro de metadata.

## Validacion Local

Comandos ejecutados:

```powershell
python -m pytest research\observacionismo-lab\tests -q
python -m pytest tests\test_observabit.py -q
python -m py_compile research\observacionismo-lab\l1_to_envelope.py research\observacionismo-lab\obs_l1_ir.py research\observacionismo-lab\obs_bit_machine.py
```

Resultados observados:

```text
research/observacionismo-lab/tests: 13 passed
claudio/tests/test_observabit.py: 6 passed
py_compile: ok
```

Despues de conectar el workpack programador y el consumidor COMMS diff
read-only:

```text
research/observacionismo-lab/tests: 34 passed
claudio focalizado ObservaBit/No-LLM/workpack: 19 passed
```

Smoke del adaptador:

```text
document_task.obs -> APPROVE / CERTEZA / bytecode 32,192,224
blocked_external_action.obs -> BLOCK / blocked_external_action
```
