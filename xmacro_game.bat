@echo off
REM Raccourci — redirige vers le lanceur unique START.bat
cd /d "%~dp0"
call START.bat %*
