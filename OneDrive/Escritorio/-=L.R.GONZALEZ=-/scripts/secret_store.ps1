# Save and load wabi-sabi secrets encrypted with DPAPI (CurrentUser)
Param(
    [switch]$SaveNow,
    [switch]$LoadNow
)

$dir = Join-Path $env:USERPROFILE '.wabi_sabi'
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
$file = Join-Path $dir 'secrets.bin'

function Save-WabiSabiSecrets {
    Param(
        [string]$NVCR_TOKEN = $null,
        [string]$NGC_ACCESSKEY_ID = $null,
        [string]$NGC_ACCESSKEY_SECRET = $null,
        [string]$QWEN_API_KEY = $null
    )
    # If parameters not provided, read from user environment (SetX created them previously)
    if (-not $NVCR_TOKEN) { $NVCR_TOKEN = [Environment]::GetEnvironmentVariable('NVCR_TOKEN','User') }
    if (-not $NGC_ACCESSKEY_ID) { $NGC_ACCESSKEY_ID = [Environment]::GetEnvironmentVariable('NGC_ACCESSKEY_ID','User') }
    if (-not $NGC_ACCESSKEY_SECRET) { $NGC_ACCESSKEY_SECRET = [Environment]::GetEnvironmentVariable('NGC_ACCESSKEY_SECRET','User') }
    if (-not $QWEN_API_KEY) { $QWEN_API_KEY = [Environment]::GetEnvironmentVariable('QWEN_API_KEY','User') }

    # Use ConvertFrom-SecureString (DPAPI, tied to current user) to store encrypted strings
    $encNVCR = $null; $encAK = $null; $encSK = $null; $encQWEN = $null
    if ($NVCR_TOKEN) { $encNVCR = (ConvertTo-SecureString $NVCR_TOKEN -AsPlainText -Force | ConvertFrom-SecureString) }
    if ($NGC_ACCESSKEY_ID) { $encAK = (ConvertTo-SecureString $NGC_ACCESSKEY_ID -AsPlainText -Force | ConvertFrom-SecureString) }
    if ($NGC_ACCESSKEY_SECRET) { $encSK = (ConvertTo-SecureString $NGC_ACCESSKEY_SECRET -AsPlainText -Force | ConvertFrom-SecureString) }
    if ($QWEN_API_KEY) { $encQWEN = (ConvertTo-SecureString $QWEN_API_KEY -AsPlainText -Force | ConvertFrom-SecureString) }

    $obj = @{
        NVCR_TOKEN = $encNVCR
        NGC_ACCESSKEY_ID = $encAK
        NGC_ACCESSKEY_SECRET = $encSK
        QWEN_API_KEY = $encQWEN
    }
    $json = $obj | ConvertTo-Json -Depth 5
    [IO.File]::WriteAllText($file,$json)
    Write-Host "WabiSabi secrets saved to $file (encrypted, tied to current Windows user via DPAPI)."
}

function Load-WabiSabiSecrets {
    if (-not (Test-Path $file)) { Write-Host "No secrets file found at $file"; return }
    $json = [IO.File]::ReadAllText($file)
    $obj = ConvertFrom-Json $json
    if ($obj.NVCR_TOKEN) {
        $s = ConvertTo-SecureString $obj.NVCR_TOKEN
        $plain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
        [Environment]::SetEnvironmentVariable('NVCR_TOKEN',$plain,'Process')
    }
    if ($obj.NGC_ACCESSKEY_ID) {
        $s = ConvertTo-SecureString $obj.NGC_ACCESSKEY_ID
        $plain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
        [Environment]::SetEnvironmentVariable('NGC_ACCESSKEY_ID',$plain,'Process')
    }
    if ($obj.NGC_ACCESSKEY_SECRET) {
        $s = ConvertTo-SecureString $obj.NGC_ACCESSKEY_SECRET
        $plain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
        [Environment]::SetEnvironmentVariable('NGC_ACCESSKEY_SECRET',$plain,'Process')
    }
    if ($obj.QWEN_API_KEY) {
        $s = ConvertTo-SecureString $obj.QWEN_API_KEY
        $plain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
        [Environment]::SetEnvironmentVariable('QWEN_API_KEY',$plain,'Process')
    }
    Write-Host "WabiSabi secrets loaded into process environment (not printed)."
}

if ($SaveNow) { Save-WabiSabiSecrets }
if ($LoadNow) { Load-WabiSabiSecrets }
