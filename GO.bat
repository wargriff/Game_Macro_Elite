@echo off
title Game XClicker Elite
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"
echo Dossier: %CD%
if exist ".git" (
    echo git pull origin main...
    git pull origin main
)
"%PY%" -m pip install -r requirements.txt -q 2>nul
echo Lancement GameXClicker.py ...
"%PY%" GameXClicker.py
if errorlevel 1 pause
