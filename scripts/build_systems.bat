@echo off
setlocal enabledelayedexpansion

echo ==============================================================================
echo [NEXUS TITAN] Building Systems Layer (C++20, MSVC, Ninja)
echo ==============================================================================

set "VCVARS=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
set "CMAKE=C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"

if not exist "!VCVARS!" (
    echo [ERROR] Visual Studio 2022 vcvars64.bat not found at: !VCVARS!
    exit /b 1
)

call "!VCVARS!"

if "%1"=="clean" (
    echo [NEXUS TITAN] Cleaning build directory...
    if exist build rmdir /s /q build
)

echo [NEXUS TITAN] Configuring CMake with Ninja generator...
"!CMAKE!" -G Ninja -B build -DCMAKE_BUILD_TYPE=Release
if errorlevel 1 exit /b 1

echo [NEXUS TITAN] Compiling C++ systems targets...
"!CMAKE!" --build build
if errorlevel 1 exit /b 1

echo [NEXUS TITAN] Executing CTest unit tests...
"!CMAKE!" -E chdir build ctest --output-on-failure
if errorlevel 1 exit /b 1

echo ==============================================================================
echo [NEXUS TITAN] Systems build and test passed successfully.
echo ==============================================================================
