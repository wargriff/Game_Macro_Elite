@echo off
title Mise a jour Game XClicker Elite
cd /d "%~dp0.."

echo === git pull branche v3 ===
git fetch origin cursor/icue-web-launcher-9626
git checkout cursor/icue-web-launcher-9626 2>nul
git pull origin cursor/icue-web-launcher-9626

echo.
echo === Verification ===
python CHECK_VERSION.py
echo.
echo Lancez: START.bat
pause
