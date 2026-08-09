$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "NeoMundi AI Periscope"
Write-Host "---------------------"
Write-Host ""

if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found."
    Write-Host "Copy .env.example to .env and add your API keys."
    exit 1
}

if (-not (Test-Path "config.yaml")) {
    Write-Host "ERROR: config.yaml not found."
    exit 1
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python is not installed or not available in PATH."
    exit 1
}

Write-Host "Installing/checking dependencies..."
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Starting AI Periscope..."
Write-Host ""

python periscope.py

Write-Host ""
Write-Host "Finished."
