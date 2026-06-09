@echo off
title Sanctuary Bot — Configuration PyCharm
cd /d "%~dp0"

echo.
echo ============================================================
echo   SANCTUARY BOT — Configuration PyCharm
echo ============================================================
echo.
echo 1. Run - Edit Configurations
echo 2. Script path : %~dp0Xmacro_main.py
echo 3. Working directory : %~dp0
echo 4. Environment variables — ajouter :
echo.
echo    PYTHONSTARTUP=%~dp0utils\autopatch.py
echo    XMACRO_DEBUG=1
echo    XMACRO_BOT=1
echo.
echo 5. Au lancement vous DEVEZ voir :
echo    [XMACRO] launcher sanctuary v2.2 + Sanctuary Bot
echo    [Sanctuary Bot] DÉMARRAGE — Je surveille ton app
echo.
echo 6. Verifier : python CHECK_VERSION.py
echo.
pause
