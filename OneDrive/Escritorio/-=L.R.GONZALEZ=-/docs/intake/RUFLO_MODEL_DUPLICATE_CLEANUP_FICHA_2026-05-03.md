# Ficha Curador - Ruflo model duplicate cleanup

Fecha: 2026-05-03

## Rutas

Canon preservado:

`-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\models\phi-4-mini\cpu_and_mobile\cpu-int4-rtn-block-32-acc-level-4`

Duplicado limpiado:

`-=MEDIOEVO=-\-=LIBROS\claudio\.skills\ruflo\v2\models\phi-4-mini\cpu_and_mobile\cpu-int4-rtn-block-32-acc-level-4`

## Decision

- classification: `VENDOR_CACHE_DUPLICATE`
- status: `CLEANED_WITH_CANON_PRESERVED`
- public_boundary: no publicar `.skills`.
- private_boundary: no copiar a paquetes publicos; ruta oculta/vendor.
- canonical_reason: la copia raiz `-=LIBROS\.skills\ruflo` conserva `.git` y remoto upstream `https://github.com/ruvnet/ruflo.git`; la copia bajo `claudio\.skills\ruflo` no tiene `.git`.

## Evidencia

Dry-run:

`qa_artifacts\release_validation\ruflo-model-duplicate-cleanup-dry-run-2026-05-03.json`

Resultado:

`qa_artifacts\release_validation\ruflo-model-duplicate-cleanup-result-2026-05-03.json`

Verificado:

- archivos duplicados: `model.onnx`, `model.onnx.data`
- hashes iguales contra canon: `true`
- bytes borrados: `96,854,299`
- archivos borrados: `2`
- archivos `model.onnx*` restantes en duplicado Claudio: `0`
- ActionGate: `e6623488-ef44-47f1-b7c2-164e7dba9272`

## Regla Futura

No borrar el clon canonico raiz sin revisar el repo upstream. Si Claudio vuelve a
necesitar esos modelos dentro de su `.skills`, regenerarlos desde fuente o
copiarlos conscientemente con nueva ficha.
