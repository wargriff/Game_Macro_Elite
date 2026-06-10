@echo off
title REPARER — Game XClicker Elite
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"
"%PY%" REPARER.py
if errorlevel 1 pause
exit /b %ERRORLEVEL%
