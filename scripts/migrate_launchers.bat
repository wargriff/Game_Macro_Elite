@echo off
REM Supprime les anciens launchers — garde uniquement START.bat
cd /d "%~dp0\.."

echo [MIGRATE] Suppression des anciens launchers...

for %%F in (
    "Build-Pro.bat"
    "Lancer Game XClicker.bat"
    "starter.bat"
    "RUN_TESTS.bat"
    "UPDATE.bat"
) do (
    if exist %%F (
        del /f /q %%F
        echo   supprime : %%F
    )
)

echo.
echo [MIGRATE] Termine. Utilisez uniquement :
echo           START.bat        — lancer le programme
echo           START.bat build  — compiler le .exe
echo           START.bat exe    — lancer le .exe
pause
