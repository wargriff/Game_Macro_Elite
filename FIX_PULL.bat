@echo off
title Fix Git Pull — Game XClicker Elite
cd /d "%~dp0"

echo.
echo ============================================================
echo   FIX PULL — remplace le code local par la branche corrigee
echo ============================================================
echo.
echo Sauvegarde dans _backup_local\ ...
if not exist "_backup_local" mkdir "_backup_local"
if not exist "_backup_local\untracked" mkdir "_backup_local\untracked"

copy /Y "Xmacro_main.py" "_backup_local\" 2>nul
copy /Y "README.md" "_backup_local\" 2>nul
copy /Y "profiles\default.json" "_backup_local\" 2>nul
copy /Y "START.bat" "_backup_local\untracked\" 2>nul
copy /Y "ui\main_window.py" "_backup_local\untracked\" 2>nul

echo.
echo Fetch branche sanctuary...
git fetch origin cursor/sanctuary-diablo-ui-9626
if errorlevel 1 (
    echo ERREUR git fetch
    pause
    exit /b 1
)

echo.
echo Bascule sur cursor/sanctuary-diablo-ui-9626 (ecrase modifications locales)...
git checkout -B cursor/sanctuary-diablo-ui-9626 origin/cursor/sanctuary-diablo-ui-9626
if errorlevel 1 (
    echo checkout echoue — nettoyage fichiers non suivis...
    git clean -fd
    git checkout -B cursor/sanctuary-diablo-ui-9626 origin/cursor/sanctuary-diablo-ui-9626
)

git reset --hard origin/cursor/sanctuary-diablo-ui-9626

echo.
echo === Verification ===
if not exist "CHECK_VERSION.py" (
    echo ERREUR: CHECK_VERSION.py toujours absent
    pause
    exit /b 1
)

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" CHECK_VERSION.py
) else (
    python CHECK_VERSION.py
)

echo.
echo === npm nodejs ===
if exist "nodejs\package.json" (
    pushd nodejs
    call npm install
    popd
)

echo.
echo OK — Lance: python Xmacro_main.py
echo Tu DOIS voir: [XMACRO] launcher sanctuary v2.2 + Sanctuary Bot
echo.
pause
