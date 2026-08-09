$ErrorActionPreference = "Stop"

# ============================================================
# NeoMundi AI Periscope — v0.1.0
#
# HOW TO USE
#
# 1. Add your NeoMundi ControlTower API key below.
# 2. Add the API key of the provider you want to use.
# 3. Configure provider, model, prompt_file and runs_per_prompt
#    in config.yaml.
# 4. Run this file.
#
# Supported providers are maintained in the official
# NeoMundi ControlTower documentation.
# ============================================================


# ============================================================
# USER API KEYS
# ============================================================

$NEOMUNDI_API_KEY = ""
$PROVIDER_API_KEY = ""


# ============================================================
# START
# ============================================================

Write-Host ""
Write-Host "========================================="
Write-Host "       NeoMundi AI Periscope"
Write-Host "             v0.1.0"
Write-Host "========================================="
Write-Host ""


# ============================================================
# CHECK REQUIRED FILES
# ============================================================

if (-not (Test-Path "config.yaml")) {
    Write-Host "ERROR: config.yaml not found."
    exit 1
}

if (-not (Test-Path "periscope.py")) {
    Write-Host "ERROR: periscope.py not found."
    exit 1
}

if (-not (Test-Path "snapshot.py")) {
    Write-Host "ERROR: snapshot.py not found."
    exit 1
}

if (-not (Test-Path "requirements.txt")) {
    Write-Host "ERROR: requirements.txt not found."
    exit 1
}


# ============================================================
# CHECK PYTHON
# ============================================================

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python is not installed or not available in PATH."
    Write-Host ""
    Write-Host "Install Python before running AI Periscope."
    exit 1
}


# ============================================================
# CHECK API KEYS
# ============================================================

if ([string]::IsNullOrWhiteSpace($NEOMUNDI_API_KEY)) {
    Write-Host "ERROR: NEOMUNDI_API_KEY is empty."
    Write-Host ""
    Write-Host "Add your NeoMundi ControlTower API key in RUN_PERISCOPE.ps1."
    exit 1
}

if ([string]::IsNullOrWhiteSpace($PROVIDER_API_KEY)) {
    Write-Host "ERROR: PROVIDER_API_KEY is empty."
    Write-Host ""
    Write-Host "Add the API key of the provider selected in config.yaml."
    exit 1
}


# ============================================================
# READ CONFIG.YAML
# ============================================================

$configContent = Get-Content "config.yaml"


# ============================================================
# READ PROVIDER
# ============================================================

$providerLine = $configContent |
    Where-Object { $_ -match '^\s*provider\s*:' } |
    Select-Object -First 1

if (-not $providerLine) {
    Write-Host "ERROR: provider is missing in config.yaml."
    exit 1
}

$provider = (($providerLine -split ':', 2)[1]).Trim().ToLower()

if ([string]::IsNullOrWhiteSpace($provider)) {
    Write-Host "ERROR: provider is empty in config.yaml."
    exit 1
}


# ============================================================
# READ MODEL
# ============================================================

$modelLine = $configContent |
    Where-Object { $_ -match '^\s*model\s*:' } |
    Select-Object -First 1

if (-not $modelLine) {
    Write-Host "ERROR: model is missing in config.yaml."
    exit 1
}

$model = (($modelLine -split ':', 2)[1]).Trim()

if ([string]::IsNullOrWhiteSpace($model)) {
    Write-Host "ERROR: model is empty in config.yaml."
    exit 1
}


# ============================================================
# READ PROMPT FILE
# ============================================================

$promptFileLine = $configContent |
    Where-Object { $_ -match '^\s*prompt_file\s*:' } |
    Select-Object -First 1

if (-not $promptFileLine) {
    Write-Host "ERROR: prompt_file is missing in config.yaml."
    exit 1
}

$promptFile = (($promptFileLine -split ':', 2)[1]).Trim()

if ([string]::IsNullOrWhiteSpace($promptFile)) {
    Write-Host "ERROR: prompt_file is empty in config.yaml."
    exit 1
}

if (-not (Test-Path $promptFile)) {
    Write-Host "ERROR: Prompt file not found:"
    Write-Host "  $promptFile"
    exit 1
}


# ============================================================
# READ RUNS PER PROMPT
# ============================================================

$runsLine = $configContent |
    Where-Object { $_ -match '^\s*runs_per_prompt\s*:' } |
    Select-Object -First 1

if (-not $runsLine) {
    Write-Host "ERROR: runs_per_prompt is missing in config.yaml."
    exit 1
}

$runsPerPromptText = (($runsLine -split ':', 2)[1]).Trim()

if ([string]::IsNullOrWhiteSpace($runsPerPromptText)) {
    Write-Host "ERROR: runs_per_prompt is empty in config.yaml."
    exit 1
}

[int]$runsPerPrompt = 0

if (-not [int]::TryParse($runsPerPromptText, [ref]$runsPerPrompt)) {
    Write-Host "ERROR: runs_per_prompt must be an integer."
    exit 1
}

if ($runsPerPrompt -lt 1) {
    Write-Host "ERROR: runs_per_prompt must be at least 1."
    exit 1
}


# ============================================================
# PASS KEYS TEMPORARILY TO PYTHON
# ============================================================

$env:CONTROLTOWER_API_KEY = $NEOMUNDI_API_KEY
$env:PROVIDER_API_KEY = $PROVIDER_API_KEY


# ============================================================
# DISPLAY CAMPAIGN CONFIGURATION
# ============================================================

Write-Host "Provider        : $provider"
Write-Host "Model           : $model"
Write-Host "Prompt file     : $promptFile"
Write-Host "Runs per prompt : $runsPerPrompt"
Write-Host ""


# ============================================================
# INSTALL / CHECK DEPENDENCIES
# ============================================================

Write-Host "Installing/checking dependencies..."
Write-Host ""

python -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Dependency installation failed."
    exit 1
}


# ============================================================
# RUN AI PERISCOPE
# ============================================================

Write-Host ""
Write-Host "Starting AI Periscope..."
Write-Host ""

python periscope.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: AI Periscope stopped with an error."
    exit 1
}


# ============================================================
# FIND LATEST CAMPAIGN RESULTS
# ============================================================

$latestCampaign = Get-ChildItem "results" -Directory |
    Where-Object { $_.Name -like "campaign_*" } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $latestCampaign) {
    Write-Host ""
    Write-Host "WARNING: No campaign results folder found."
    Write-Host "Campaign completed, but snapshot generation was skipped."
    exit 0
}

$resultsJson = Join-Path $latestCampaign.FullName "campaign_results.json"

if (-not (Test-Path $resultsJson)) {
    Write-Host ""
    Write-Host "WARNING: campaign_results.json not found."
    Write-Host "Snapshot generation was skipped."
    exit 0
}


# ============================================================
# GENERATE SNAPSHOT
# ============================================================

Write-Host ""
Write-Host "Generating campaign snapshot..."
Write-Host ""

python snapshot.py `
    --input "$resultsJson" `
    --config "config.yaml" `
    --neomundi-logo "assets/LOGO_NeoMundi_Controltower.png" `
    --output-dir "$($latestCampaign.FullName)"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "WARNING: Snapshot generation failed."
    Write-Host "Campaign results remain available in:"
    Write-Host "  $($latestCampaign.FullName)"
    exit 0
}


# ============================================================
# END
# ============================================================

Write-Host ""
Write-Host "========================================="
Write-Host "       Campaign complete"
Write-Host "========================================="
Write-Host ""
Write-Host "Results:"
Write-Host "  $($latestCampaign.FullName)"
Write-Host ""
Write-Host "Generated files may include:"
Write-Host "  campaign_results.json"
Write-Host "  campaign_results.csv"
Write-Host "  AI_PERISCOPE_SNAPSHOT.html"
Write-Host "  AI_PERISCOPE_SNAPSHOT.pdf"
Write-Host ""
