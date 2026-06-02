# Wrapper so "git" works even when Git is not in PATH yet.
$gitExe = "C:\Program Files\Git\cmd\git.exe"
if (-not (Test-Path $gitExe)) {
    Write-Error "Git not installed: https://git-scm.com/download/win"
}
& $gitExe @args
