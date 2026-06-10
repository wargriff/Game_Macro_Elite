@echo off
REM Obsolète — redirige vers le lanceur unique
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"
"%PY%" OUVRE_MOI.py
exit /b %ERRORLEVEL%
