<#
.SYNOPSIS
  Quita la tarea del OSIT boot witness (deja el sistema como estaba).
#>
param(
  [string]$TaskName = "OSIT Boot Witness"
)
$ErrorActionPreference = "Stop"

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
  Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
  Write-Output "Tarea '$TaskName' eliminada. El witness log NO se borra (bórralo a mano si quieres)."
} else {
  Write-Output "No existe la tarea '$TaskName'; nada que quitar."
}
