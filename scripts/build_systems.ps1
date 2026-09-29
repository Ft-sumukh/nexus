# ==============================================================================
# NEXUS TITAN — Systems Build & Test Script (PowerShell Wrapper)
# ==============================================================================
param (
    [switch]$Clean = $false
)

$ErrorActionPreference = "Stop"

$BatScript = Join-Path $PSScriptRoot "build_systems.bat"
$Arg = if ($Clean) { "clean" } else { "" }

& cmd.exe /c "`"$BatScript`" $Arg"
if ($LASTEXITCODE -ne 0) {
    throw "C++ systems build/test failed with exit code $LASTEXITCODE"
}
