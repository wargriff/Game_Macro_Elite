@echo off
title Game XClicker Elite — PyCharm
cd /d "%~dp0"

echo.
echo ============================================================
echo   Game XClicker Elite — Configuration PyCharm
echo ============================================================
echo.
echo run.py et main.py sont SUPPRIMES — ne les utilisez plus.
echo.
echo 1. Run - Edit Configurations
echo 2. Supprimez toute config qui pointe vers run.py ou main.py
echo 3. Nouvelle config Python :
echo    Script path : %~dp0gxclicker.py
echo    Working directory : %~dp0
echo.
echo    Import rapide : pycharm\Game_XClicker_Elite.run.xml
echo    (Run - Edit Configurations - Import...)
echo.
echo 4. Lancement hors PyCharm : double-clic START.bat
echo.
pause
