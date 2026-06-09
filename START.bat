@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

cd /d "%~dp0"
title Game XClicker Elite

if /I "%~1"=="build" goto :build_exe
if /I "%~1"=="exe"   goto :run_exe
goto :run_app

REM ============================================================
REM  LANCEMENT APPLICATION (defaut)
REM ============================================================
:run_app
echo.
echo ╔══════════════════════════════════════════════╗
echo ║         Game XClicker Elite — START          ║
echo ╚══════════════════════════════════════════════╝
echo.

call :find_python
if errorlevel 1 (
    echo [ERR] Python introuvable. Installez Python 3.12+
    pause
    exit /b 1
)

echo [START] Python : %PY_CMD%
echo [START] Installation dependances...
"%PY_CMD%" -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo [ERR] pip install a echoue
    pause
    exit /b 1
)

call :run_ai_guardian

echo [START] Lancement Xmacro_main.py...
echo.
"%PY_CMD%" Xmacro_main.py
set "EXIT_CODE=!errorlevel!"
echo.
echo [START] Termine (code !EXIT_CODE!)
pause
exit /b !EXIT_CODE!

REM ============================================================
REM  BUILD .EXE UNIQUE
REM ============================================================
:build_exe
echo.
echo ╔══════════════════════════════════════════════╗
echo ║      Build Game_XClicker_Elite.exe           ║
echo ╚══════════════════════════════════════════════╝
echo.

call :find_python
if errorlevel 1 (
    echo [ERR] Python introuvable
    pause
    exit /b 1
)

echo [BUILD] Installation dependances + PyInstaller...
"%PY_CMD%" -m pip install -r requirements.txt pyinstaller -q

if exist "build" rmdir /s /q "build" 2>nul
if exist "dist\Game_XClicker_Elite.exe" del /f /q "dist\Game_XClicker_Elite.exe" 2>nul

echo [BUILD] Compilation en cours...
"%PY_CMD%" -m PyInstaller build.spec --noconfirm
if errorlevel 1 (
    echo [ERR] Build echoue
    pause
    exit /b 1
)

echo.
echo [BUILD] OK — Executable unique :
echo         dist\Game_XClicker_Elite.exe
echo.
pause
exit /b 0

REM ============================================================
REM  LANCER LE .EXE DEJA COMPILE
REM ============================================================
:run_exe
if not exist "dist\Game_XClicker_Elite.exe" (
    echo [ERR] dist\Game_XClicker_Elite.exe introuvable
    echo       Lancez d'abord : START.bat build
    pause
    exit /b 1
)
echo [START] Lancement dist\Game_XClicker_Elite.exe
start "" "dist\Game_XClicker_Elite.exe"
exit /b 0

REM ============================================================
REM  IA GUARDIAN (Node.js C:\src)
REM ============================================================
:run_ai_guardian
set "NODE_BIN="
if exist "C:\src\node.exe" (
    set "NODE_BIN=C:\src\node.exe"
) else if exist "C:\src\node\node.exe" (
    set "NODE_BIN=C:\src\node\node.exe"
) else (
    where node >nul 2>&1
    if !errorlevel!==0 set "NODE_BIN=node"
)

if "!NODE_BIN!"=="" (
    echo [AI] Node.js absent — lancement sans analyse IA
    exit /b 0
)

set "AI_DIR=C:\src\ai-guardian"
if not exist "!AI_DIR!\analyzer.js" set "AI_DIR=%~dp0nodejs\ai-guardian"

if not exist "C:\src\ai-guardian" mkdir "C:\src\ai-guardian" 2>nul
if exist "%~dp0nodejs\ai-guardian\analyzer.js" (
    copy /Y "%~dp0nodejs\ai-guardian\*.js" "C:\src\ai-guardian\" >nul 2>&1
    copy /Y "%~dp0nodejs\ai-guardian\package.json" "C:\src\ai-guardian\" >nul 2>&1
    set "AI_DIR=C:\src\ai-guardian"
)

echo [AI] Analyse du projet...
"!NODE_BIN!" "!AI_DIR!\analyzer.js" --project "%~dp0" --fix
echo.
exit /b 0

REM ============================================================
REM  DETECTION PYTHON
REM ============================================================
:find_python
set "PY_CMD="
if exist ".venv\Scripts\python.exe" set "PY_CMD=.venv\Scripts\python.exe"
if not defined PY_CMD if exist "venv\Scripts\python.exe" set "PY_CMD=venv\Scripts\python.exe"
if not defined PY_CMD (
    where python >nul 2>&1
    if !errorlevel!==0 set "PY_CMD=python"
)
if not defined PY_CMD exit /b 1
exit /b 0
