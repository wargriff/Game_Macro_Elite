@echo off
title Mise a jour — Game XClicker Elite
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"
"%PY%" REPARER.py
exit /b %ERRORLEVEL%
