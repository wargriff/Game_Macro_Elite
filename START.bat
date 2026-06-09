@echo off
title Game XClicker Elite
cd /d "%~dp0"

set "EXE=dist\Game XClicker Elite\Game XClicker Elite.exe"
set "PY=%~dp0..\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

if /I "%~1"=="build" goto build
if /I "%~1"=="rebuild" goto build

if exist "ui.py" if exist "ui\" (
    if exist "ui.py.bak" del /f "ui.py.bak"
    ren "ui.py" "ui.py.bak" 2>nul
)

if exist "%EXE%" (
    start "" "%CD%\%EXE%"
    exit /b 0
)

"%PY%" gxclicker.py
if errorlevel 1 pause
exit /b %ERRORLEVEL%

:build
if exist "ui.py" if exist "ui\" ren "ui.py" "ui.py.bak" 2>nul
"%PY%" scripts\generate_icon.py 2>nul
"%PY%" -m pip install pyinstaller pywebview pillow psutil -q
"%PY%" -m PyInstaller build.spec --noconfirm
if errorlevel 1 ( echo BUILD ECHEC & pause & exit /b 1 )
powershell -Command "Get-ChildItem 'dist\Game XClicker Elite' -Recurse -ErrorAction SilentlyContinue | Unblock-File" 2>nul
echo.
echo OK: dist\Game XClicker Elite\Game XClicker Elite.exe
echo Lancez: START.bat
pause
exit /b 0
