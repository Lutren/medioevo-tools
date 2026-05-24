param(
  [string]$OutputDir = "",
  [string]$WebBuildDir = ""
)

$ErrorActionPreference = "Stop"

function Resolve-ProjectPath([string]$relative) {
  return [System.IO.Path]::GetFullPath((Join-Path $ProjectRoot $relative))
}

function Write-Utf8NoBom([string]$Path, [string]$Content) {
  $utf8 = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Content, $utf8)
}

function Get-Sha256Hex([string]$Path) {
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try {
    $stream = [System.IO.File]::OpenRead($Path)
    try {
      $hash = $sha.ComputeHash($stream)
      return ([System.BitConverter]::ToString($hash)).Replace("-", "")
    } finally {
      $stream.Dispose()
    }
  } finally {
    $sha.Dispose()
  }
}

$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$DistRoot = Resolve-ProjectPath "dist"
$OutDir = if ($OutputDir) { [System.IO.Path]::GetFullPath($OutputDir) } else { Resolve-ProjectPath "dist\winapp" }
$WebDir = if ($WebBuildDir) { [System.IO.Path]::GetFullPath($WebBuildDir) } else { Resolve-ProjectPath "dist\public" }
$AppOut = Join-Path $OutDir "app"
$LauncherSource = Resolve-ProjectPath "windows-app\DuatCity.WinLauncher.cs"
$LauncherExe = Join-Path $OutDir "DUATCity.exe"
$Csc = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"

if (-not (Test-Path $Csc)) {
  throw "C# compiler not found: $Csc"
}
if (-not (Test-Path (Join-Path $WebDir "index.html"))) {
  throw "Web build missing. Run corepack pnpm --filter @workspace/duat-city run build first: $WebDir"
}
if (-not (Test-Path $LauncherSource)) {
  throw "Launcher source missing: $LauncherSource"
}

$resolvedOut = [System.IO.Path]::GetFullPath($OutDir)
$expectedPrefix = [System.IO.Path]::GetFullPath((Join-Path $DistRoot "winapp"))
if (-not $resolvedOut.StartsWith($expectedPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Refusing to clean output outside dist\winapp: $resolvedOut"
}

if (Test-Path $OutDir) {
  Remove-Item -LiteralPath $OutDir -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $AppOut | Out-Null
Get-ChildItem -LiteralPath $WebDir -Force | ForEach-Object {
  Copy-Item -LiteralPath $_.FullName -Destination $AppOut -Recurse -Force
}

& $Csc /nologo /target:exe /optimize+ /out:$LauncherExe $LauncherSource
if ($LASTEXITCODE -ne 0) {
  throw "csc failed with exit code $LASTEXITCODE"
}

$exeHash = Get-Sha256Hex $LauncherExe
$appFiles = Get-ChildItem -LiteralPath $AppOut -File -Recurse
$appBytes = ($appFiles | Measure-Object -Property Length -Sum).Sum
$manifest = [ordered]@{
  schema = "duat/windows-app-manifest/v1.4"
  fingerprint = "DUAT-v1.4-WINAPP-CONVERSION"
  generatedAt = (Get-Date).ToUniversalTime().ToString("o")
  wrapper = "native_dotnet_edge_app_mode"
  preferredWrappers = @("electron", "tauri")
  dependencyGate = "REVIEW_FOR_ELECTRON_TAURI_NO_LOCAL_DEPENDENCY"
  executable = [ordered]@{
    path = "dist/winapp/DUATCity.exe"
    sha256 = $exeHash
    size_bytes = (Get-Item -LiteralPath $LauncherExe).Length
  }
  app = [ordered]@{
    copied_from = "dist/public"
    copied_to = "dist/winapp/app"
    file_count = $appFiles.Count
    size_bytes = [int64]$appBytes
    provenance = "DUAT v1.4 local Vite build; no new public assets copied"
  }
  runtime = [ordered]@{
    url_path = "/duat-city/"
    loopback_only = $true
    edge_app_mode = $true
    audio_requires_user_gesture = $true
    canvas_fallback_preserved = $true
    iso3d_toggle_preserved = $true
  }
  boundaries = [ordered]@{
    publication_allowed = $false
    wabi_execution_allowed = $false
    sandbox_execution_allowed = $false
    real_apply_allowed = $false
    cloud_used = $false
    mcp_execution = $false
    unknown_zip_code_executed = $false
    assets_copied_without_provenance = $false
  }
}

$manifestJson = $manifest | ConvertTo-Json -Depth 8
Write-Utf8NoBom (Join-Path $OutDir "WINAPP_MANIFEST_v1_4.json") $manifestJson
New-Item -ItemType Directory -Force -Path (Resolve-ProjectPath "public\asset-manifest") | Out-Null
Write-Utf8NoBom (Resolve-ProjectPath "public\asset-manifest\windows_app_manifest_v1_4.json") $manifestJson

$launchCmd = @"
@echo off
setlocal
"%~dp0DUATCity.exe" %*
"@
Write-Utf8NoBom (Join-Path $OutDir "DUATCity-Launch.cmd") $launchCmd

Write-Output (@{
  ok = $true
  exe = $LauncherExe
  sha256 = $exeHash
  app_file_count = $appFiles.Count
  manifest = (Join-Path $OutDir "WINAPP_MANIFEST_v1_4.json")
} | ConvertTo-Json -Depth 4)
