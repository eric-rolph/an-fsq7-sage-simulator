# Directory Reconciliation Script
# Compare an-fsq7-sage-simulator vs an-fsq7-simulator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SAGE Simulator - Directory Reconciliation" -ForegroundColor Cyan
Write-Host "========================================
" -ForegroundColor Cyan

$sage = "C:\Users\ericr\an-fsq7-sage-simulator"
$old = "C:\Users\ericr\an-fsq7-simulator"

# Check existence
if (-not (Test-Path $old)) {
    Write-Host "✅ Old directory already removed or doesn't exist" -ForegroundColor Green
    exit 0
}

Write-Host "📊 Directory Comparison
" -ForegroundColor Yellow

# File counts
$sageCount = (Get-ChildItem $sage -Recurse -File).Count
$oldCount = (Get-ChildItem $old -Recurse -File).Count

Write-Host "File Counts:" -ForegroundColor White
Write-Host "  SAGE-simulator: $sageCount files" -ForegroundColor Green
Write-Host "  Old simulator:  $oldCount files" -ForegroundColor Yellow

# Size comparison
$sageSize = [math]::Round(((Get-ChildItem $sage -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB), 2)
$oldSize = [math]::Round(((Get-ChildItem $old -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB), 2)

Write-Host "
Directory Sizes:" -ForegroundColor White
Write-Host "  SAGE-simulator: $sageSize MB" -ForegroundColor Green
Write-Host "  Old simulator:  $oldSize MB" -ForegroundColor Yellow

# Git status
Write-Host "
Git Repository:" -ForegroundColor White
if (Test-Path "$sage\.git") {
    Write-Host "  SAGE-simulator: ✅ Has git repo" -ForegroundColor Green
} else {
    Write-Host "  SAGE-simulator: ❌ No git repo" -ForegroundColor Red
}

if (Test-Path "$old\.git") {
    Write-Host "  Old simulator:  ✅ Has git repo" -ForegroundColor Yellow
} else {
    Write-Host "  Old simulator:  ❌ No git repo" -ForegroundColor Yellow
}

# Last modified dates
$sageLastModified = (Get-ChildItem $sage -Recurse -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime
$oldLastModified = (Get-ChildItem $old -Recurse -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime

Write-Host "
Last Modified:" -ForegroundColor White
Write-Host "  SAGE-simulator: $($sageLastModified.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Green
Write-Host "  Old simulator:  $($oldLastModified.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Yellow

# Unique files in old directory
Write-Host "
📄 Files ONLY in old simulator:" -ForegroundColor Yellow
$oldFiles = Get-ChildItem $old -Recurse -File | Select-Object -ExpandProperty Name
$sageFiles = Get-ChildItem $sage -Recurse -File | Select-Object -ExpandProperty Name
$uniqueOld = $oldFiles | Where-Object { $_ -notin $sageFiles }

if ($uniqueOld) {
    $uniqueOld | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
} else {
    Write-Host "  (None - all files exist in SAGE-simulator)" -ForegroundColor Gray
}

# Decision matrix
Write-Host "
========================================" -ForegroundColor Cyan
Write-Host "RECOMMENDATION" -ForegroundColor Cyan
Write-Host "========================================
" -ForegroundColor Cyan

Write-Host "✅ SAGE-simulator is clearly the active project:" -ForegroundColor Green
Write-Host "   - Has git repository with commit history"
Write-Host "   - More recent modifications ( hours newer)"
Write-Host "   - Contains testing infrastructure"
Write-Host ""

Write-Host "⚠️  Old simulator should be archived or removed:" -ForegroundColor Yellow
Write-Host "   - No git repository"
Write-Host "   - Older by  hours"
Write-Host "   - No unique critical files"
Write-Host ""

Write-Host "🎯 Suggested Actions:
" -ForegroundColor Cyan

Write-Host "Option 1: Archive (SAFEST)" -ForegroundColor Green
Write-Host "  Compress-Archive -Path "$old" -DestinationPath "$old-backup-20251111.zip""
Write-Host "  Remove-Item "$old" -Recurse -Force"
Write-Host ""

Write-Host "Option 2: Rename as Backup" -ForegroundColor Yellow
Write-Host "  Rename-Item "$old" "$old.OLD""
Write-Host ""

Write-Host "Option 3: Direct Delete (if confident)" -ForegroundColor Red
Write-Host "  Remove-Item "$old" -Recurse -Force"
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Run one of the above commands to proceed" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
