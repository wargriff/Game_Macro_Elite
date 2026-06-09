@echo off
title Game XClicker Elite — Centre de controle
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"

echo.
echo Lancement centre de controle (tout en 1)...
echo.

if not exist "main.py" (
    echo ERREUR: main.py absent — REPARER.bat
    pause
    exit /b 1
)

"%PY%" -m pip install -r requirements.txt -q 2>nul
"%PY%" main.py
if errorlevel 1 pause
exit /b %ERRORLEVEL%
