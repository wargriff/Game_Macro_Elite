@echo off
title Build Game XClicker Elite.exe
cd /d "%~dp0"

set "PY=%~dp0..\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo === Game XClicker Elite — BUILD ===

if exist "ui.py" if exist "ui\" (
    if exist "ui.py.bak" del /f "ui.py.bak"
    ren "ui.py" "ui.py.bak"
)

"%PY%" scripts\generate_icon.py 2>nul
"%PY%" -m pip install pyinstaller pywebview pillow psutil -q

echo Compilation PyInstaller...
"%PY%" -m PyInstaller build.spec --noconfirm
if errorlevel 1 (
    echo ECHEC compilation
    pause
    exit /b 1
)

powershell -Command "Get-ChildItem 'dist\Game XClicker Elite' -Recurse -ErrorAction SilentlyContinue | Unblock-File" 2>nul

echo.
echo === OK ===
echo Executable: dist\Game XClicker Elite\Game XClicker Elite.exe
echo Lancez: START.bat
echo.
echo Smart App Control bloque ?
echo   Clic droit .exe ^> Proprietes ^> Debloquer
echo.
pause
