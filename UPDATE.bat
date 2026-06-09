@echo off
title Mise a jour Game XClicker Elite
cd /d "%~dp0"

echo === Sauvegarde fichiers locaux ===
if not exist "_backup_local" mkdir "_backup_local"
copy /Y "ui\main_window.py" "_backup_local\main_window.py.bak" 2>nul
copy /Y "Xmacro_main.py" "_backup_local\Xmacro_main.py.bak" 2>nul

echo === Git pull branche fix ===
git fetch origin
git checkout cursor/sanctuary-diablo-ui-9626
git pull origin cursor/sanctuary-diablo-ui-9626

echo === Node.js ===
if exist "nodejs\package.json" (
    pushd nodejs
    call npm install
    popd
)

echo === Verification ===
findstr /C:"master_combo" ui\sanctuary_window.py >nul && echo [OK] sanctuary_window.py contient master_combo || echo [ERREUR] sanctuary_window.py ancien!
findstr /C:"ui.main_window" Xmacro_main.py >nul && echo [OK] Xmacro_main.py import correct || echo [ERREUR] Xmacro_main.py ancien!

echo.
echo Termine. Lance: python Xmacro_main.py
pause
