$ErrorActionPreference = "Stop"

# ============================================================
# NeoMundi AI Periscope — V0.1
#
# HOW TO USE
# 1. Add your NeoMundi ControlTower API key below.
# 2. Add ONLY the API key of the provider you want to use.
# 3. Configure provider, model, prompt_file and runs_per_prompt
#    in config.yaml.
# 4. Run this file.
# ============================================================


# ============================================================
# USER API KEYS
# ============================================================

# NeoMundi ControlTower
$NEOMUNDI_API_KEY = ""


# AI PROVIDERS
# Fill ONLY the provider key you are using.

$OPENAI_API_KEY    = ""
$ANTHROPIC_API_KEY = ""
$MISTRAL_API_KEY   = ""
$DEEPSEEK_API_KEY  = ""
$PPLX_API_KEY      = ""
$COHERE_API_KEY    = ""
$XAI_API_KEY       = ""
$QWEN_API_KEY      = ""
$TOGETHER_API_KEY  = ""
$MOONSHOT_API_KEY  = ""


# ============================================================
# START
# ============================================================

Write-Host ""
Write-Host "========================================="
Write-Host "       NeoMundi AI Periscope"
Write-Host "========================================="
Write-Host ""


# ============================================================
# CHECK FILES
# ============================================================

if (-not (Test-Path "config.yaml")) {
    Write-Host "ERROR: config.yaml not found."
    exit 1
}

if (-not (Test-Path "periscope.py")) {
    Write-Host "ERROR: periscope.py not found."
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
    exit 1
}


# ============================================================
# CHECK NEOMUNDI KEY
# ============================================================

if ([string]::IsNullOrWhiteSpace($NEOMUNDI_API_KEY)) {
    Write-Host "ERROR: NEOMUNDI_API_KEY is empty."
    Write-Host "Add your NeoMundi ControlTower API key in RUN_PERISCOPE.ps1."
    exit 1
}


# ============================================================
# READ PROVIDER FROM config.yaml
# ============================================================

$configContent = Get-Content "config.yaml"

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
# SELECT PROVIDER API KEY
# ============================================================

$PROVIDER_API_KEY = ""

switch ($provider) {

    "openai" {
        $PROVIDER_API_KEY = $OPENAI_API_KEY
    }

    "anthropic" {
        $PROVIDER_API_KEY = $ANTHROPIC_API_KEY
    }

    "mistral" {
        $PROVIDER_API_KEY = $MISTRAL_API_KEY
    }

    "deepseek" {
        $PROVIDER_API_KEY = $DEEPSEEK_API_KEY
    }

    "perplexity" {
        $PROVIDER_API_KEY = $PPLX_API_KEY
    }

    "cohere" {
        $PROVIDER_API_KEY = $COHERE_API_KEY
    }

    "xai" {
        $PROVIDER_API_KEY = $XAI_API_KEY
    }

    "qwen" {
        $PROVIDER_API_KEY = $QWEN_API_KEY
    }

    "together" {
        $PROVIDER_API_KEY = $TOGETHER_API_KEY
    }

    "moonshot" {
        $PROVIDER_API_KEY = $MOONSHOT_API_KEY
    }

    default {
        Write-Host "ERROR: Unsupported provider: $provider"
        Write-Host ""
        Write-Host "Supported providers:"
        Write-Host "  openai"
        Write-Host "  anthropic"
        Write-Host "  mistral"
        Write-Host "  deepseek"
        Write-Host "  perplexity"
        Write-Host "  cohere"
        Write-Host "  xai"
        Write-Host "  qwen"
        Write-Host "  together"
        Write-Host "  moonshot"
        exit 1
    }
}


# ============================================================
# CHECK PROVIDER KEY
# ============================================================

if ([string]::IsNullOrWhiteSpace($PROVIDER_API_KEY)) {
    Write-Host "ERROR: No API key configured for provider '$provider'."
    Write-Host "Add the corresponding provider API key in RUN_PERISCOPE.ps1."
    exit 1
}


# ============================================================
# PASS KEYS TEMPORARILY TO PYTHON
# ============================================================

$env:CONTROLTOWER_API_KEY = $NEOMUNDI_API_KEY
$env:PROVIDER_API_KEY = $PROVIDER_API_KEY


# ============================================================
# INSTALL / CHECK DEPENDENCIES
# ============================================================

Write-Host "Provider detected : $provider"
Write-Host ""
Write-Host "Installing/checking dependencies..."

python -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Dependency installation failed."
    exit 1
}


# ============================================================
# RUN PERISCOPE
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
# END
# ============================================================

Write-Host ""
Write-Host "========================================="
Write-Host "       Campaign complete"
Write-Host "========================================="
Write-Host ""
