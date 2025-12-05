# Setup script for AI Insights Service
Write-Host "Setting up AI Insights Service..." -ForegroundColor Green
Write-Host ""

# Navigate to ai-insights-service directory
Set-Location $PSScriptRoot

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created ✓" -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists ✓" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment and install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "AI Insights Service setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Update DATABASE_URL in .env file with your PostgreSQL credentials" -ForegroundColor White
Write-Host "2. Run: python -m uvicorn app.main:app --reload" -ForegroundColor White
Write-Host ""
