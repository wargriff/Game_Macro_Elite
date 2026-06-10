@echo off
title Ouvrir Game XClicker dans Visual Studio
cd /d "%~dp0"

echo [1/2] Telechargement httplib + json...
powershell -NoProfile -ExecutionPolicy Bypass -File "cpp\third_party\fetch_deps.ps1"
if errorlevel 1 (
    echo ERREUR fetch deps
    pause
    exit /b 1
)

echo.
echo [2/2] Ouverture Visual Studio...
echo.
echo Fermez votre ancien projet vide.
echo Ouvrez CE fichier solution:
echo   %~dp0Game_XClicker_Elite.sln
echo.

start "" "%~dp0Game_XClicker_Elite.sln"
echo.
echo Dans VS:
echo   1) Configuration: Release  x64
echo   2) Projet demarrage: GameXClicker (ou GameXClickerQt si Qt installe)
echo   3) Build ^> Generer la solution
echo   4) F5 pour lancer
pause
