<#
.SYNOPSIS
  Registra el OSIT boot witness como tarea al inicio de sesión (usuario actual, sin admin).
.DESCRIPTION
  Crea una tarea de Programador de tareas que ejecuta osit_boot_witness.py en cada logon.
  Es read-only sobre el sistema (solo escribe su propio witness log). Reversible:
  ejecuta unregister_osit_boot_task.ps1 para quitarla. NO toca el BIOS/UEFI.
.NOTES
  Es un CAMBIO DE SISTEMA: ejecútalo tú a conciencia. No requiere privilegios de administrador.
#>
param(
  [string]$TaskName = "OSIT Boot Witness",
  [string]$Python = "python"
)
$ErrorActionPreference = "Stop"

$script = Join-Path $PSScriptRoot "osit_boot_witness.py"
if (-not (Test-Path $script)) { throw "No se encontró el entrypoint: $script" }

$action   = New-ScheduledTaskAction   -Execute $Python -Argument ('"{0}"' -f $script)
$trigger  = New-ScheduledTaskTrigger  -AtLogOn
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings `
  -Description "OSIT logon witness (obsai-core). DEMO_ONLY, read-only, sin admin." -Force | Out-Null

Write-Output "Registrada la tarea '$TaskName' (al inicio de sesión)."
Write-Output "Para quitarla:  pwsh -File `"$($PSScriptRoot)\unregister_osit_boot_task.ps1`""
