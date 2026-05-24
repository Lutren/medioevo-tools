Param(
    [string]$DefaultModel = 'nemotron_ultra_253b'
)

# Startup helper: ensure secrets are loaded, ACTIVE_WABISABI_MODEL is set and start
# one windowless stub adapter for the default model.
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$workspaceRoot = Resolve-Path (Join-Path $scriptDir '..')
$wabiRoot = Resolve-Path (Join-Path $workspaceRoot 'apps\local\wabi-sabi')
$logDir = Join-Path $wabiRoot 'runtime\logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$startupLog = Join-Path $logDir 'wabi_sabi_startup.log'

function Write-StartupLog {
    param([string]$Message)
    $stamp = Get-Date -Format 'yyyy-MM-ddTHH:mm:ssK'
    Add-Content -LiteralPath $startupLog -Value "$stamp $Message"
}

function Resolve-WindowlessPython {
    $pythonw = Get-Command pythonw.exe -ErrorAction SilentlyContinue
    if ($pythonw) {
        return $pythonw.Source
    }
    $python = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($python) {
        $siblingPythonw = Join-Path (Split-Path -Parent $python.Source) 'pythonw.exe'
        if (Test-Path -LiteralPath $siblingPythonw) {
            return $siblingPythonw
        }
    }
    throw "pythonw.exe not found; refusing to start a visible console adapter."
}

function Test-LocalPortOpen {
    param(
        [int]$Port
    )
    $client = [System.Net.Sockets.TcpClient]::new()
    try {
        $async = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
        if (-not $async.AsyncWaitHandle.WaitOne(500)) {
            return $false
        }
        $client.EndConnect($async)
        return $true
    } catch {
        return $false
    } finally {
        $client.Close()
    }
}

function Start-WindowlessPython {
    param(
        [string[]]$Arguments,
        [string]$WorkingDirectory
    )
    $pythonExe = Resolve-WindowlessPython
    Start-Process -FilePath $pythonExe -ArgumentList $Arguments -WindowStyle Hidden -WorkingDirectory $WorkingDirectory | Out-Null
}

function Test-AdapterRunning {
    param([string]$AdapterPath)
    $adapterName = Split-Path -Leaf $AdapterPath
    $escapedPath = [regex]::Escape($AdapterPath)
    $proc = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -in @('python.exe', 'pythonw.exe') -and
            $_.CommandLine -and
            ($_.CommandLine -match $escapedPath -or $_.CommandLine -like "*$adapterName*")
        } |
        Select-Object -First 1
    return [bool]$proc
}

$loadScript = Join-Path $scriptDir 'load_secrets.ps1'
if (Test-Path $loadScript) {
    & $loadScript *> $null
} else {
    Write-StartupLog "load_secrets.ps1 not found; proceeding without secrets."
}

if (-not $env:ACTIVE_WABISABI_MODEL -or $env:ACTIVE_WABISABI_MODEL -eq '') { [Environment]::SetEnvironmentVariable('ACTIVE_WABISABI_MODEL',$DefaultModel,'Process') }
Write-StartupLog "ACTIVE_WABISABI_MODEL=$env:ACTIVE_WABISABI_MODEL"

$adaptersDir = Join-Path $wabiRoot 'adapters' | Resolve-Path

$mid = $env:ACTIVE_WABISABI_MODEL
if ($mid -match 'nemotron') {
    $adapter = Join-Path $adaptersDir 'stub_nemotron.py'
} elseif ($mid -match 'qwen') {
    $adapter = Join-Path $adaptersDir 'stub_qwen.py'
} elseif ($mid -match 'deep_see4') {
    $adapter = Join-Path $adaptersDir 'stub_deepsee4.py'
} else {
    Write-StartupLog "No adapter configured for model id: $mid"
}

if ($adapter) {
    if (Test-AdapterRunning -AdapterPath $adapter) {
        Write-StartupLog "adapter already running: $adapter"
    } else {
        Start-WindowlessPython -Arguments @("`"$adapter`"") -WorkingDirectory $adaptersDir
        Write-StartupLog "adapter started windowless: $adapter"
    }
}

Write-StartupLog "Startup script completed."
