# TELECOM CORE TEST REPORT

Fecha: 2026-05-12

## Comandos ejecutados

| Comando | Ruta | Resultado |
|---|---|---|
| `npm test -- --runInBand` | `C:\Users\L-Tyr\OneDrive\Documentos\New project 3` | FAILED_EXPECTED: Vitest 2.1.9 no reconoce `--runInBand`. |
| `npm run build` | `C:\Users\L-Tyr\OneDrive\Documentos\New project 3` | PASSED: `tsc -b && vite build`, 1593 modules transformed. |
| `npm test` | `C:\Users\L-Tyr\OneDrive\Documentos\New project 3` | PASSED: 2 test files, 15 tests. |
| `python -m compileall -q .` | `MEDIOEVO_LIVE_TREE` | PASSED. |
| `pytest -q` | `MEDIOEVO_LIVE_TREE` | NOT_APPLICABLE: no `test_*.py` / `*_test.py` Python suite detected. |
| `Start-Process npm.cmd run dev -- --port 5174` | `C:\Users\L-Tyr\OneDrive\Documentos\New project 3` | PASSED_LOCAL: servidor Vite local disponible. |
| `Invoke-WebRequest http://127.0.0.1:5174/telecom` | local | PASSED_LOCAL: HTML con root de Vite servido. |
| `Invoke-WebRequest http://127.0.0.1:5174/src/App.tsx` | local | PASSED_LOCAL: contiene `TelecomCore` y ruta `/telecom`. |
| `Invoke-WebRequest http://127.0.0.1:5174/src/ui/TelecomCore.tsx` | local | PASSED_LOCAL: contiene `DUAT Telecom Core`, `Latest Bulletin`, `WitnessLog Timeline` y `P0 Alerts`. |

## Evidencia

- `src/messagebus/service.test.ts`: 4 tests nuevos para canales/agentes minimos, create/send/ack/resolve, P0/export y handoff/WitnessLog.
- `src/simulation/engine.test.ts`: 11 tests existentes siguen pasando.
- Build de Vite genero `dist/index.html`, CSS y JS.
- UI local verificada en `http://127.0.0.1:5174/telecom`.
- Browser integrado: no expuso la herramienta `node_repl js` requerida por el plugin; se uso verificacion HTTP local como fallback.

## Resultado

Estado: PASSED_LOCAL.

Bloqueo externo: se mantiene por `10_QUALITY/SECRET_SCAN_REPORT.md`.

## Incidencias

- El primer comando de test uso una bandera propia de Jest. Se corrigio con `npm test`.
