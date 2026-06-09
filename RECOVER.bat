@echo off
title RECUPERATION Game XClicker Elite
cd /d "%~dp0"

echo.
echo ============================================================
echo   RECUPERATION — ne lance PAS git clean depuis le dossier parent !
echo ============================================================
echo.

if not exist ".git" (
    echo ERREUR: pas de dossier .git ici.
    echo Va dans Game_XClicker_Elite ou clone le repo.
    pause
    exit /b 1
)

echo [1] Fetch branche corrigee...
git fetch origin cursor/sanctuary-diablo-ui-9626
if errorlevel 1 (
    echo Fetch echoue — essai URL alternative...
    git remote set-url origin https://github.com/wargriff/Game_XClicker_Elite.git
    git fetch origin cursor/sanctuary-diablo-ui-9626
)

echo [2] Bascule branche...
git checkout -B cursor/sanctuary-diablo-ui-9626 origin/cursor/sanctuary-diablo-ui-9626
git reset --hard origin/cursor/sanctuary-diablo-ui-9626

echo [3] Verification...
if not exist "CHECK_VERSION.py" (
    echo ECHEC — fichiers manquants. Utilise CLONE_FRESH.bat
    pause
    exit /b 1
)

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" CHECK_VERSION.py
) else (
    python CHECK_VERSION.py
)

echo.
echo [4] npm...
if exist "nodejs\package.json" (
    pushd nodejs
    call npm install
    popd
)

echo.
echo OK — Lance: python Xmacro_main.py
pause
