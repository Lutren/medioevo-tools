# Ficha Curador SETO - VALIDATION_REPORT_NODE_UI (1).md

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\VALIDATION_REPORT_NODE_UI (1).md` |
| SHA256 | `1D183B6313E549D8E0BAEFBA1E2FF3134A4AFA11E70DB0CCD18347F4A1C6C15E` |
| Bytes | `3722` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `ARCHIVO_FRIO` |
| Clasificacion | `TEXT_SOURCE_REVIEW` |
| Lane | `cleanup` |
| Decision | `ABSORBIDO_CANONIZADO_ARCHIVO_FRIO` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\downloads\2026-05-10\1D183B6313E549D8_validation_report_node_ui-1.md` |
| Atlas | `Curaduria SETO` |

## Resumen

Text source; register before deciding canon, archive or deletion.

## Sinapsis

- Destino: `Curador review queue`.
- Evidencia: SHA256 `1D183B6313E549D8E0BAEFBA1E2FF3134A4AFA11E70DB0CCD18347F4A1C6C15E`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
