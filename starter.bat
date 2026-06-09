@echo off
chcp 65001 >nul
title XMacro Elite — AI Guardian + Launcher

REM Aller dans le dossier du projet (là où se trouve ce .bat)
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════╗
echo ║       XMacro Elite — Starter + AI Guardian   ║
echo ╚══════════════════════════════════════════════╝
echo.

REM --- Détection Node.js (priorité C:\src) ---
set "NODE_BIN="
if exist "C:\src\node.exe" (
    set "NODE_BIN=C:\src\node.exe"
) else if exist "C:\src\node\node.exe" (
    set "NODE_BIN=C:\src\node\node.exe"
) else (
    where node >nul 2>&1
    if %errorlevel%==0 set "NODE_BIN=node"
)

REM --- Dossier IA Guardian ---
set "AI_DIR=C:\src\ai-guardian"
if not exist "%AI_DIR%\analyzer.js" (
    set "AI_DIR=%~dp0nodejs\ai-guardian"
)

if "%NODE_BIN%"=="" (
    echo [WARN] Node.js introuvable dans C:\src — lancement sans IA Node
    goto :launch_python
)

echo [AI] Node.js : %NODE_BIN%
echo [AI] Dossier  : %AI_DIR%
echo.

REM --- Synchroniser vers C:\src si besoin ---
if not exist "C:\src\ai-guardian" mkdir "C:\src\ai-guardian" 2>nul
if exist "%~dp0nodejs\ai-guardian\analyzer.js" (
    copy /Y "%~dp0nodejs\ai-guardian\*.js" "C:\src\ai-guardian\" >nul 2>&1
    copy /Y "%~dp0nodejs\ai-guardian\package.json" "C:\src\ai-guardian\" >nul 2>&1
    set "AI_DIR=C:\src\ai-guardian"
)

echo [AI] Analyse du projet en cours...
"%NODE_BIN%" "%AI_DIR%\analyzer.js" --project "%~dp0" --fix
echo.

:launch_python
echo [XMACRO] Lancement de Xmacro_main.py...
echo.

python Xmacro_main.py
set "EXIT_CODE=%errorlevel%"

echo.
echo [XMACRO] Terminé (code %EXIT_CODE%)
pause
exit /b %EXIT_CODE%
