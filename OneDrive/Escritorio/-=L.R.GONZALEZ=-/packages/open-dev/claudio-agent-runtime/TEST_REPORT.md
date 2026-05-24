# TEST_REPORT Claudio Agent Runtime P0

Fecha: 2026-05-15

## Comandos

```powershell
python -m pytest packages\open-dev\claudio-agent-runtime\tests -q
python -m compileall -q packages\open-dev\claudio-agent-runtime\claudio_agent_runtime
python tools\release\scan_secrets.py --path packages\open-dev\claudio-agent-runtime --json
python -m claudio_agent_runtime doctor --root fixtures\state --json
python -m claudio_agent_runtime permissions check fixtures\permission_external_publish.json --json
python -m claudio_agent_runtime ghostgate tools --json
python -m claudio_agent_runtime ghostgate check fixtures\ghostgate_plan_blocked.json --json
python -m claudio_agent_runtime execute write fixtures\execute_write_approved.json --root <temp-root> --json
python -m claudio_agent_runtime rollback restore <rollback-id> --root <temp-root> --json
python -m claudio_agent_runtime skills list --root fixtures\skills --json
python -m claudio_agent_runtime doctor --root fixtures\state --witness-root <temp-root> --json
python -m claudio_agent_runtime witness status --root <temp-root> --json
python -m claudio_agent_runtime budget status --root fixtures\state --json
python -m claudio_agent_runtime budget report --root fixtures\state --output-root qa_artifacts --json
python -m claudio_agent_runtime budget calibrate --output-root qa_artifacts --json
```

## Resultado

- Pytest: `34 passed in 2.34s`
- Compileall: PASS, sin salida de error
- Secret scan focalizado: `count_reported=0`
- Doctor smoke: PASS; canales externos disabled; secretos en modo presence-only
- Doctor R/Phi integration: PASS; `rphi_budget` incluido en salida JSON
- Doctor calibration integration: PASS; `rphi_calibration` reporta latest status cuando existe artefacto local
- Permission smoke: `public_publish` devuelve `REVIEW`
- Skills smoke: lista metadata con `loaded=false`
- Witness smoke: eventos JSONL redactados, sin output completo
- GhostGate smoke: `write_file`, `run_command` y `git_push` bloqueados en plan mode
- Execute smoke: `write_file` local reversible crea rollback; acciones `REVIEW` no se ejecutan
- Rollback smoke: `rollback restore` devolvio `status=restored`
- R/Phi budget tests: PASS; empty inputs, missing files, missing evidence,
  rollback failure, clean signals, Phi_eff cost sensitivity, regime boundaries
  schema stability and presence-only secret reporting covered
- R/Phi calibration tests: PASS; 9 episodios sinteticos, checks direccionales,
  schema estable, CLI `budget calibrate` y artefactos generados cubiertos
- Calibration latest: `PASS`, `9/9` episodios

## Frontera

- No dependencias nuevas.
- No red.
- No canales externos.
- No copia de codigo Mercury.
- No publicacion.
- No runtime privado, libros, RPG/TCG ni secretos.
