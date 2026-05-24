# Load authorized local provider credentials into the current PowerShell
# process only. This script does not print, commit or persist secret values
# unless -PersistUser is explicitly passed.
Param(
    [string]$Path = "C:\Users\L-Tyr\OneDrive\Escritorio\Formal\bu\banananana.txt",
    [switch]$Force,
    [switch]$EnableCloud,
    [switch]$PersistUser
)

if (-not (Test-Path -LiteralPath $Path)) {
    Write-Host "File not found: $Path" -ForegroundColor Red
    exit 1
}

if (-not $Force) {
    $consent = Read-Host "This will read credentials from $Path and set process env vars without printing secrets. Continue? (yes/no)"
    if ($consent -ne 'yes') {
        Write-Host "Aborted by user."
        exit 1
    }
}

$content = Get-Content -LiteralPath $Path -ErrorAction Stop
$raw = $content -join "`n"
$loaded = New-Object System.Collections.Generic.List[string]

function Set-SecretEnv {
    Param(
        [string]$Name,
        [string]$Value
    )
    if ([string]::IsNullOrWhiteSpace($Value)) { return }
    [Environment]::SetEnvironmentVariable($Name, $Value.Trim(), 'Process')
    if ($PersistUser) {
        [Environment]::SetEnvironmentVariable($Name, $Value.Trim(), 'User')
    }
    $loaded.Add($Name) | Out-Null
}

function First-RegexValue {
    Param(
        [string]$Text,
        [string]$Pattern
    )
    $m = [regex]::Match($Text, $Pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if ($m.Success) { return $m.Groups[1].Value }
    return ""
}

$nvidiaApiKey = First-RegexValue $raw '(nvapi-[A-Za-z0-9_\-]{16,})'
Set-SecretEnv 'NVIDIA_API_KEY' $nvidiaApiKey
Set-SecretEnv 'NVIDIA_NIM_API_KEY' $nvidiaApiKey

$openAiKey = First-RegexValue $raw '(?m)^\s*OPENAI_API_KEY\s*[:=]\s*["'']?([^"''\s]+)'
Set-SecretEnv 'OPENAI_API_KEY' $openAiKey

$qwenKey = First-RegexValue $raw '(?m)^\s*(?:QWEN_API_KEY|DASHSCOPE_API_KEY)\s*[:=]\s*["'']?([^"''\s]+)'
Set-SecretEnv 'QWEN_API_KEY' $qwenKey
Set-SecretEnv 'DASHSCOPE_API_KEY' $qwenKey

$deepseekKey = First-RegexValue $raw '(?m)^\s*DEEPSEEK_API_KEY\s*[:=]\s*["'']?([^"''\s]+)'
Set-SecretEnv 'DEEPSEEK_API_KEY' $deepseekKey

$mistralKey = First-RegexValue $raw '(?m)^\s*MISTRAL_API_KEY\s*[:=]\s*["'']?([^"''\s]+)'
Set-SecretEnv 'MISTRAL_API_KEY' $mistralKey

$minimaxKey = First-RegexValue $raw '(?m)^\s*MINIMAX_API_KEY\s*[:=]\s*["'']?([^"''\s]+)'
Set-SecretEnv 'MINIMAX_API_KEY' $minimaxKey

$moonshotKey = First-RegexValue $raw '(?m)^\s*(?:MOONSHOT_API_KEY|KIMI_API_KEY)\s*[:=]\s*["'']?([^"''\s]+)'
Set-SecretEnv 'MOONSHOT_API_KEY' $moonshotKey
Set-SecretEnv 'KIMI_API_KEY' $moonshotKey

for ($i = 0; $i -lt $content.Count; $i++) {
    if ($content[$i] -match 'AccessKey ID' -and $i + 1 -lt $content.Count) {
        Set-SecretEnv 'NGC_ACCESSKEY_ID' $content[$i + 1]
    }
    if ($content[$i] -match 'AccessKey Secret' -and $i + 1 -lt $content.Count) {
        Set-SecretEnv 'NGC_ACCESSKEY_SECRET' $content[$i + 1]
    }
    if ($content[$i] -match 'Password:\s*(.+)$') {
        Set-SecretEnv 'NVCR_TOKEN' $Matches[1]
    }
}

if ($EnableCloud) {
    [Environment]::SetEnvironmentVariable('WABI_ALLOW_CLOUD_PROVIDERS', '1', 'Process')
    $loaded.Add('WABI_ALLOW_CLOUD_PROVIDERS') | Out-Null
}

[Environment]::SetEnvironmentVariable('WABI_CLOUD_MAX_TOKENS', '128', 'Process')
$loaded.Add('WABI_CLOUD_MAX_TOKENS') | Out-Null

$unique = $loaded | Sort-Object -Unique
Write-Host ("Loaded env vars: " + (($unique | ForEach-Object { $_ }) -join ', ')) -ForegroundColor Green
Write-Host "Secret values were not printed." -ForegroundColor Green
if ($PersistUser) {
    Write-Host "Values were persisted to the current Windows user environment by explicit request." -ForegroundColor Yellow
} else {
    Write-Host "Values are process/session-only. Dot-source this script before running Wabi commands." -ForegroundColor Yellow
}
