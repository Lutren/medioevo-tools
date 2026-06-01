# Ficha Curador SETO - 06_HERRAMIENTAS.md

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\06_HERRAMIENTAS.md` |
| SHA256 | `F214A1507B0822C2D5AC42000EBFCB55EB6EC4F9DB216CA87BA610B0B94F2D09` |
| Bytes | `3270` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `ARCHIVO_FRIO` |
| Clasificacion | `TEXT_SOURCE_REVIEW` |
| Lane | `cleanup` |
| Decision | `ABSORBIDO_CANONIZADO_ARCHIVO_FRIO` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\downloads\2026-05-31\F214A1507B0822C2_06_herramientas.md` |
| Atlas | `Curaduria SETO` |

## Resumen

Text source; register before deciding canon, archive or deletion.

## Sinapsis

- Destino: `Curador review queue`.
- Evidencia: SHA256 `F214A1507B0822C2D5AC42000EBFCB55EB6EC4F9DB216CA87BA610B0B94F2D09`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
