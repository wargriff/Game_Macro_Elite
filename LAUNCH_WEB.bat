@echo off
REM Obsolète — utilisez Mission Control (INTERFACE WEB)
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"
echo.
echo  Ce raccourci est obsolete.
echo  Lancez OUVRE_MOI.pyw puis cliquez INTERFACE WEB dans Mission Control.
echo.
"%PY%" OUVRE_MOI.py
exit /b %ERRORLEVEL%
