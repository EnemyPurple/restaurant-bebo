# Регистрирует автозапуск watchdog при входе в Windows (локальный туннель).
$ErrorActionPreference = "Stop"

$taskName = "BeboRestaurantTunnel"
$scriptPath = Join-Path $PSScriptRoot "tunnel-watchdog.ps1"
$projectRoot = Split-Path $PSScriptRoot -Parent
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    throw "Сначала создайте venv: python -m venv .venv"
}

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" -WorkingDirectory $projectRoot
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null

Write-Host "Autostart enabled: task '$taskName'"
Write-Host "Public URL will be saved to tools\public-url.txt"
Write-Host ""
Write-Host "Run now: Start-ScheduledTask -TaskName '$taskName'"
Write-Host "Disable: Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false"
