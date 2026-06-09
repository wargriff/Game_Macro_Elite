@echo off
title CLONE FRESH — Game XClicker Elite
set "PARENT=C:\Users\wargriff\Pycharm_Project_v 3.12"
set "TARGET=%PARENT%\Game_XClicker_Elite_Sanctuary"

echo.
echo Clone propre dans:
echo   %TARGET%
echo.

if exist "%TARGET%" (
    echo Le dossier existe deja. Renomme-le ou supprime-le d'abord.
    pause
    exit /b 1
)

git clone -b cursor/sanctuary-diablo-ui-9626 https://github.com/wargriff/Game_XClicker_Elite.git "%TARGET%"
if errorlevel 1 (
    echo Clone echoue.
    pause
    exit /b 1
)

cd /d "%TARGET%"

echo.
echo Installation Python...
if exist "%PARENT%\.venv\Scripts\pip.exe" (
    "%PARENT%\.venv\Scripts\pip.exe" install -r requirements.txt
) else (
    pip install -r requirements.txt
)

echo.
echo npm...
cd nodejs
call npm install
cd ..

echo.
python CHECK_VERSION.py

echo.
echo ============================================================
echo   Ouvre PyCharm sur: %TARGET%
echo   Script: Xmacro_main.py
echo   Env: PYTHONSTARTUP=%TARGET%\utils\autopatch.py
echo ============================================================
pause
