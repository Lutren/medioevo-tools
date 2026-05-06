# Portfolio Curador Audit - 2026-05-05

Estado: `AUDITORIA_CON_EVIDENCIA / SIN_BORRADO_DIRECTO`

Raiz de gobierno: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`

## Alcance

| ruta | rol operativo | decision |
|---|---|---|
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-` | canon, teoria, paquetes y fuentes PSI/Observacionismo | `REGISTERED_CONTINUE_WITH_BOUNDARY` |
| `C:\Users\L-Tyr\Downloads` | fuentes crudas, prototipos, capturas y paquetes de investigacion | `REGISTERED_CONTINUE_WITH_BOUNDARY` |
| `C:\Users\L-Tyr\OneDrive\Escritorio` | accesos, handoffs y raices de trabajo | revisar por ficha, no borrar por nombre |
| `E:\` | offload, RPG privado, assets, audio, modelos y cache externo | `REGISTERED_CONTINUE_WITH_BOUNDARY` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-` | gobierno, productos, publish staging, docs y herramientas | fuente de control local |

## Evidencia generada

| evidencia | resultado |
|---|---|
| `python tools\release\pending_review.py --write --quiet` | `active_dedup=1700`, `claudio_open=52`, salida en `qa_artifacts/pending/pending_review_2026-05-05.json` |
| `python tools\release\source_intake.py --hash --write` | `SOURCE_INTAKE_REGISTER.md` y `source_intake_register.json` actualizados con Downloads actuales |
| `python tools\release\audit_repo.py` | `10758` archivos activos, `1774` directorios, Git roots detectados por carril |
| `python tools\release\find_large_files.py --limit 40 --min-mb 10 --include-denied --json` | peso principal en historia Git, vendor/modelos, releases comerciales y entornos |
| `python tools\release\curador_preflight.py --path <ruta>` | `REGISTERED_CONTINUE_WITH_BOUNDARY` para PSI, Downloads y `E:\` |
| inventario focalizado | `qa_artifacts\release_validation\portfolio-curador-inventory-2026-05-05.json` |
| safety scan global | `reported findings: 200`; el workspace completo sigue no apto para publicacion por glob amplio |

## Verdad operativa

La limpieza no debe empezar por borrar documentos. El ruido actual viene de tres clases distintas:

1. Fuentes crudas valiosas sin ficha suficiente: TXT, PY, HTML, ZIP, PDF/DOCX y capturas nuevas en Downloads.
2. Duplicados exactos ya copiados desde Downloads hacia `-=PSI=-`, donde `-=PSI=-` debe actuar como copia canonica de investigacion.
3. Peso estructural que no se resuelve con `Remove-Item`: objetos Git, vendors, entornos, modelos, paquetes comerciales y frontera privada.

## Snapshot por ruta

| ruta | archivos revisados | dirs revisados | MB aprox | lectura |
|---|---:|---:|---:|---|
| `-=PSI=-` | 120 | 11 | 6.33 | contiene canon activo, archivo legacy, paquetes y salidas OSIT/TUIP nuevas |
| `Downloads` | 175 | 1 | 77.13 | alta concentracion de prototipos Claudio/DUAT/Observacionismo y duplicados exactos |
| `Escritorio` | 117 | 9 | 1.10 | accesos y handoffs, bajo peso; no parece el problema de espacio |
| `-=L.R.GONZALEZ=-` nivel 1 | 140 | 20 | 7.53 | gobierno y control docs; el peso real esta en subarboles |
| `E:\` nivel focalizado | 240 | 28 | 1400.49 | RPG privado, assets, audio, caches, offload y modelos; no publicar ni limpiar como basura |

## Fichas y fuentes

Nueva ficha PSI:

- `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\00_FICHA_TECNICA_PSI_2026-05-05.md`

Registro maestro actualizado:

- `SOURCE_INTAKE_REGISTER.md`
- `source_intake_register.json`

Evidencia de duplicados:

- `qa_artifacts\release_validation\portfolio-curador-inventory-2026-05-05.json`

## Duplicados exactos relevantes

No se borraron archivos en este pase. Estos grupos quedan como candidatos con regla canonica:

| grupo | copia canonica propuesta | candidatos futuros |
|---|---|---|
| documentos OSIT/TUIP en PDF/DOCX | `-=PSI=-` | copias identicas en `Downloads` |
| `OBSERVACIONISMO_TUI_R3_PACK.zip` | `-=PSI=-\OBSERVACIONISMO_TUI_R3_PACK (1).zip` hasta revisar lineage | copia identica en `Downloads` |
| `claudio_ui_nollm.html` | por decidir; prototipo, no canon PSI | duplicados en Downloads y PSI |
| `duat_observacionismo_unified_v4_code_agent*.zip` | una sola copia en Downloads si se conserva | dos copias con sufijo `(1)` y `(2)` |
| `claudio_local_code_agent*.py/.zip` | una copia limpia tras revision de codigo | copias con sufijo `(1)` |
| `Downloads\New folder\*.md/.txt` contra PSI | `-=PSI=-` o `canon\extensiones_formales` segun ruta | espejo `Downloads\New folder` |
| `-=PSI=-\archive\vault_redundante_2026-04-26` | no canonico; evidencia legacy | solo archivable/borrable despues de ficha y gate |

## No borrar

| ruta/patron | razon |
|---|---|
| `E:\Medioevo_RPG` | proyecto privado vivo; validacion y frontera propia |
| `E:\MEDIOEVO_ASSETS` | assets privados/comerciales/TCG; requiere source-of-truth por asset |
| `-=MEDIOEVO=-\-=LIBROS\.git\objects\**` | peso de historia Git; requiere plan de repo limpio/offload, no borrado directo |
| `metaevo-tcg`, `claudio\tcg`, `runtime\game_bridge` | frontera privada |
| `apps\commercial\*\qa_artifacts` | evidencia comercial y QA; no eliminar por tamano |
| `Downloads\*.png` numericos | parecen lote de imagenes/capturas; aun `REVIEW_REQUIRED_DOWNLOAD` hasta ficha visual |

## Configuracion aplicada

- `SOURCE_INTAKE_REGISTER.md` fue regenerado con hash actual para que Downloads deje de ser una pila suelta.
- `pending_review` quedo actualizado al 2026-05-05.
- Se agrego esta auditoria como punto de continuidad para el siguiente agente.
- Se agrego una seccion nueva en `DELETE_CANDIDATES.md` con candidatos, no acciones ejecutadas.

## Siguiente cierre seguro

1. Revisar los grupos duplicados listados en `DELETE_CANDIDATES.md`.
2. Elegir copia canonica para `claudio_ui_nollm` y prototipos `claudio_local_code_agent`.
3. Si el usuario autoriza limpieza, borrar solo duplicados exactos con SHA registrado, copia canonica preservada y gate `APPROVE`.
4. Convertir las fuentes crudas de mayor valor en fichas separadas: `DUAT/GEODIA R4`, `OSIT/TUIP`, `Claudio local code agent`, `imagenes/capturas Downloads`.
5. Mantener `E:\` como frontera privada/offload; no mezclar RPG/assets con open-dev ni website.
