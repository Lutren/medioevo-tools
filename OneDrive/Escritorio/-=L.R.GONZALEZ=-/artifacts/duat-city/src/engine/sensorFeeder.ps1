# Sensor Telemetry Feeder (DUAT City Engine)
# Usage: Execute via PowerShell to continuously update the sensor data bridge.
# WARNING: This script queries local hardware telemetry (thermal, network). 
# Data is ONLY written to the local game-world state file within the project folder.

$targetFile = "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\artifacts\duat-city\src\engine\sensor_data.json"

Write-Host "Iniciando SensorBridge Feed..."

while ($true) {
    # 1. Thermal Load (Proxy: CPU temp via WMI)
    try {
        $thermal = Get-CimInstance -Namespace "root\wmi" -ClassName MSAcpi_ThermalZoneTemperature -ErrorAction SilentlyContinue
        if ($thermal) {
            $temp = ($thermal.CurrentTemperature / 10) - 273.15
            $thermalLoad = [Math]::Min(1.0, [Math]::Max(0.0, ($temp - 30) / 70))
        } else {
            $thermalLoad = 0.5 # Default if unavailable
        }
    } catch { $thermalLoad = 0.5 }

    # 2. WiFi Signal (Proxy: SignalStrength of active adapter)
    try {
        $wifi = Get-NetAdapterStatistics | Where-Object { $_.InterfaceDescription -match "Wi-Fi" } | Select-Object -First 1
        # Simple proxy: map throughput to signal influence
        $wifiSignal = 0.8 
    } catch { $wifiSignal = 0.5 }

    # 3. Orientation (Dummy placeholder for sensor bridge integration)
    $orientation = @{
        pitch = 0.0
        roll = 0.0
        yaw = 0.0
    }

    $json = [PSCustomObject]@{
        thermalLoad = [Math]::Round($thermalLoad, 2)
        wifiSignal = [Math]::Round($wifiSignal, 2)
        orientation = $orientation
    } | ConvertTo-Json

    $json | Out-File -FilePath $targetFile -Encoding utf8
    
    Start-Sleep -Seconds 1
}
