@echo off
title Fix Game XClicker Elite — ui.py + git pull
cd /d "%~dp0"

echo ============================================
echo  FIX Game XClicker Elite v3.1
echo ============================================

REM --- Fix ui.py (cause principale) ---
if exist "ui.py" (
    echo [FIX] ui.py detecte — renommage...
    if exist "ui.py.bak" del /f "ui.py.bak"
    ren "ui.py" "ui.py.bak"
    echo [FIX] ui.py -^> ui.py.bak OK
)

REM --- Git pull ---
where git >nul 2>&1
if not errorlevel 1 (
    git fetch origin cursor/icue-web-launcher-9626 2>nul
    git checkout cursor/icue-web-launcher-9626 2>nul
    git pull origin cursor/icue-web-launcher-9626 2>nul
)

set PY=
if exist "..\.venv\Scripts\python.exe" set PY=..\.venv\Scripts\python.exe
if "%PY%"=="" if exist ".venv\Scripts\python.exe" set PY=.venv\Scripts\python.exe
if "%PY%"=="" if exist "venv\Scripts\python.exe" set PY=venv\Scripts\python.exe
if "%PY%"=="" set PY=python

echo.
echo === Verification ===
"%PY%" CHECK_VERSION.py
if errorlevel 1 (
    echo.
    echo Fichiers manquants — copiez le projet depuis GitHub:
    echo https://github.com/wargriff/Game_XClicker_Elite/tree/cursor/icue-web-launcher-9626
    pause
    exit /b 1
)

echo.
echo === Dependances ===
"%PY%" -m pip install -r requirements.txt -q
if exist "nodejs\package.json" (
    pushd nodejs
    call npm install --silent 2>nul
    popd
)

echo.
echo === Lancement ===
"%PY%" run.py
if errorlevel 1 pause
