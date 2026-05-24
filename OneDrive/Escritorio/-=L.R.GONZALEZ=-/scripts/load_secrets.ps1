# Wrapper to load secrets into current session
Param()
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$store = Join-Path $scriptDir 'secret_store.ps1'
if (-not (Test-Path $store)) { Write-Host "secret_store.ps1 missing"; exit 1 }
. $store
Load-WabiSabiSecrets
