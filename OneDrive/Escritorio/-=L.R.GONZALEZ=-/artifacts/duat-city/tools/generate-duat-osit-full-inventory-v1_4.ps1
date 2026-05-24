$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression.FileSystem

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ManifestDir = Join-Path $ProjectRoot "public\asset-manifest"
$DocsDir = Join-Path $ProjectRoot "docs"
$StagingDir = Join-Path $ProjectRoot "_external_review\v1_4"
New-Item -ItemType Directory -Force -Path $ManifestDir, $DocsDir, $StagingDir | Out-Null

$Fingerprint = "DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL"
$GeneratedAt = (Get-Date).ToUniversalTime().ToString("o")

function Write-Utf8NoBom([string]$Path, [string]$Content) {
  $encoding = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

$Sources = @(
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Screenshot 2026-05-20 020022.png",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\07_LORE_LIBROS.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Duat-Fibmob-Lab.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\lovable-project-b08d75ee-a06a-4ec9-bbc8-7837b3f19692-2026-05-20.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\MEDIOEVO_OSIT_AI_HUMAN_PACKET_2026-05-19.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Assets Du WABI",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\MEDIOEVO_OSIT_AI_HUMAN_PACKET_2026-05-19\09_MEDIOEVO_OSIT_AI_HUMAN_PACKET_COMPLETO.pdf",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\agent-foundry-os.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\client_ready_lovable_ui_i18n_assets.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\COGNITIVE_ARCHETYPES.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\Duat-Fibmob-Lab.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\files.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\lovable-project-c1214deb-51fb-453e-90aa-5353b2470e2a-2026-05-18.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_AGENT_FOLDER_v2_0.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_DUAT_LOCATION_TRADING_CARDS_BATCH_001.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_DUAT_VISUAL_BIBLE_EXTRACT_v0_2.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_OSIT_DOCUMENTOS_ACTUALIZADOS_TRUTHGATE_EIC_v0_3_2026-05-17.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_OSIT_DOCUMENTOS_FORMALIZADOS_v2_1_2026-05-17.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_OSIT_KNOWLEDGE_FOLDER_v1_0.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_OSIT_PORTAFOLIO_HUMANO_IA_2026-05-15.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_OSIT_TEORIAS_COMUNICACION_CONSCIENCIA_v0_1_2026-05-17.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_OSIT_TRABAJO_MEJORADO_v0_2_2026-05-17.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\MEDIOEVO_OSIT_v12_2_6_ACTIVE_SAFEBOUNDARY_SCIENCE_PATCHED.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\project-bolt-sb1-yvfmocrc.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\Prompt-Analyzer.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\wabisabi_cli_provider_patch_v0_1.zip",
  "C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Back up if integrated all, telete all\2026-05-19_consolidated_from_root\wabisabi_real_cli_v0_2.zip"
)

function Classify-Use([string]$Path) {
  $p = $Path.ToLowerInvariant()
  $uses = New-Object System.Collections.Generic.List[string]
  if ($p -match "lovable|isometric|visual|assets|screenshot|trading|cards") { $uses.Add("visual_renderer_assets") }
  if ($p -match "wabi|cli|agent-foundry|prompt") { $uses.Add("agent_orchestration") }
  if ($p -match "osit|truthgate|science|teorias|knowledge|lore|libros") { $uses.Add("osit_language_lore") }
  if ($p -match "fibmob|physics|duat") { $uses.Add("pixel_light_game_engine") }
  if ($uses.Count -eq 0) { $uses.Add("review_required") }
  return @($uses)
}

function Classify-Recommendation([string]$Path, [Int64]$SizeBytes, [bool]$IsDirectory) {
  $p = $Path.ToLowerInvariant()
  if ($IsDirectory) { return "reference_only" }
  if ($SizeBytes -gt 50MB) { return "metadata_only_large_source" }
  if ($p -match "\.zip$") { return "selective_extract_review_required" }
  if ($p -match "\.(png|jpg|jpeg|webp|gif|pdf)$") { return "reference_only" }
  return "review_required"
}

function Get-ObservacionismoState([string]$Recommendation, [bool]$Exists) {
  if (-not $Exists) {
    return [ordered]@{ R=0.62; Phi_eff=0.38; regime="SATURADO"; action_gate="BLOCK"; reason="missing_local_path" }
  }
  switch ($Recommendation) {
    "reference_only" {
      return [ordered]@{ R=0.28; Phi_eff=0.68; regime="FUNCIONAL"; action_gate="REVIEW"; reason="license_unknown_reference_only" }
    }
    "selective_extract_review_required" {
      return [ordered]@{ R=0.34; Phi_eff=0.64; regime="FUNCIONAL_REVIEW"; action_gate="REVIEW"; reason="selective_extraction_requires_allowlist_hash_tests" }
    }
    "metadata_only_large_source" {
      return [ordered]@{ R=0.43; Phi_eff=0.56; regime="CARGADO"; action_gate="REVIEW"; reason="large_source_raw_wholesale_blocked" }
    }
    default {
      return [ordered]@{ R=0.37; Phi_eff=0.60; regime="FUNCIONAL_REVIEW"; action_gate="REVIEW"; reason="unknown_review_required" }
    }
  }
}

$records = New-Object System.Collections.Generic.List[object]
$entryRecords = New-Object System.Collections.Generic.List[object]
$foundCount = 0

foreach ($source in $Sources) {
  $exists = Test-Path -LiteralPath $source
  if (-not $exists) {
    $records.Add([ordered]@{ path=$source; exists=$false; status="MISSING_LOCAL_PATH"; recommendation="review_required"; observacionismo_state=(Get-ObservacionismoState "review_required" $false); public_safe_guess="review"; publication_allowed=$false })
    continue
  }
  $foundCount += 1
  $item = Get-Item -LiteralPath $source
  $size = if ($item.PSIsContainer) { 0 } else { $item.Length }
  $recommendation = Classify-Recommendation $source $size $item.PSIsContainer
  $observacionismoState = Get-ObservacionismoState $recommendation $true
  $entryCount = 0
  $sampleEntries = @()
  if (-not $item.PSIsContainer -and $item.Extension.ToLowerInvariant() -eq ".zip") {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($source)
    try {
      $entryCount = $zip.Entries.Count
      $sampleEntries = @($zip.Entries | Select-Object -First 40 | ForEach-Object { $_.FullName })
      foreach ($entry in ($zip.Entries | Select-Object -First 250)) {
        if ([string]::IsNullOrWhiteSpace($entry.FullName) -or $entry.FullName.EndsWith("/")) { continue }
        $entryRecords.Add([ordered]@{
          source = $item.Name
          path = $entry.FullName
          extension = [System.IO.Path]::GetExtension($entry.FullName).TrimStart(".").ToLowerInvariant()
          size_bytes = $entry.Length
          useful_for = @(Classify-Use $entry.FullName)
          copy_status = "not_copied"
          execution_status = "not_executed"
          recommendation = "reference_only_or_adapt_after_review"
        })
      }
    } finally {
      $zip.Dispose()
    }
  } elseif ($item.PSIsContainer) {
    $entryCount = (Get-ChildItem -LiteralPath $source -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
    $sampleEntries = @(Get-ChildItem -LiteralPath $source -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 40 | ForEach-Object { $_.FullName })
  }
  $records.Add([ordered]@{
    path = $source
    filename = $item.Name
    exists = $true
    type = if ($item.PSIsContainer) { "directory" } elseif ($item.Extension.ToLowerInvariant() -eq ".zip") { "zip" } else { $item.Extension.TrimStart(".").ToLowerInvariant() }
    size_bytes = $size
    entry_count = $entryCount
    useful_for = @(Classify-Use $source)
    recommendation = $recommendation
    observacionismo_state = $observacionismoState
    extraction_status = if ($recommendation -eq "metadata_only_large_source") { "metadata_only_raw_wholesale_blocked" } else { "metadata_only_selective_staging_ready" }
    copy_status = "not_copied_to_public"
    license_status = "unknown_review_required"
    public_safe_guess = "review"
    publication_allowed = $false
    unknown_code_executed = $false
    sample_entries = @($sampleEntries)
  })
}

$manifest = [ordered]@{
  schema = "duat/osit-full-source-inventory/v1.4"
  fingerprint = $Fingerprint
  generated_at = $GeneratedAt
  source_count = $Sources.Count
  found_count = $foundCount
  records = @($records.ToArray())
  sampled_zip_entries = @($entryRecords.ToArray())
  staging = [ordered]@{
    path = "_external_review/v1_4"
    mode = "metadata_only_selective_extraction"
    raw_wholesale_extraction = "BLOCKED_BY_SOURCE_ADOPTION_LAW"
  }
  module_observacionismo = [ordered]@{
    visual_renderer_assets = [ordered]@{ R=0.34; Phi_eff=0.64; regime="FUNCIONAL_REVIEW"; action_gate="REVIEW"; reason="assets and renderer candidates are useful but license/provenance reviewed only" }
    agent_orchestration = [ordered]@{ R=0.32; Phi_eff=0.66; regime="FUNCIONAL_REVIEW"; action_gate="REVIEW"; reason="Wabi/agent code remains proposal/design-only; no execution" }
    osit_language_lore = [ordered]@{ R=0.38; Phi_eff=0.61; regime="FUNCIONAL_REVIEW"; action_gate="REVIEW"; reason="lore and formulas require ScienceClaimGate/public boundary" }
    pixel_light_game_engine = [ordered]@{ R=0.36; Phi_eff=0.62; regime="FUNCIONAL_REVIEW"; action_gate="REVIEW"; reason="large physics/light sources require selective adaptation only" }
  }
  boundary = [ordered]@{
    metadata_only = $true
    unknown_code_executed = $false
    assets_copied_to_public = $false
    publication_allowed = $false
    cloud_used = $false
    mcp_execution = $false
  }
}

Write-Utf8NoBom (Join-Path $ManifestDir "duat_osit_full_sources_manifest_v1_4.json") ($manifest | ConvertTo-Json -Depth 12)
Write-Utf8NoBom (Join-Path $StagingDir "STAGING_BOUNDARY.md") "# DUAT OSIT v1.4 staging`n`nMetadata-only selective staging. Raw wholesale extraction remains blocked by source-adoption law. No unknown code executed. No assets copied to public."

Write-Output "sources=$($Sources.Count)"
Write-Output "found=$($manifest.found_count)"
Write-Output "sampled_entries=$($entryRecords.Count)"
