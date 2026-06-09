@echo off
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"
"%PY%" main.py --build
pause
exit /b %ERRORLEVEL%
