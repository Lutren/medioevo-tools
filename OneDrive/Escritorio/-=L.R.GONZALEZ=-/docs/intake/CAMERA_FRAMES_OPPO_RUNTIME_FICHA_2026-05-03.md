# Ficha Curador - camera_frames OPPO runtime

Fecha: 2026-05-03

Ruta:

`-=MEDIOEVO=-\-=LIBROS\claudio\camera_frames`

## Estado

- classification: `LOCAL_RUNTIME_ASSET`
- status: `REGISTERED_CONTINUE_WITH_BOUNDARY`
- public_boundary: no publicar; carpeta ignorada por Git.
- private_boundary: no contiene RPG/TCG segun ruta, pero puede contener capturas de contexto local; tratar como runtime privado.
- discard_rule: limpieza permitida solo por hash exacto, dentro de la carpeta
  ignorada, conservando una muestra y con ActionGate aprobado.

## Evidencia

Comandos:

```powershell
python tools\release\curador_preflight.py --path '.\-=MEDIOEVO=-\-=LIBROS\claudio\camera_frames'
git -C '.\-=MEDIOEVO=-\-=LIBROS\claudio' check-ignore -v -- 'camera_frames\oppo_frame_1.png'
```

Dry-run:

`qa_artifacts\release_validation\camera-frames-cleanup-dry-run-2026-05-03.json`

Resultado:

`qa_artifacts\release_validation\camera-frames-cleanup-result-2026-05-03.json`

Resultado verificado:

- `total_files=218`
- `total_bytes=1,735,498`
- `unique_hashes=1`
- `exact_duplicate_delete_candidates_count=217`
- `deleted_count=217`
- `deleted_bytes=1,727,537`
- `preserved_count=1`
- muestra ignorada por `.gitignore:231:camera_frames/`
- ActionGate decision: `1587d99b-449c-4b5e-a7e7-36214498a471`

## Lectura

Los archivos `oppo_frame_*.png` eran una secuencia runtime ignorada con el
mismo SHA256. No son fuente ni producto; son evidencia visual local/regenerable.

## Decision

Se borraron 217 duplicados exactos y se preservo una muestra:

`oppo_frame_20260418_002952.png`

No publicar. Si la carpeta vuelve a crecer, repetir el mismo protocolo: ficha,
dry-run, ActionGate y preservacion de muestra por hash.
