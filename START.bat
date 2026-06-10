@echo off
title Game XClicker Elite — Mission Control
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"

echo.
echo  Si .bat bloque par Windows Smart App Control, utilisez PYTHON:
echo    python DEBLOQUER.py
echo    python GO.py
echo    python REPARER.py
echo.

if not exist "GameXClicker.py" (
    echo ERREUR: GameXClicker.py absent — REPARER.bat
    pause
    exit /b 1
)

"%PY%" -m pip install -r requirements.txt -q 2>nul
"%PY%" GameXClicker.py
if errorlevel 1 pause
exit /b %ERRORLEVEL%
