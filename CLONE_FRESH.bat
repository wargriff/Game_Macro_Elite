@echo off
title CLONE FRESH — Game XClicker Elite
cd /d "%~dp0"

set "TARGET=%~dp0"
if "%TARGET:~-1%"=="\" set "TARGET=%TARGET:~0,-1%"

echo.
echo ============================================================
echo   Installation propre Game XClicker Elite
echo   Cible: %TARGET%
echo ============================================================
echo.

if exist "%TARGET%\.git" (
    echo Ce dossier contient deja git. Lancez: python REPARER.py
    pause
    exit /b 1
)

for %%I in ("%TARGET%") do set "PARENT=%%~dpI"
if "%PARENT:~-1%"=="\" set "PARENT=%PARENT:~0,-1%"

echo Clone branche main ...
git clone https://github.com/wargriff/Game_XClicker_Elite.git "%TARGET%"
if errorlevel 1 (
    echo Clone echoue.
    pause
    exit /b 1
)

cd /d "%TARGET%"

set "PY=%PARENT%\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=%TARGET%\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo Installation Python ...
"%PY%" -m pip install -r requirements.txt

echo.
echo ============================================================
echo   OK — Visual Studio / Cursor :
echo   %TARGET%
echo.
echo   Lanceur C++     : BUILD_CPP.bat puis GameXClicker.exe
echo   Lanceur Python  : OUVRE_MOI.pyw
echo ============================================================
echo.
call REPARER.bat
pause
