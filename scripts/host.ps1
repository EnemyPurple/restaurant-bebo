$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$python = ".\.venv\Scripts\python.exe"
$cloudflared = ".\tools\cloudflared.exe"

if (-not (Test-Path $python)) {
    throw "Virtual env not found. Run: python -m venv .venv && .\.venv\Scripts\pip install -r requirements\dev.txt"
}

Write-Host "Applying migrations (DB is preserved in dev)..."
& $python manage.py migrate --noinput
Write-Host "Syncing photo files only (BUNDLED_MEDIA_MODE=preserve in .env)..."
& $python manage.py sync_bundled_media
& $python manage.py collectstatic --noinput

Write-Host "Starting Django on http://0.0.0.0:8000 ..."
Start-Process -FilePath $python -ArgumentList "manage.py","runserver","0.0.0.0:8000" -WorkingDirectory (Get-Location)

Start-Sleep -Seconds 3

if (Test-Path $cloudflared) {
    Write-Host ""
    Write-Host "Public URL will appear below (copy the https://....trycloudflare.com link):"
    Write-Host "Keep this window open — closing it stops public access."
    Write-Host ""
    & $cloudflared tunnel --url http://127.0.0.1:8000 --no-autoupdate
} else {
    Write-Host "cloudflared not found in tools/. Site is available on LAN: http://<your-ip>:8000"
}
