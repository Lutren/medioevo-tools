
# Log Rotator: Atomically move/clear logs to prevent locking
$logPath = "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\claudio\runtime\ollama.log"
if (Test-Path $logPath) {
    $date = Get-Date -Format "yyyyMMdd-HHmmss"
    Move-Item -Path $logPath -Destination "$logPath.$date.old"
    New-Item -Path $logPath -ItemType File
    Write-Output "Log rotated: $logPath.$date.old"
}

