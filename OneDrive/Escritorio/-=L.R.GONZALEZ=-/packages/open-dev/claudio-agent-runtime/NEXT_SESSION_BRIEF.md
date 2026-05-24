# NEXT_SESSION_BRIEF Claudio Agent Runtime

## Estado

R_close: 0.04
Phi_eff: 0.91
Regimen: OPTIMO
Autonomy level: 3

## Decisiones tomadas

- `DUAT Operator Shell` es la capa humana/producto.
- `claudio-agent-runtime` es el kernel P0 local dry-run.
- Mercury queda como referencia de implementacion, no como dependencia.
- Canales externos, daemon, provider fallback real y SQLite/FTS quedan en REVIEW.

## Cambios realizados

- Se creo `packages/open-dev/claudio-agent-runtime`.
- Se implementaron comandos P0: `doctor`, `permissions check`, `skills list/inspect`, `memory status/search`, `tasks list/add`, `brief`.
- Se agregaron fixtures para `APPROVE`, `REVIEW`, `BLOCK`, skills, memory y task board.
- Se agregaron tests unitarios/smoke.
- Se implemento `R/Phi budget` deterministico desde task board, memory, WitnessLog,
  command outcomes, rollback y gate events.
- `doctor` y `brief` ahora exponen R/Phi local.
- Se agrego CLI `budget status/report` y artefactos `qa_artifacts/rphi-budget-*`.
- Se agrego calibracion sintetica `budget calibrate` con 9 episodios:
  clean, missing evidence, contradiction, failed command, review/block,
  rollback success/failure, stale memory y mixed realistic sanitized.
- `doctor` y `brief` ahora pueden mostrar el estado de calibracion local si
  existe `qa_artifacts/rphi-calibration-latest.json`.

## Evidencia

- `python -m pytest packages\open-dev\claudio-agent-runtime\tests -q` -> `34 passed in 2.34s`
- `python -m compileall -q packages\open-dev\claudio-agent-runtime\claudio_agent_runtime` -> PASS
- `python tools\release\scan_secrets.py --path packages\open-dev\claudio-agent-runtime --json` -> `count_reported=0`
- `python -m claudio_agent_runtime budget report --root fixtures\state --output-root qa_artifacts --json` -> PASS
- `python -m claudio_agent_runtime budget calibrate --output-root qa_artifacts --json` -> `calibration_status=PASS`, `9/9` episodios

## Pendientes reales

- Extender `WitnessLog` a contrato COMMS/ObservationEnvelope.
- Endurecer `GhostGate plan` con schemas y tool registry formal.
- Calibrar pesos R/Phi con episodios reales sanitizados antes de cualquier claim externo.

## Riesgos

- No publicar: licencia sigue `LEGAL_REVIEW_REQUIRED`.
- No activar Telegram/GitHub/Spotify/daemon sin gate separado.
- No mezclar canon privado ni DUAT/GEODIA interno.

## Bloqueos

- Publicacion externa: `REVIEW`.
- Canales externos: `REVIEW`.
- Dependencias nuevas: `REVIEW`.

## Proxima accion verificable

Agregar un episodio real sanitizado desde un cierre local y compararlo contra
la matriz sintetica sin cambiar pesos automaticamente.

## Segunda perdida

Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.
