# Editorial Internal Exports Closeout - 2026-05-22

## Estado

Carril local cerrado para Fragmentos y Calibracion.

## Evidencia

- `python tools\release\pending_review.py --write --quiet`:
  `active_dedup=0`, `claudio_open=0`.
- `books\editorial\internal_exports\FRAGMENTOS_INTERNAL_EXPORT_2026-05-22`
  creado con MD, HTML, DOCX, PDF, EPUB, README y manifiesto.
- `books\editorial\internal_exports\CALIBRACION_INTERNAL_EXPORT_2026-05-22`
  creado con MD, HTML, DOCX, PDF, EPUB, README y manifiesto.
- Ambos `INTERNAL_EXPORT_MANIFEST.json` verifican `hash_ok=True`.
- Ambos manifiestos declaran `PublicationGate=BLOCK`,
  `originals_modified=false` y `external_actions_performed=false`.

## ActionGate

- Copia local path-scoped desde canon10 integrado: APPROVE.
- Generacion local de EPUB con Calibre `ebook-convert`: APPROVE.
- Manifiestos/hash/README: APPROVE.
- GitHub, Gumroad, KDP, web, redes, push, deploy, public ZIP o release externo:
  BLOCK.

## Frontera

Estos paquetes contienen material editorial completo para revision privada. No
son staging publico, no cambian licencia y no autorizan venta ni publicacion.

## Proxima accion verificable

Ejecutar QA visual DOCX split o preparar brief de portada interno bajo gate
REVIEW. Si `pending_review.py` sigue en cero, no abrir features nuevas sin una
directiva local verificable.
