# Terminal Window Popup Diagnosis 2026-05-07

## Estado

Estado: `PRIMARY_CAUSE_IDENTIFIED / FIX_APPLIED_FOR_CURADOR_TASK`

## Sintoma

El usuario reporto que de repente se abre y se cierra una ventana de terminal.

## Evidencia observada

### Candidato principal

Tarea programada:

- TaskName: `CuradorSETO-Downloads-Intake`
- TaskPath: `\`
- LastRunTime observado: `2026-05-07 01:05:01`
- LastTaskResult: `0`
- Trigger: repeticion cada `PT30M`
- Accion original:
  `C:\Users\L-Tyr\curador_seto_downloads.cmd`

Contenido del `.cmd`:

```cmd
@echo off
cd /d "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-"
"C:\Users\L-Tyr\AppData\Local\Programs\Python\Python311\python.exe" tools\release\curador_automation.py absorb --root downloads --recursive --write-index --write-fichas --write-atlas --archive-absorbed --apply-safe-deletes
```

Lectura tecnica:

- Windows Task Scheduler ejecutando un `.cmd` con `InteractiveToken` puede abrir
  una consola visible aunque el proceso termine rapido.
- La frecuencia de 30 minutos explica la aparicion repentina.
- La evidencia de salida del curador existe:
  `qa_artifacts/release_validation/curador-automation-downloads-absorb-result-2026-05-07.json`.

### Candidatos secundarios

- Startup: `OpenClaw Gateway.cmd` usa `start "" /min cmd.exe /d /c ...`.
  Puede abrir consola minimizada al iniciar sesion.
- Run key: `HKCU\...\Run\ClaudioHarnessAutopilot` llama `powershell.exe`
  directamente con `run_claudio_harness_autopilot.ps1 -Full`. Puede abrir
  consola al iniciar sesion.
- Wabi manual: `apps/local/wabi-sabi/wabi-window.ps1` usa `WindowStyle Normal`
  de forma intencional cuando el operador abre Wabi como ventana persistente.

## Accion aplicada

Se creo un wrapper oculto:

- `tools/release/curador_seto_downloads_hidden.vbs`

El wrapper ejecuta el `.cmd` existente con `WScript.Shell.Run(..., 0, True)`,
manteniendo el exit code y evitando ventana visible.

Se actualizo la accion de la tarea programada:

```txt
Execute: C:\Windows\System32\wscript.exe
Argument: //B //Nologo "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\tools\release\curador_seto_downloads_hidden.vbs"
```

## Verificacion

- Smoke wrapper:
  `cscript.exe //Nologo "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\tools\release\curador_seto_downloads_hidden.vbs"`
  -> exit `0`.
- Tarea lanzada manualmente tras el cambio:
  `Start-ScheduledTask -TaskName CuradorSETO-Downloads-Intake`
  -> `State=Ready`, `LastRunTime=2026-05-07 01:13:40`, `LastTaskResult=0`.
- Accion actual exportada:
  `Command=C:\WINDOWS\System32\wscript.exe`.
- Proxima ejecucion programada observada:
  `2026-05-07 01:35:00`.
- Pending snapshot tras el cambio:
  `active_dedup=0`, `claudio_open=0`.
- Cache residue after diagnostics:
  `terminal-popup-postfix-cache-cleanup-2026-05-07.json` removed one
  regenerated `tools/release/__pycache__`; final validation
  `terminal-popup-postfix-cache-final-validation-2026-05-07.json` returned
  `total_candidates=0`, `blocked_count=0`, `errors=0`.
- Final cache validation after JSON/diff checks:
  `terminal-popup-final-cache-validation-2026-05-07.json` returned
  `total_candidates=0`, `blocked_count=0`, `errors=0`.

## Backup

Antes de cambiar la tarea se exporto XML:

- `qa_artifacts/release_validation/curador-seto-downloads-intake-task-before-hidden-2026-05-07.xml`

## Lo que no se cambio

- No se desactivo la tarea.
- No se cambio la cadencia de 30 minutos.
- No se tocaron claves Startup/Run secundarias.
- No se mataron procesos.
- No se leyeron ni imprimieron secretos.

## Pendiente seguro

Si todavia aparece una ventana despues de este cambio, revisar en este orden:

1. `OpenClaw Gateway.cmd` en Startup.
2. `ClaudioHarnessAutopilot` en `HKCU\...\Run`.
3. Eventos de Task Scheduler cercanos al timestamp exacto del popup.
