Param(
    [string]$ModelId
)

# Select a wabi-sabi model for this PowerShell session.
# Usage: .\select_model.ps1 -ModelId nemotron_ultra_253b

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$workspaceRoot = Resolve-Path (Join-Path $scriptDir '..')
$confPath = Join-Path $workspaceRoot 'apps\local\wabi-sabi\config\models.wabisabi.yaml'
if (-not (Test-Path $confPath)) {
    Write-Host "Config not found at $confPath. Wabi-Sabi canonical route may be missing." -ForegroundColor Yellow
}

if (-not $ModelId) {
    Write-Host "Please provide -ModelId. Available IDs are listed in apps\local\wabi-sabi\config\models.wabisabi.yaml." -ForegroundColor Cyan
    exit 1
}

# Set active model in this session
$env:ACTIVE_WABISABI_MODEL = $ModelId
Write-Host "ACTIVE_WABISABI_MODEL set to $ModelId (session only)." -ForegroundColor Green
Write-Host "Note: Secrets are NOT displayed. Ensure required env vars are set: NVCR_TOKEN, NGC_ACCESSKEY_ID, NGC_ACCESSKEY_SECRET, QWEN_API_KEY as needed." -ForegroundColor Yellow
