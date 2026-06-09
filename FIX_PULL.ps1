# Fix Git Pull — PowerShell (copier-coller tout le bloc)

Set-Location "C:\Users\wargriff\Pycharm_Project_v 3.12\Game_XClicker_Elite"

Write-Host "=== Sauvegarde locale ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "_backup_local" | Out-Null
Copy-Item Xmacro_main.py, README.md -Destination "_backup_local\" -ErrorAction SilentlyContinue
Copy-Item profiles\default.json -Destination "_backup_local\" -ErrorAction SilentlyContinue

Write-Host "=== Fetch + bascule branche corrigee ===" -ForegroundColor Cyan
git fetch origin cursor/sanctuary-diablo-ui-9626
git checkout -B cursor/sanctuary-diablo-ui-9626 origin/cursor/sanctuary-diablo-ui-9626
if ($LASTEXITCODE -ne 0) {
    Write-Host "Nettoyage fichiers non suivis..." -ForegroundColor Yellow
    git clean -fd
    git checkout -B cursor/sanctuary-diablo-ui-9626 origin/cursor/sanctuary-diablo-ui-9626
}
git reset --hard origin/cursor/sanctuary-diablo-ui-9626

Write-Host "=== Verification ===" -ForegroundColor Cyan
python CHECK_VERSION.py
if ($LASTEXITCODE -ne 0) { Write-Host "ECHEC verification" -ForegroundColor Red; exit 1 }

Write-Host "=== npm install ===" -ForegroundColor Cyan
Set-Location nodejs; npm install; Set-Location ..

Write-Host "=== Lancement ===" -ForegroundColor Green
$env:PYTHONSTARTUP = "$PWD\utils\autopatch.py"
$env:XMACRO_DEBUG = "1"
$env:XMACRO_BOT = "1"
python Xmacro_main.py
