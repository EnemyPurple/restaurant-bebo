# Publish restaurant-bebo: push to GitHub and open Render deploy.
$ErrorActionPreference = "Stop"

$gitCmd = "C:\Program Files\Git\cmd"
$gitBin = "C:\Program Files\Git\bin"
if (Test-Path $gitCmd) {
    $env:Path = "$gitCmd;$gitBin;" + $env:Path
} else {
    Write-Error "Git not found. Install from https://git-scm.com/download/win"
}

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root

$remote = "https://github.com/EnemyPurple/restaurant-bebo.git"
$existing = git remote get-url origin 2>$null
if (-not $existing) {
    git remote add origin $remote
} elseif ($existing -ne $remote) {
    git remote set-url origin $remote
}

git branch -M main
$status = git status --porcelain
if ($status) {
    git add -A
    git -c user.name="EnemyPurple" -c user.email="EnemyPurple@users.noreply.github.com" commit -m "Update project"
}
git push -u origin main

Write-Host ""
Write-Host "GitHub: https://github.com/EnemyPurple/restaurant-bebo" -ForegroundColor Green
Write-Host ""
Write-Host "Opening Render Blueprint setup..." -ForegroundColor Cyan
Write-Host "1. Sign in with GitHub if asked"
Write-Host "2. Select repo: EnemyPurple/restaurant-bebo"
Write-Host "3. Click Apply on render.yaml"
Write-Host "4. Set ADMIN_PASSWORD (e.g. qawsea123) and deploy"
Write-Host ""

Start-Process "https://dashboard.render.com/select-repo?type=blueprint"
