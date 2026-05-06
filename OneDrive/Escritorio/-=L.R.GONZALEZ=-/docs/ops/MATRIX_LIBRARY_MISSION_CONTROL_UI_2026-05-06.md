# Matrix Library Mission Control UI - 2026-05-06

## Estado

- Resultado: `VALIDATED_LOCAL`
- Carril: Prompt 15 / Biblioteca Matrix / Mission Control
- ActionGate efectivo: `REVIEW`
- Host observado: `CONTAMINADO`
- Accion host indicada: `recalibrate`
- Evidencia host: `runtime/host_observacionista/latest_report.json`, timestamp `2026-05-06T08:18:32Z`
- Pending refresh inicial: `active_dedup=389`, `claudio_open=69`

## Implementacion

Se conecto Biblioteca Matrix al Mission Control como panel local:

- Panel `matrix-library-panel` con indice, modulos, activos y limite de canon completo.
- Lecturas UI desde `/api/local/matrix/status` y `/api/local/matrix/modules`.
- Fallback local para `public_safe`: biblioteca oculta y sin rutas locales.
- Separacion de errores entre mapa Matrix y Biblioteca Matrix; un fallo de biblioteca ya no degrada el mapa principal.
- Prueba estatica del HTML ampliada para exigir panel y rutas locales de Matrix.

## Archivos Tocadas

- `-=MEDIOEVO=-/-=LIBROS/claudio/apps/hormiguero_mission_control/index.html`
  - SHA256: `B93B9F62D7CC10996533606BF2509008DE005BAC6F6434886C5B453BE0DECBE8`
- `-=MEDIOEVO=-/-=LIBROS/claudio/tests/test_hormiguero_mission_control_api.py`
  - SHA256: `39D4C9A3606223572C219472BE7A032C2183BEBFB130ACDC8F40686222EBA964`

Nota de concurrencia: ambos archivos ya tenian cambios locales previos de otros carriles. Esta pasada agrego solo la conexion Biblioteca Matrix/fallback y las aserciones UI relacionadas, preservando los cambios concurrentes.

## Validacion

- `python -m pytest tests\test_hormiguero_mission_control_api.py -q`
  - Resultado: `27 passed in 1.19s`
- `python -m pytest tests\test_hormiguero_mission_control_api.py::test_hormiguero_index_serves_restored_ui tests\test_matrix_library_api.py -q`
  - Resultado: `7 passed in 1.60s`
- `python -m py_compile apps\hormiguero_mission_control\app.py core\matrix_library.py`
  - Resultado: `OK`
- Check estatico de IDs/rutas:
  - `missing=[]`
  - `matrix_status_refs=2`
  - `matrix_modules_refs=2`
- COMMS validator antes de publicar este evento:
  - Resultado: `PASS`
- JSONL COMMS despues de publicar evento:
  - Resultado: `lines=7`, `last_event=matrix-library-mission-control-ui-2026-05-06-007`
- COMMS validator despues de publicar evento:
  - Resultado: `PASS`

## Limites

- No se arranco daemon.
- No se abrio navegador ni servidor.
- No se hizo publicacion, deploy, push ni accion externa.
- No se tocaron pesos, aliases, adaptadores ni entrenamiento.
- No se tocaron rutas privadas RPG/TCG.
- No se hizo borrado, movimiento destructivo ni limpieza amplia.

## Falsadores

- El HTML deja de contener `matrix-library-panel`.
- `/api/local/matrix/status` o `/api/local/matrix/modules` desaparecen del Mission Control.
- El perfil `public_safe` accede a rutas locales de Biblioteca Matrix.
- El mapa Matrix cae por un fallo aislado de Biblioteca Matrix.
- Las pruebas `test_hormiguero_mission_control_api.py` o `test_matrix_library_api.py` fallan.
