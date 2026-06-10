@echo off
title Clone Game XClicker Elite — Visual Studio
set "PARENT=C:\Users\wargriff\visual_studio_project"
set "TARGET=%PARENT%\Game_XClicker_Elite"

echo.
echo ============================================================
echo   Clone vers: %TARGET%
echo ============================================================
echo.

if not exist "%PARENT%" mkdir "%PARENT%"

if exist "%TARGET%" (
    echo Le dossier existe deja.
    echo Renommez-le ou supprimez-le, puis relancez ce script.
    echo.
    echo Ou lancez INSTALL_COMPLET.ps1 qui gere la sauvegarde auto.
    pause
    exit /b 1
)

git clone https://github.com/wargriff/Game_XClicker_Elite.git "%TARGET%"
if errorlevel 1 (
    echo Clone echoue — installez Git: https://git-scm.com
    pause
    exit /b 1
)

cd /d "%TARGET%"
call INSTALL_COMPLET.bat
exit /b %ERRORLEVEL%
