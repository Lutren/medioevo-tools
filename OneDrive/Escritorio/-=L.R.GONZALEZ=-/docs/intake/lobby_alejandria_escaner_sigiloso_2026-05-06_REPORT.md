# Lobby de Alejandria Full Absorption

Generated UTC: `2026-05-06T19:08:19.237457+00:00`

## Summary

- Files read: `2`
- Total lines read: `74`
- Archived to Archivo Frio: `1`
- Kept in Lobby: `1`

## Lane Counts

| lane | files |
|---|---:|
| `Curaduria SETO` | 1 |
| `Matrix/Biblioteca` | 1 |

## Records

| file | lane | gate | status | sha256 | lines | target |
|---|---|---|---|---|---:|---|
| `escaner sigiloso.txt` | `Curaduria SETO` | `REVIEW` | `ABSORBIDO_ARCHIVO_FRIO` | `0C7CDDAA915D42C4` | 37 | `docs/intake`<br>`runtime/curador_seto` |
| `README_LOBBY_DE_ALEJANDRIA.md` | `Matrix/Biblioteca` | `REVIEW` | `CANONICO_EN_LOBBY` | `462F1B416C3803A4` | 37 | `docs/matrix`<br>`library/index.json`<br>`library/modules` |

## Extracted Patterns

### escaner sigiloso.txt

- Original: `C:\Users\L-Tyr\OneDrive\Escritorio\Lobby de Alejandria\escaner sigiloso.txt`
- Archivo Frio: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\lobby_alejandria\2026-05-06\20_curaduria_seto\0C7CDDAA915D42C4_escaner-sigiloso.txt`
- Decision: `ABSORB_TO_ATLAS_AND_ARCHIVE_SOURCE`
- Evidence markers: `none`
- Patterns:
  - # Creamos un paquete ARP para obtener la MAC del objetivo
  - # Enviamos y recibimos respuesta
  - # Este es el 'kernel' de observación inversa:
  - # Identificar la presencia del sistema por su respuesta al vacío.

### README_LOBBY_DE_ALEJANDRIA.md

- Original: `C:\Users\L-Tyr\OneDrive\Escritorio\Lobby de Alejandria\README_LOBBY_DE_ALEJANDRIA.md`
- Decision: `KEEP_LOBBY_OPERATING_README`
- Evidence markers: `actiongate`
- Patterns:
  - # Lobby de Alejandria
  - ## Regla
  - ## Prohibido
  - - Publicar contenido sin ActionGate.
  - ## Ritmo
  - ## Ultimo pase

