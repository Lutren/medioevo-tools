# Claudio Root Next Safe Batches - 2026-05-06

Status: `POST_CLEANUP_REVIEW / NO_MOVE_NO_DELETE`

## Estado Actual

Despues de los lotes aplicados:

- root items: `234`
- root files: `88`
- root directories: `146`
- docs raiz pendientes: `6`
- launchers raiz pendientes: `0`
- media/UI raiz pendientes: `0`
- Python raiz pendientes: `2` tracked + scripts sensibles/comerciales bloqueados por nombre
- caches regenerables aprobadas restantes: `0` en el postcheck final

## Lotes Restantes

| lote | count | decision | accion segura siguiente |
|---|---:|---|---|
| `root_data_config` | 48 | `MOVE_CANDIDATE_REVIEW` | crear mapa de dependencias antes de mover |
| `local_state_db` | 10 | `KEEP_REVIEW_RETENTION` | no mover sin saber quien abre cada DB |
| `secret_or_sensitive` | 14 | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | no leer ni mover automaticamente |
| `cache_regenerable` | 5 | `REVIEW` | no borrar: `cache`, `logs`, `screenshots`, `_ui_uploads`, `camera_frames` pueden contener evidencia o entradas humanas |
| `domain_module_or_legacy_dir` | 109 | `REVIEW_DESTINATION` | revisar por modulo, no por barrido global |

## Regla Fundamental

La raiz de Claudio ya no debe recibir documentos, launchers, scripts sueltos ni
assets sueltos. Todo nuevo archivo debe entrar a una ruta con funcion:

- documentos: `docs/`
- herramientas: `tools/`
- runtime/state: `runtime/`
- datos/config revisados: `data/`
- assets/UI: `assets/`
- material sensible: bloqueado hasta gate

## Proximo Paso Correcto

No mover los 48 JSON/CSV/YAML todavia. Primero generar un mapa:

1. nombre de archivo;
2. hash;
3. si contiene marcadores sensibles;
4. rutas de codigo que lo leen;
5. destino propuesto;
6. rollback;
7. gate.

Solo despues de ese mapa se puede aplicar un lote `data/root_config_review`.

## Bloqueo

No borrar bases de datos, secretos, logs, screenshots, uploads, camera frames,
configs comerciales, tokens, Gumroad, Jellyfin, TV, perfiles de usuario,
beneficiarios ni material privado desde esta fase.

