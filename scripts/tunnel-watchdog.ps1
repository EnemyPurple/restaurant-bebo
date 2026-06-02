$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$python = ".\.venv\Scripts\python.exe"
$logDir = Join-Path (Get-Location) "tools"
$logFile = Join-Path $logDir "tunnel-watchdog.log"
$publicUrlFile = Join-Path $logDir "public-url.txt"
$djangoPort = 8000

function Write-Log($msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $msg"
    Add-Content -Path $logFile -Value $line
    Write-Host $line
}

function Test-LocalSite {
    try {
        $code = (Invoke-WebRequest -Uri "http://127.0.0.1:$djangoPort/" -UseBasicParsing -TimeoutSec 5).StatusCode
        return $code -eq 200
    } catch {
        return $false
    }
}

function Stop-DjangoOnPort {
    $lines = netstat -ano | Select-String ":$djangoPort\s+.*LISTENING"
    foreach ($line in $lines) {
        $procId = ($line -split '\s+')[-1]
        if ($procId -match '^\d+$') {
            Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
        }
    }
    Start-Sleep -Seconds 1
}

function Start-Django {
    if (Test-LocalSite) { return }
    Write-Log "Starting Django..."
    Start-Process -FilePath $python -ArgumentList "manage.py","runserver","127.0.0.1:$djangoPort" -WorkingDirectory (Get-Location) -WindowStyle Hidden
    Start-Sleep -Seconds 4
}

function Start-Tunnel {
    Write-Log "Starting SSH tunnel..."
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "ssh"
    $psi.Arguments = "-o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ExitOnForwardFailure=yes -R 80:127.0.0.1:$djangoPort nokey@localhost.run"
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $proc = [System.Diagnostics.Process]::Start($psi)

    $deadline = (Get-Date).AddSeconds(45)
    $url = $null
    while ((Get-Date) -lt $deadline -and -not $proc.HasExited) {
        while (-not $proc.StandardOutput.EndOfStream) {
            $line = $proc.StandardOutput.ReadLine()
            if ($line -match "(https://[a-z0-9]+\.lhr\.life)") {
                $url = $Matches[1]
                break
            }
        }
        if ($url) { break }
        Start-Sleep -Milliseconds 300
    }

    if ($url) {
        Set-Content -Path $publicUrlFile -Value $url -Encoding utf8
        Write-Log "Public URL: $url"
    } else {
        Write-Log "Tunnel started but URL not captured yet."
    }

    return $proc
}

Write-Log "Watchdog started."

& $python manage.py migrate --noinput | Out-Null
& $python manage.py sync_bundled_media | Out-Null

Stop-DjangoOnPort
Start-Django

while ($true) {
    if (-not (Test-LocalSite)) {
        Write-Log "Django down, restarting."
        Start-Django
    }

    $tunnel = Start-Tunnel
    if ($tunnel) {
        $tunnel.WaitForExit()
        Write-Log "Tunnel exited with code $($tunnel.ExitCode). Restarting in 5s."
    }
    Start-Sleep -Seconds 5
}
