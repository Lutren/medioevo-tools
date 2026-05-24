$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.IO.Compression.FileSystem

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ManifestDir = Join-Path $ProjectRoot "public\asset-manifest"
$DocsDir = Join-Path $ProjectRoot "docs"
$StagingDir = Join-Path $ProjectRoot "_external_review\v1_3_2"
New-Item -ItemType Directory -Force -Path $ManifestDir, $DocsDir, $StagingDir | Out-Null

$Fingerprint = "DUAT-v1.3.2-LOVABLE-ISO-EXTRACTION-VERMEER-LIGHT"
$GeneratedAt = (Get-Date).ToUniversalTime().ToString("o")
$SourceRoot = "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-"

function Write-Utf8NoBom([string]$Path, [string]$Content) {
  $encoding = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

$ZipPaths = @(
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\wabisabi_real_cli_v0_2.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\agent-foundry-os.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\client_ready_lovable_ui_i18n_assets.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\COGNITIVE_ARCHETYPES.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\Duat-Fibmob-Lab.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\lovable-project-c1214deb-51fb-453e-90aa-5353b2470e2a-2026-05-18.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_AGENT_FOLDER_v2_0.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_DUAT_LOCATION_TRADING_CARDS_BATCH_001.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_DUAT_VISUAL_BIBLE_EXTRACT_v0_2.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\project-bolt-sb1-yvfmocrc.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\Prompt-Analyzer.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\wabisabi_cli_provider_patch_v0_1.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Duat-Fibmob-Lab.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\lovable-project-b08d75ee-a06a-4ec9-bbc8-7837b3f19692-2026-05-20.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\MEDIOEVO_OSIT_AI_HUMAN_PACKET_2026-05-19.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\07_LORE_LIBROS.zip"
)

function Get-StackTags([string]$Path) {
  $p = $Path.ToLowerInvariant()
  $tags = New-Object System.Collections.Generic.List[string]
  if ($p -match "react-three|@react-three|r3f") { $tags.Add("React Three Fiber") }
  if ($p -match "three|webgl|gltf|glb") { $tags.Add("Three.js/WebGL") }
  if ($p -match "drei|orbitcontrols|camera-controls") { $tags.Add("Drei/camera controls") }
  if ($p -match "canvas|getcontext|ctx\.") { $tags.Add("Canvas") }
  if ($p -match "css3d|preserve-3d|perspective") { $tags.Add("CSS 3D") }
  if ($p -match "iso|isometric|tilemap|tileset|grid") { $tags.Add("Isometric grid") }
  if ($p -match "light|shadow|bloom|postprocess|composer|fxaa") { $tags.Add("Light/postprocess") }
  if ($p -match "sprite|billboard|agent|character") { $tags.Add("Sprite/billboard") }
  if ($p -match "i18n|locale|translation|lang") { $tags.Add("i18n") }
  if ($p -match "visual.?bible|style.?guide|palette|moodboard") { $tags.Add("Visual bible") }
  if ($p -match "duat|osit|medioevo|wabi|fibmob") { $tags.Add("DUAT/MEDIOEVO") }
  if ($tags.Count -eq 0) { $tags.Add("unknown") }
  return @($tags)
}

function Get-TypeTag([string]$Path) {
  $p = $Path.ToLowerInvariant()
  if ($p -match "react-three|@react-three|r3f") { return "react_three_fiber" }
  if ($p -match "three|webgl|gltf|glb") { return "three" }
  if ($p -match "drei|orbitcontrols|camera-controls") { return "drei" }
  if ($p -match "canvas|getcontext|ctx\.") { return "canvas" }
  if ($p -match "css3d|preserve-3d|perspective") { return "css_3d" }
  if ($p -match "iso|isometric|tilemap|tileset|grid") { return "isometric_grid" }
  if ($p -match "light|shadow|bloom|postprocess|composer|fxaa") { return "lighting" }
  if ($p -match "sprite|billboard|agent|character") { return "billboard_sprite" }
  if ($p -match "component|panel|toolbar|hud|tsx$") { return "ui_panel" }
  if ($p -match "i18n|locale|translation|lang") { return "i18n_asset" }
  if ($p -match "visual.?bible|style.?guide|palette|moodboard") { return "visual_bible" }
  if ($p -match "duat|osit|medioevo|wabi|fibmob") { return "duat_component" }
  return "unknown"
}

function Get-UsefulFor([string]$Type) {
  switch ($Type) {
    "react_three_fiber" { return @("iso3d shell", "camera routing") }
    "three" { return @("iso3d shell", "lighting reference") }
    "drei" { return @("camera controls", "zoom interaction") }
    "canvas" { return @("canvas fallback") }
    "isometric_grid" { return @("isometric city routing", "tile depth sorting") }
    "lighting" { return @("Vermeer light behavior", "render budget") }
    "billboard_sprite" { return @("2d pixel population") }
    "ui_panel" { return @("mode director UI") }
    "i18n_asset" { return @("UI language assets") }
    "visual_bible" { return @("art direction reference") }
    "duat_component" { return @("DUAT integration reference") }
    default { return @("unknown") }
  }
}

function New-Record([string]$EntryPath, [string]$ZipName, [Int64]$Size) {
  $type = Get-TypeTag $EntryPath
  $ext = [System.IO.Path]::GetExtension($EntryPath).TrimStart(".").ToLowerInvariant()
  $runtimeCode = @("ts","tsx","js","jsx","mjs","cjs","vue","svelte") -contains $ext
  $requiresDep = $EntryPath -match "@react-three|three|drei|postprocess|composer|webgl"
  $recommendation = if ($type -in @("react_three_fiber","three","drei","isometric_grid","lighting","billboard_sprite","canvas")) { "adapt" } elseif ($type -in @("ui_panel","i18n_asset","visual_bible","duat_component")) { "reference_only" } else { "reject" }
  $risk = if ($runtimeCode) { "high" } elseif ($requiresDep) { "medium" } else { "low" }
  [pscustomobject]@{
    path = $EntryPath
    source_zip = $ZipName
    type = $type
    stack_detected = @(Get-StackTags $EntryPath)
    useful_for = @(Get-UsefulFor $type)
    risk = $risk
    integration_recommendation = $recommendation
    reason = if ($recommendation -eq "reject") { "No renderer-relevant signal found." } else { "Renderer/UI/art-direction signal detected from path metadata." }
    requires_dependency = [bool]$requiresDep
    unknown_code_execution_risk = $false
    size_bytes = $Size
    notes = "Read-only metadata scan. No zip code executed; concepts must be adapted through local DUAT adapter."
  }
}

$allRecords = New-Object System.Collections.Generic.List[object]
$missing = New-Object System.Collections.Generic.List[object]

foreach ($zipPath in $ZipPaths) {
  if (-not (Test-Path -LiteralPath $zipPath)) {
    $missing.Add([pscustomobject]@{ path = $zipPath; status = "MISSING_LOCAL_PATH" })
    continue
  }
  $zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
  try {
    foreach ($entry in $zip.Entries) {
      if ([string]::IsNullOrWhiteSpace($entry.FullName) -or $entry.FullName.EndsWith("/")) { continue }
      $record = New-Record $entry.FullName ([System.IO.Path]::GetFileName($zipPath)) $entry.Length
      if ($record.integration_recommendation -ne "reject") { $allRecords.Add($record) }
    }
  } finally {
    $zip.Dispose()
  }
}

$rendererRecords = @($allRecords | Where-Object { $_.type -in @("react_three_fiber","three","drei","canvas","css_3d","isometric_grid","lighting","billboard_sprite","duat_component") } | Select-Object -First 900)
$isoRecords = @($allRecords | Where-Object { $_.type -in @("react_three_fiber","three","drei","css_3d","isometric_grid","lighting","billboard_sprite") } | Select-Object -First 600)
$uiRecords = @($allRecords | Where-Object { $_.type -in @("ui_panel","i18n_asset","duat_component") } | Select-Object -First 600)
$visualRecords = @($allRecords | Where-Object { $_.type -eq "visual_bible" -or $_.path -match "palette|style|mood|visual|bible|trading|card|asset" } | Select-Object -First 600)

function New-Manifest([string]$Schema, [object[]]$Records) {
  [ordered]@{
    schema = $Schema
    fingerprint = $Fingerprint
    generated_at = $GeneratedAt
    source_root = $SourceRoot
    records = @($Records)
    missing_paths = @($missing.ToArray())
    boundary = [ordered]@{
      metadata_only = $true
      unknown_code_executed = $false
      publication_allowed = $false
      no_raw_source_adoption = $true
      staging_dir = "_external_review/v1_3_2"
    }
  }
}

New-Manifest "duat/forensics/lovable-renderer-candidates/v1.3.2" $rendererRecords |
  ConvertTo-Json -Depth 10 | ForEach-Object { Write-Utf8NoBom (Join-Path $ManifestDir "lovable_renderer_candidates_v1_3_2.json") $_ }
New-Manifest "duat/forensics/isometric-renderer-inventory/v1.3.2" $isoRecords |
  ConvertTo-Json -Depth 10 | ForEach-Object { Write-Utf8NoBom (Join-Path $ManifestDir "isometric_renderer_inventory_v1_3_2.json") $_ }
New-Manifest "duat/forensics/ui-i18n-assets-inventory/v1.3.2" $uiRecords |
  ConvertTo-Json -Depth 10 | ForEach-Object { Write-Utf8NoBom (Join-Path $ManifestDir "ui_i18n_assets_inventory_v1_3_2.json") $_ }
New-Manifest "duat/forensics/visual-bible-inventory/v1.3.2" $visualRecords |
  ConvertTo-Json -Depth 10 | ForEach-Object { Write-Utf8NoBom (Join-Path $ManifestDir "visual_bible_inventory_v1_3_2.json") $_ }

[ordered]@{
  schema = "duat/external-review/staging-metadata/v1.3.2"
  fingerprint = $Fingerprint
  generated_at = $GeneratedAt
  zip_count_requested = $ZipPaths.Count
  zip_count_found = ($ZipPaths.Count - $missing.Count)
  record_count = $allRecords.Count
  missing_paths = @($missing.ToArray())
  boundary = "METADATA_ONLY_NO_EXECUTION_NO_PUBLICATION"
} | ConvertTo-Json -Depth 8 | ForEach-Object { Write-Utf8NoBom (Join-Path $StagingDir "zip_metadata_inventory_v1_3_2.json") $_ }

@"
# DUAT v1.3.2 External Review Staging

Boundary: METADATA_ONLY_NO_EXECUTION_NO_PUBLICATION.

This folder stores review metadata for Lovable/isometric renderer forensics.
No code from zips was executed. No assets were copied into public release.
"@ | ForEach-Object { Write-Utf8NoBom (Join-Path $StagingDir "STAGING_BOUNDARY.md") $_ }

Write-Output "renderer_records=$($rendererRecords.Count)"
Write-Output "iso_records=$($isoRecords.Count)"
Write-Output "ui_records=$($uiRecords.Count)"
Write-Output "visual_records=$($visualRecords.Count)"
Write-Output "missing_paths=$($missing.Count)"
