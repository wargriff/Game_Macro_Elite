@echo off
title Install — Visual Studio project
cd /d "%~dp0"
call "%~dp0scripts\_env.bat"

echo.
echo Dossier projet: %CD%
echo.
echo [1/3] Dependances Python...
"%PY%" -m pip install -r requirements.txt -q

echo [2/3] Build Control Panel C++ (optionnel)...
if exist "BUILD_CPP.bat" call BUILD_CPP.bat

echo.
echo [3/3] Pret.
echo   C++  : GameXClicker.exe  (apres BUILD_CPP.bat)
echo   Python : OUVRE_MOI.pyw
echo.
pause
