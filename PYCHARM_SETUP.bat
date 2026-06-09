@echo off
title Game XClicker Elite — PyCharm
cd /d "%~dp0"

echo.
echo ============================================================
echo   Game XClicker Elite — Configuration PyCharm
echo ============================================================
echo.
echo IMPORTANT: n'utilisez PAS un ancien run.py supprime.
echo.
echo 1. Run - Edit Configurations
echo 2. Script path : %~dp0gxclicker.py
echo    (NE PAS utiliser un run.py supprime ou absent)
echo 3. Working directory : %~dp0
echo.
echo    Config prete a copier : pycharm\Game_XClicker_Elite.run.xml
echo    PyCharm : Run - Edit Configurations - Import...
echo.
echo 4. Si run.py manquant, executez :
echo    python scripts\repair_launchers.py
echo    ou double-cliquez START.bat
echo.
echo 5. Lancement recommande hors PyCharm :
echo    START.bat
echo.
pause
