Param(
    [switch]$Force
)

$path = "C:\Users\L-Tyr\OneDrive\Escritorio\Formal\banananana.txt"
if (-not (Test-Path $path)) { Write-Host "File not found: $path" -ForegroundColor Red; exit 1 }

if (-not $Force) {
    $consent = Read-Host "Esto persistirá credenciales como variables de usuario (SetX). Continuar? (yes/no)"
    if ($consent -ne 'yes') { Write-Host "Abortado por usuario."; exit }
}

$content = Get-Content $path -ErrorAction Stop

$nvcr_token = ($content | Where-Object { $_ -match 'Password:' -or $_ -match '^a2I' } ) | Select-Object -First 1
$ak=''; $sk=''
for ($i=0; $i -lt $content.Count; $i++) {
    if ($content[$i] -match 'AccessKey ID') { $ak = $content[$i+1].Trim() }
    if ($content[$i] -match 'AccessKey Secret') { $sk = $content[$i+1].Trim() }
}

if ($nvcr_token) { & setx NVCR_TOKEN $nvcr_token }
if ($ak) { & setx NGC_ACCESSKEY_ID $ak }
if ($sk) { & setx NGC_ACCESSKEY_SECRET $sk }

Write-Host "Credenciales persistidas en variables de usuario (SetX). Reinicia la sesión para que estén en el entorno global de usuario." -ForegroundColor Green
