@echo off
title Game XClicker Elite — SOURIS WARGRIFF
cd /d "%~dp0"

set "EXE=%~dp0dist\Game XClicker Elite\Game XClicker Elite.exe"

REM ── Mode 1 : .exe (production) ──
if exist "%EXE%" (
    if /I "%~1"=="build" goto build
    if /I "%~1"=="rebuild" goto build
    start "" "%EXE%" %*
    exit /b 0
)

REM ── Mode 2 : Python dev (avant build) ──
if /I "%~1"=="build" goto build
if /I "%~1"=="rebuild" goto build

set "PY=%~dp0..\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

REM Fix ui.py automatique
if exist "ui.py" if exist "ui\" (
    echo [START] Renommage ui.py...
    if exist "ui.py.bak" del /f "ui.py.bak"
    ren "ui.py" "ui.py.bak"
)

echo [START] Mode dev — lancez START.bat build pour creer le .exe
"%PY%" "%~dp0gxclicker.py" %*
exit /b %ERRORLEVEL%

:build
call "%~dp0BUILD.bat"
exit /b %ERRORLEVEL%
