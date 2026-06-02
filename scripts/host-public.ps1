$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$python = ".\.venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    throw "Virtual env not found. Run: python -m venv .venv && .\.venv\Scripts\pip install -r requirements\dev.txt"
}

Write-Host "Applying migrations and syncing media..."
& $python manage.py migrate --noinput
& $python manage.py sync_bundled_media
& $python manage.py collectstatic --noinput

Write-Host ""
Write-Host "Starting Django on http://127.0.0.1:8000 ..."
Start-Process -FilePath $python -ArgumentList "manage.py","runserver","0.0.0.0:8000" -WorkingDirectory (Get-Location)

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Opening public tunnel (localhost.run via SSH)..."
Write-Host "Copy the https://....lhr.life link below — it works from any network."
Write-Host "Keep this window open. Closing it stops public access."
Write-Host ""

ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 80:127.0.0.1:8000 nokey@localhost.run
