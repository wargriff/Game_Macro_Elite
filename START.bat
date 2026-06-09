@echo off
title Game XClicker Elite
cd /d "%~dp0"

echo ========================================
echo   Game XClicker Elite — SOURIS WARGRIFF
echo ========================================

REM --- Node.js C:\src (votre installation) ---
set "XCLICKER_NODE_PATH=C:\src\node.exe"
if exist "C:\src\node.exe" set "NODE=C:\src\node.exe"
if not defined NODE if exist "C:\src\node\node.exe" set "NODE=C:\src\node\node.exe"
if not defined NODE set "NODE=node"

REM --- Python venv ---
set "PY=%~dp0..\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=%~dp0venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo Python: %PY%
echo Node:   %NODE%
"%PY%" --version 2>nul
if errorlevel 1 ( echo ERREUR Python & pause & exit /b 1 )

REM --- Fix ui.py ---
if exist "ui.py" if exist "ui\" (
    echo [FIX] ui.py -^> ui.py.bak
    if exist "ui.py.bak" del /f "ui.py.bak"
    ren "ui.py" "ui.py.bak"
)

if not exist "gxclicker.py" (
    echo ERREUR: git pull origin cursor/icue-web-launcher-9626
    pause
    exit /b 1
)

REM --- Cree/repare run.py + main.py (PyCharm compat) ---
if not exist "scripts\repair_launchers.py" (
    echo ERREUR: scripts\repair_launchers.py absent — git pull
    pause
    exit /b 1
)
"%PY%" scripts\repair_launchers.py
if not exist "run.py" (
    echo ERREUR: impossible de creer run.py
    pause
    exit /b 1
)

if /I "%~1"=="build" goto build
if /I "%~1"=="browser" goto runbrowser

set "EXE=%~dp0dist\Game XClicker Elite\Game XClicker Elite.exe"
if exist "%EXE%" (
    echo Lancement .exe...
    start "" "%EXE%"
    exit /b 0
)

echo Installation dependances Python...
"%PY%" -m pip install -r requirements.txt -q 2>nul

if exist "nodejs\package.json" (
    echo Installation Node.js (C:\src)...
    pushd nodejs
    if not exist node_modules (
        "%NODE%" --version 2>nul
        if errorlevel 1 (
            echo WARN: Node introuvable — UI via port 17840
        ) else (
            call "%NODE%" "%~dp0nodejs\node_modules\npm\bin\npm-cli.js" install 2>nul
            if errorlevel 1 call npm install --silent
        )
    )
    popd
)

echo Lancement gxclicker.py ...
"%PY%" gxclicker.py
if errorlevel 1 pause
exit /b %ERRORLEVEL%

:runbrowser
set GX_BROWSER=1
"%PY%" gxclicker.py
if errorlevel 1 pause
exit /b %ERRORLEVEL%

:build
"%PY%" -m pip install -r requirements.txt pyinstaller -q
"%PY%" scripts\generate_icon.py 2>nul
"%PY%" -m PyInstaller build.spec --noconfirm
if errorlevel 1 ( echo BUILD ECHEC & pause & exit /b 1 )
powershell -Command "Get-ChildItem 'dist\Game XClicker Elite' -Recurse -ErrorAction SilentlyContinue | Unblock-File" 2>nul
echo OK: dist\Game XClicker Elite\Game XClicker Elite.exe
pause
exit /b 0
