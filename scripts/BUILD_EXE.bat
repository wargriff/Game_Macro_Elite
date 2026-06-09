@echo off
title Build Game XClicker Elite.exe
cd /d "%~dp0.."

echo === 1. Icone ===
python scripts\generate_icon.py

echo === 2. PyInstaller ===
pip install pyinstaller pywebview pillow psutil -q
pyinstaller build.spec --noconfirm

echo === 3. Debloquer Windows Smart App Control ===
powershell -Command "Get-ChildItem 'dist\Game XClicker Elite' -Recurse | Unblock-File" 2>nul

echo.
echo === TERMINE ===
echo Lancez: dist\Game XClicker Elite\Game XClicker Elite.exe
echo.
echo Si Smart App Control bloque:
echo   1. Parametres ^> Confidentialite ^> Controle intelligent des applications ^> Desactiver
echo   OU
echo   2. Clic droit .exe ^> Proprietes ^> Debloquer ^> OK
echo.
pause
