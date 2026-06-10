@echo off
REM Obsolète — utilisez Mission Control (LANCER .EXE)
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"
echo.
echo  Ce raccourci est obsolete.
echo  Lancez OUVRE_MOI.pyw puis cliquez LANCER .EXE dans Mission Control.
echo.
"%PY%" OUVRE_MOI.py
exit /b %ERRORLEVEL%
