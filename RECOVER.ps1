# RECUPERATION — copier-coller UN SEUL BLOC dans PowerShell

# IMPORTANT: guillemets obligatoires (espace dans "Pycharm_Project_v 3.12")

$GameDir = "C:\Users\wargriff\Pycharm_Project_v 3.12\Game_XClicker_Elite"

if (Test-Path $GameDir) {
    Write-Host "=== Recuperation dans Game_XClicker_Elite ===" -ForegroundColor Cyan
    Set-Location $GameDir

    if (Test-Path ".git") {
        git remote set-url origin https://github.com/wargriff/Game_XClicker_Elite.git
        git fetch origin cursor/sanctuary-diablo-ui-9626
        git checkout -B cursor/sanctuary-diablo-ui-9626 origin/cursor/sanctuary-diablo-ui-9626
        git reset --hard origin/cursor/sanctuary-diablo-ui-9626
        python CHECK_VERSION.py
    } else {
        Write-Host "Pas de .git — clone fresh necessaire" -ForegroundColor Red
    }
} else {
    Write-Host "=== Clone fresh ===" -ForegroundColor Cyan
    $Target = "C:\Users\wargriff\Pycharm_Project_v 3.12\Game_XClicker_Elite_Sanctuary"
    git clone -b cursor/sanctuary-diablo-ui-9626 https://github.com/wargriff/Game_XClicker_Elite.git $Target
    Set-Location $Target
    pip install -r requirements.txt
    Set-Location nodejs; npm install; Set-Location ..
    python CHECK_VERSION.py
    Write-Host "Ouvre PyCharm sur: $Target" -ForegroundColor Green
}

Write-Host "`nNE JAMAIS lancer 'git clean -fd' depuis Pycharm_Project_v 3.12 (dossier parent)!" -ForegroundColor Yellow
