@echo off
REM Build avancé CLI — sinon utilisez Mission Control ^> BUILD .EXE
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"
"%PY%" GameXClicker.py --build --desktop
pause
exit /b %ERRORLEVEL%
