# Formal Archive Intake - 2026-05-13

Estado: `CUARENTENA_METADATA_ONLY`

## Alcance

Fuentes revisadas sin extraccion en sitio, sin ejecucion de codigo y sin
movimiento de archivos:

- `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\medioevo_info_chemistry_v0_2.zip`
- `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\medioevo_prompt_compression_experiment_bundle.zip`

El directorio original `C:\Users\L-Tyr\OneDrive\Escritorio\Formal` ya no existe
como raiz activa. La copia canonica local encontrada para este cierre esta bajo
`-=CEREBRO=-\archive\bu`.

## Evidencia

Comando seguro usado: PowerShell con
`[System.IO.Compression.ZipFile]::OpenRead(...)`, lectura de directorio central
solamente. No se llamo `ExtractToDirectory`, no se abrio binario ejecutable y no
se escribio contenido del ZIP fuera de este reporte.

| Archivo | Bytes | SHA256 | Entradas |
|---|---:|---|---:|
| `medioevo_info_chemistry_v0_2.zip` | 10795 | `2ABF02A879318E35AA88246F81FDD5AC1A954912252613839964AD6BC461FE54` | 5 |
| `medioevo_prompt_compression_experiment_bundle.zip` | 31117 | `E2BC987C24F7D46706481033EDA3C5981241854EF2675CFEAD3770890817727C` | 5 |

## Inventario Cuarentenado

### `medioevo_info_chemistry_v0_2.zip`

| Entrada | Bytes descomprimidos | Bytes comprimidos | Ruta |
|---|---:|---:|---|
| JSON tabla periodica | 18906 | 4049 | `medioevo_info_chemistry_v0_2/periodic_table_info.json` |
| JSON moleculas | 7465 | 1776 | `medioevo_info_chemistry_v0_2/molecules_medievo.json` |
| Prompt generador arquitectura | 2491 | 1286 | `medioevo_info_chemistry_v0_2/architecture_generator_prompt.md` |
| Codigo generador arquitectura | 5098 | 2003 | `medioevo_info_chemistry_v0_2/architecture_generator.py` |
| README | 1495 | 765 | `medioevo_info_chemistry_v0_2/README.md` |

Decision: candidato de valor tecnico bajo `CODE_INSIGHT`; requiere extraccion
cuarentenada futura si se quiere comparar `architecture_generator.py` contra
contratos Wabi/Sabi. No se importa ni ejecuta.

### `medioevo_prompt_compression_experiment_bundle.zip`

| Entrada | Bytes descomprimidos | Bytes comprimidos | Ruta |
|---|---:|---:|---|
| Resultados completos | 8394 | 1393 | `results_full.csv` |
| Estadisticas resumen | 281 | 177 | `summary_stats.csv` |
| Comparacion de ganadores | 1829 | 639 | `comparison_wins.csv` |
| Corpus simulado | 33968 | 5550 | `simulated_corpus.csv` |
| Libro de calculo | 24695 | 22726 | `medioevo_prompt_compression_experiment.xlsx` |

Decision: candidato de evidencia experimental y benchmarking. El siguiente paso
seguro es leer CSV/XLSX en carpeta temporal cuarentenada solo si un claim o test
lo necesita. No hay canon directo desde este ZIP.

## Riesgos

- `architecture_generator.py` puede ser codigo generado; queda bloqueado para
  ejecucion directa.
- El XLSX puede requerir QA con herramienta de planillas si se usa como
  evidencia; no se abre visualmente en este pase.
- Estos ZIPs no justifican borrado, renombrado ni migracion masiva.

## Cierre

El pendiente `Formal P1: archive-intake cuarentenado` queda cerrado en modo
metadata-only. La fuente original permanece intacta y hashada.

