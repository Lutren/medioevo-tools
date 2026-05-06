# Observacionismo Language Downloads/PSI Intake

Status: `LOCAL_REVIEW_CONTINUE_WITH_BOUNDARY`

Fecha: 2026-05-05

## Fuentes

| fuente | ruta | decision |
|---|---|---|
| Downloads | `C:\Users\L-Tyr\Downloads` | `KEEP_GATED_SOURCE` |
| PSI | `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-` | `KEEP_CANON_REVIEW_BOUNDARY` |

## Evidencia Generada

| artefacto | uso |
|---|---|
| `qa_artifacts/observacionismo_language/observacionismo_language_inventory_2026-05-05.json` | inventario completo con hashes, encabezados, terminos, duplicados y ZIP manifests |
| `qa_artifacts/observacionismo_language/observacionismo_language_inventory_2026-05-05.md` | resumen humano del inventario |
| `docs/developer/OBSERVACIONISMO_MINIMAL_MACHINE_LANGUAGE_2026-05-05.md` | sintesis tecnica y ruta de lenguaje minimo |
| `research/observacionismo-lab/obs_bit_machine.py` | prototipo L0 de maquina de bits |
| `research/observacionismo-lab/tests/test_obs_bit_machine.py` | pruebas del prototipo |
| `research/observacionismo-lab/obs_l1_ir.py` | parser L1 de cinco verbos hacia bytecode L0 y envelope |
| `research/observacionismo-lab/tests/test_obs_l1_ir.py` | pruebas del parser L1 |
| `qa_artifacts/observacionismo_language/obs_bit_machine_pytest_2026-05-05.txt` | evidencia de pytest: 3 passed |
| `qa_artifacts/observacionismo_language/obs_bit_machine_demo_2026-05-05.json` | demo de bytecode y trazas |
| `qa_artifacts/observacionismo_language/obs_l1_ir_pytest_2026-05-05.txt` | evidencia de pytest: 7 passed |
| `qa_artifacts/observacionismo_language/obs_l1_ir_demo_2026-05-05.json` | demo L1 con bytecode, checks y ObservationEnvelope |

## Verificacion

- `python -m pytest research\observacionismo-lab\tests -q` -> `3 passed`.
- `python research\observacionismo-lab\obs_bit_machine.py` -> bytecode
  `[32, 129, 192, 224]`, assembly `OBS/XOR/OUT/HALT`, salidas `[1]` y `[0]`
  para entradas `1,0` y `1,1`.
- `python -m pytest research\observacionismo-lab\tests -q` tras L1 ->
  `7 passed`.
- `python research\observacionismo-lab\obs_l1_ir.py` -> `ok=true`, bytecode
  `[32, 129, 192, 224]`, checks pasan y envelope `action_gate=APPROVE`.
- Secret scan focalizado con `tools\release\scan_secrets.py --path ... --json`
  sobre los archivos manuales nuevos/actualizados -> `count_reported=0` en
  todos.

## Resumen De Inventario

- Archivos revisados: `275`
- Errores de lectura: `0`
- Grupos de duplicados exactos: `49`
- Extensiones principales: `.md=100`, `.txt=69`, `.py=32`, `.zip=27`,
  `.csv=12`, `.json=10`, `.docx=9`, `.pdf=9`, `.html=7`.
- Terminos dominantes: `gate`, `psi`, `phi`, `j_c`, `ast`, `eml`,
  `witnesslog`, `actiongate`, `lenguaje`, `bit`, `byte`, `compact`.

## Lectura Operativa

CERTEZA:

- Hay duplicados exactos entre `Downloads` y `-=PSI=-` para documentos OSIT,
  TUIP, ingenieria observacionista y paquetes TUI.
- Las fuentes de mayor senal no apuntan a crear un lenguaje grande; apuntan a
  un IR de control con evidencia, gates, AST y handoff.
- Existe codigo local que implementa `ActionGate`, `WitnessLog`, analisis AST,
  residuo, estado PSI y agentes locales.
- El prototipo nuevo `ObsBitMachine` ejecuta bytecode de 8 bits y pasa pruebas.
- El parser L1 de cinco verbos compila a bytecode L0, evalua checks y devuelve
  un `ObservationEnvelope` local.

INFERENCIA:

- La ruta mas pragmatica es L0 maquina de bits, L1 IR de cinco verbos, L2 DSL
  humano minimo. El puente L1->L0 ya esta implementado en modo local.
- Rust/Zig podrian ser runtimes futuros, pero Python es suficiente para falsar
  el diseno actual.
- `@anchor`, `!ASSERT`, `?DISPROVE` y control de KV-cache deben tratarse como
  contratos o hooks, no como capacidad real hasta tener runtime que los aplique.

INCOGNITA:

- No se valido visualmente el contenido completo de PDFs; se priorizaron DOCX,
  TXT, MD, Python y ZIP manifests.
- No se eligio canon para los 49 grupos duplicados.
- No se conecto el VM a `obsai-core` ni a Claudio runtime.

BLOQUEADO:

- No importar ZIPs completos ni TXT crudos a paquetes publicos.
- No publicar claims de fisica, biologia, conciencia o prediccion social desde
  esta sintesis.
- No ejecutar acciones externas, push, deploy ni Gumroad.
- No borrar duplicados hasta elegir canon y pasar ActionGate.

## ObservationEnvelope

```json
{
  "envelope_version": "seto-observation-v1",
  "source_path": "C:\\Users\\L-Tyr\\Downloads + -=CEREBRO=-\\-=PSI=-",
  "source_kind": "directory",
  "sha256": "see qa_artifacts/observacionismo_language/observacionismo_language_inventory_2026-05-05.json",
  "size_bytes": 0,
  "evidence": [
    "curador_preflight REGISTERED_CONTINUE_WITH_BOUNDARY for both roots",
    "inventory records=275 errors=0 duplicates=49",
    "pytest research/observacionismo-lab/tests -q -> 7 passed",
    "obs_l1_ir demo ok=true action_gate=APPROVE"
  ],
  "psi_state": "CERTEZA",
  "claim_level": "operational",
  "falsifiers": [
    "a simpler IR with lower residue explains the same tasks",
    "runtime cannot enforce the proposed gate/trace semantics",
    "tests fail or bytecode trace is non-reproducible"
  ],
  "risk_flags": [
    "raw_downloads",
    "duplicated_sources",
    "research_claims",
    "publication_blocked"
  ],
  "action_gate": "REVIEW",
  "decision": "KEEP",
  "fingerprint": "OBS_LANGUAGE_DOWNLOADS_PSI_2026-05-05"
}
```

## Decision

Mantener las fuentes crudas en su lugar. Usar solo la sintesis operativa, la VM
L0 y el parser L1 local como base para el siguiente paso: conexion por
envelopes/gates hacia `obsai-core`, sin copiar canon ni paquetes completos.
