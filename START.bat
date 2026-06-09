@echo off
title Game XClicker Elite — SOURIS WARGRIFF v3.0
cd /d "%~dp0"

set XMACRO_DEBUG=0
set XCLICKER_UI=webview
set PYTHONSTARTUP=%~dp0utils\autopatch.py

echo ============================================
echo  Game XClicker Elite — SOURIS WARGRIFF
echo  Interface JS iCUE + moteur Python Win32
echo ============================================

if exist "nodejs\package.json" (
    where node >nul 2>&1
    if not errorlevel 1 (
        pushd nodejs
        if not exist "node_modules\" call npm install --silent
        popd
    ) else (
        echo [START] Node.js requis — installez https://nodejs.org
    )
)

REM Python: venv puis systeme
set PY=
if exist ".venv\Scripts\python.exe" set PY=.venv\Scripts\python.exe
if "%PY%"=="" if exist "venv\Scripts\python.exe" set PY=venv\Scripts\python.exe
if "%PY%"=="" set PY=python

"%PY%" scripts\generate_icon.py 2>nul
"%PY%" CHECK_VERSION.py
if errorlevel 1 (
    echo.
    echo Mise a jour: git pull origin cursor/icue-web-launcher-9626
    pause
    exit /b 1
)

echo.
echo Mode interface:
echo   [1] Bureau JS iCUE (recommande) — run.py
echo   [2] PyQt Sanctuary (legacy)      — run.py --pyqt
echo.
set /p MODE="Choix [1/2] (defaut 1): "
if "%MODE%"=="" set MODE=1

if "%MODE%"=="2" (
    "%PY%" run.py --pyqt
) else (
    "%PY%" run.py
)

if errorlevel 1 pause
