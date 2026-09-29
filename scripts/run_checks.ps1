# ==============================================================================
# NEXUS TITAN — Unified Quality & Verification Runner
# Runs static type checks, C++ CTest, Python pytest, and TypeScript vitest
# ==============================================================================
$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  NEXUS TITAN -- Unified Verification Suite" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# 1. C++ Systems Layer
Write-Host ""
Write-Host "[1/3] Building and Testing C++ Systems Layer..." -ForegroundColor Yellow
$BuildScript = Join-Path $PSScriptRoot "build_systems.ps1"
& powershell -ExecutionPolicy Bypass -File $BuildScript
if ($LASTEXITCODE -ne 0) { throw "C++ Systems verification failed with exit code $LASTEXITCODE" }

# 2. Python AI Runtime Layer
Write-Host ""
Write-Host "[2/3] Running Python AI Runtime Test Suite..." -ForegroundColor Yellow
& python -m pytest tests/ai -v
if ($LASTEXITCODE -ne 0) { throw "Python AI Runtime verification failed with exit code $LASTEXITCODE" }

# 3. TypeScript Layer
Write-Host ""
Write-Host "[3/3] Running TypeScript Checks and Tests..." -ForegroundColor Yellow
& npm.cmd run typecheck
if ($LASTEXITCODE -ne 0) { throw "TypeScript typecheck failed with exit code $LASTEXITCODE" }
& npm.cmd test
if ($LASTEXITCODE -ne 0) { throw "TypeScript test suite failed with exit code $LASTEXITCODE" }

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host "  [ALL CHECKS PASSED] NEXUS TITAN Foundation Verified" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
