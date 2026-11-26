# 1-Click Git Auto-Sync PowerShell Utility
Param(
    [string]$Message = ""
)

$RepoDir = Split-Path -Parent $PSScriptRoot
Set-Location $RepoDir

Write-Host "🔍 Checking git status in $RepoDir..." -ForegroundColor Cyan

$status = git status --porcelain
if (-not $status) {
    Write-Host "ℹ️ Working tree clean. No changes to commit." -ForegroundColor Green
    exit 0
}

$branch = git branch --show-current
if (-not $branch) { $branch = "main" }

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMsg = if ($Message) { $Message } else { "Auto-sync: project updates [$timestamp]" }

Write-Host "📦 Staging all project changes..." -ForegroundColor Yellow
git add -A

Write-Host "💾 Creating commit: '$commitMsg'..." -ForegroundColor Yellow
git commit -m "$commitMsg"

Write-Host "🚀 Pushing to origin/$branch..." -ForegroundColor Cyan
git push origin $branch

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Successfully synchronized with GitHub!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Notice during push (check remote credentials/permissions)." -ForegroundColor Magenta
}
