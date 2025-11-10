# PowerShell Setup Script for AN/FSQ-7 Simulator
# Run this script to install and launch the simulator

Write-Host "===============================================" -ForegroundColor Green
Write-Host "  AN/FSQ-7 SAGE Computer Simulator Setup" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Check Python version
Write-Host "Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    $versionMatch = [regex]::Match($pythonVersion, "(\d+)\.(\d+)")
    $major = [int]$versionMatch.Groups[1].Value
    $minor = [int]$versionMatch.Groups[2].Value
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "✗ Python 3.8 or higher required. Please upgrade Python." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install dependencies." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
Write-Host ""

# Initialize Reflex
Write-Host "Initializing Reflex application..." -ForegroundColor Cyan
if (-not (Test-Path ".web")) {
    reflex init --loglevel warning
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to initialize Reflex." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✓ Reflex initialized successfully" -ForegroundColor Green
} else {
    Write-Host "✓ Reflex already initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Starting the simulator..." -ForegroundColor Cyan
Write-Host "Once the server starts, open your browser to:" -ForegroundColor Yellow
Write-Host "  http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Gray
Write-Host ""

# Run the simulator
reflex run
