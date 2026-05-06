# Observacionismo Minimal Machine Language

Status: `LOCAL_RESEARCH_DRAFT`

Fecha: 2026-05-05

Fuentes verificadas:

- Inventario local: `qa_artifacts/observacionismo_language/observacionismo_language_inventory_2026-05-05.md`
- Prototipo local: `research/observacionismo-lab/obs_bit_machine.py`
- Pruebas locales: `research/observacionismo-lab/tests/test_obs_bit_machine.py`

Este documento no convierte texto crudo de Downloads en canon. Extrae una ruta
operativa minima desde los documentos revisados en `Downloads` y `-=PSI=-`.

## Tesis Operativa

La forma mas compacta y coherente de programar con Observacionismo no es crear
otro lenguaje grande. Es separar tres niveles:

| nivel | nombre | funcion |
|---|---|---|
| L0 | bit machine | operaciones observables sobre bits, con traza y residuo |
| L1 | IR observacionista | cinco verbos: observar, documentar, verificar, actuar, handoff |
| L2 | superficie humana | DSL minimo para tareas, gates, evidencias y artefactos |

Regla: si una idea no puede bajar a L1 como verbo con evidencia, o a L0 como
transicion de estado medible, es teoria o comentario, no instruccion.

## Lectura De Las Fuentes

El inventario encontro 275 archivos relevantes: 100 Markdown, 69 TXT, 32 Python,
27 ZIP, 12 CSV, 10 JSON, 9 DOCX, 9 PDF y 7 HTML. Hay 49 grupos de duplicados
exactos, incluyendo copias entre `Downloads` y `-=PSI=-` de OSIT/TUIP, ingenieria
observacionista, paquetes TUI y documentos de deconstruccion.

Los terminos dominantes no apuntan a un lenguaje tradicional completo. Apuntan
a control de estado: `gate`, `psi`, `phi`, `j_c`, `ast`, `eml`,
`witnesslog`, `actiongate`, `lenguaje`, `bit`, `byte`, `compact`.

La conclusion tecnica es estable: el sistema ya converge hacia un IR, no hacia
una sintaxis grande. `# CLAUDIO -- LOCAL CODE AGENT.txt` define ObservaScript
como IR interno con cinco verbos y advierte no convertirlo en lenguaje grande.
Los documentos LCP agregan `@anchor`, `!ASSERT`, `?DISPROVE` y `#AST`, pero esos
comandos solo son validos como hooks o restricciones cuando existe un runtime
que pueda hacerlos cumplir.

## Observacionismo Aplicado A Lenguajes

| familia | valor observacionista | residuo principal | decision |
|---|---|---|---|
| Assembly/bytecode | maxima cercania a estado, costo y side effects | baja ergonomia, alto riesgo humano | usar solo como L0/VM |
| C | control real de memoria y ABI | undefined behavior y seguridad manual | backend o runtime, no superficie diaria |
| Rust | ownership, tipos fuertes, concurrencia mas segura | mas sintaxis y curva | buen runtime si el sistema crece |
| Zig | control explicito, simpleza relativa | ecosistema menor | candidato para runtime pequeno |
| Go | concurrencia simple y builds faciles | abstraccion media, GC | servicios locales y herramientas |
| Python | minima friccion y gran introspeccion | ejecucion dinamica, imports con efectos | prototipos, scanners, gates |
| JavaScript/TypeScript | UI y apps locales | tooling ruidoso | superficies UI, no nucleo |
| SQL | estado declarativo verificable | no expresa acciones generales | evidencia, manifests, queries |
| Lisp/Scheme | homoiconicidad, macros, AST natural | menos ecosistema operativo local | inspiracion para L1/DSL |
| Forth | pila minima, extensible desde palabras | dificil de leer en grande | inspiracion fuerte para L0/L1 |
| Prolog/Datalog | reglas y consultas falsables | control de efectos limitado | validacion, policy, claims |
| Haskell/ML | tipos y pureza | distancia operativa | contratos criticos, no MVP |

Decision pragmatica: Python para el prototipo y pruebas; Rust/Zig despues solo
si el VM deja de ser investigacion y necesita ejecutarse como runtime robusto.

## Ingenieria Observacionista

Una funcion observacionista minima cumple:

1. Recibe estado declarado.
2. Produce una transicion medible.
3. Emite evidencia o no puede actuar.
4. Calcula residuo.
5. Pasa por gate antes de efectos secundarios.
6. Deja traza reproducible.

En codigo, eso significa preferir:

- datos inmutables o copiados antes de mutar;
- funciones pequenas con entradas/salidas explicitas;
- AST/IR antes que prompts largos;
- bytecode o JSON estricto antes que texto ambiguo;
- tests de falsacion antes que narrativa de exito;
- `WitnessLog` y hashes para cambios relevantes.

## Ingenieria Observacionista Inversa

La ruta inversa no empieza preguntando "que quiso decir el autor". Empieza con
IO observado:

1. Observar entradas, salidas, trazas, hashes, tests y errores.
2. Enumerar mecanismos candidatos.
3. Ejecutarlos contra la observacion.
4. Medir residuo.
5. Elegir el programa mas simple que explica la evidencia.
6. Marcar como `INFERENCIA` todo lo que no sea probado por ejecucion.

El prototipo `ObsBitMachine` implementa esta idea para funciones binarias:
observa una tabla de verdad, enumera programas pequenos y elige el menor con
residuo cero.

## L0: Maquina De Bits

El prototipo usa instrucciones de 8 bits:

```text
bbb xxx yy
```

| campo | bits | significado |
|---|---:|---|
| `bbb` | 3 | opcode, 8 operaciones maximas |
| `xxx` | 3 | direccion principal, 0-7 |
| `yy` | 2 | direccion secundaria, 0-3 |

Opcode v0:

| opcode | nombre | efecto |
|---:|---|---|
| 0 | `NOP` | no muta |
| 1 | `OBS x` | observa bit `x` y lo registra en trace |
| 2 | `ZERO x` | pone `mem[x]=0` |
| 3 | `ONE x` | pone `mem[x]=1` |
| 4 | `XOR x y` | `mem[x] = mem[x] xor mem[y]` |
| 5 | `AND x y` | `mem[x] = mem[x] and mem[y]` |
| 6 | `OUT x` | emite `mem[x]` |
| 7 | `HALT` | termina |

No hay loops, filesystem, red, memoria dinamica ni llamadas externas. Eso es
intencional: reduce residuo y hace falsable cada paso.

## L1: IR De Cinco Verbos

El IR humano no debe crecer mas alla de:

```text
OBSERVAR -> DOCUMENTAR -> VERIFICAR -> ACTUAR -> HANDOFF
```

Mapeo a L0:

| L1 | L0 minimo | prueba |
|---|---|---|
| observar | `OBS` | trace contiene bit/estado |
| documentar | `OUT` + hash externo | output reproducible |
| verificar | `XOR`/`AND` + comparacion | residuo medido |
| actuar | mutacion `ZERO`/`ONE`/`XOR`/`AND` | gate previo |
| handoff | `OUT` final + `HALT` | estado cerrado |

### Implementacion L1 Local

El parser local quedo implementado en
`research/observacionismo-lab/obs_l1_ir.py`.

Sintaxis v0:

```text
OBSERVAR bit 0
ACTUAR xor 0 1
DOCUMENTAR bit 0
VERIFICAR output == [1]
VERIFICAR halted == true
VERIFICAR residue <= 0
HANDOFF
```

Salida observada:

- bytecode: `[32, 129, 192, 224]`
- assembly: `OBS 0 0`, `XOR 0 1`, `OUT 0 0`, `HALT 0 0`
- `ObservationEnvelope.action_gate`: `APPROVE` cuando checks pasan
- `ObservationEnvelope.action_gate`: `REVIEW` cuando checks fallan

Esto completa el puente minimo L1 -> L0 sin inflar el lenguaje: `VERIFICAR`
queda fuera del bytecode como check posterior, para que la maquina de bits siga
siendo pequena y falsable.

## Lo Que Se Descarta

- No crear un lenguaje grande tipo Python nuevo.
- No prometer control real de KV-cache/logits si el runtime local no lo expone.
- No mezclar claims de fisica, biologia o conciencia con el lenguaje operativo.
- No importar ZIPs ni TXT crudos: solo patrones con hash, ficha y prueba.

## Siguiente Implementacion

1. Mantener `ObsBitMachine` como L0 local.
2. Conectar el IR a `obsai-core` solo por envelopes y gates, no por copia de
   teoria cruda.
3. Medir `Phi_eff_code` por prueba cerrada: tests verdes nuevos por costo de
   contexto, no lineas generadas.
4. Agregar falsadores: si un programa mas simple explica igual las salidas, la
   explicacion anterior baja de `CERTEZA` a `INFERENCIA`.
