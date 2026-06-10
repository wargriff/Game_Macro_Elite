@echo off
title Game XClicker Elite
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"
echo.
echo  Lanceur unique : OUVRE_MOI.pyw (double-clic) ou ce START.bat
echo  Maintenance   : python REPARER.py
echo.
"%PY%" OUVRE_MOI.py
if errorlevel 1 pause
exit /b %ERRORLEVEL%
