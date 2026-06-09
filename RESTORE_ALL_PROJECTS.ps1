# =============================================================================
# RESTAURATION projets — Pycharm_Project_v 3.12
# Lance PowerShell EN ADMINISTRATEUR si possible
# Clic droit > Executer avec PowerShell
# =============================================================================

$Root = "C:\Users\wargriff\Pycharm_Project_v 3.12"
$LogFile = Join-Path $Root "_restore_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

function Log($msg) {
    $line = "[$(Get-Date -Format 'HH:mm:ss')] $msg"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line -ErrorAction SilentlyContinue
}

if (-not (Test-Path $Root)) {
    Write-Host "Dossier introuvable: $Root" -ForegroundColor Red
    exit 1
}

Set-Location $Root
Log "=== DEBUT RESTAURATION dans $Root ==="
Log "Log: $LogFile"

# -----------------------------------------------------------------------------
# ETAPE 1 — Restaurer chaque sous-projet qui a encore un dossier .git
# (git clean a supprime les fichiers non suivis, pas l'historique Git)
# -----------------------------------------------------------------------------
Log ""
Log "=== ETAPE 1: git reset --hard dans chaque depot Git ==="

Get-ChildItem -Path $Root -Directory -Recurse -Filter ".git" -ErrorAction SilentlyContinue |
    ForEach-Object {
        $repoDir = $_.Parent.FullName
        # Ignorer node_modules/.git etc.
        if ($repoDir -match "node_modules|\.venv|venv|site-packages") { return }

        Log "Depot: $repoDir"
        Push-Location $repoDir
        try {
            git status 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) { Log "  skip (git invalide)"; return }

            $branch = git rev-parse --abbrev-ref HEAD 2>$null
            Log "  branche: $branch"

            git fetch --all 2>&1 | ForEach-Object { Log "  $_" }
            git reset --hard HEAD 2>&1 | ForEach-Object { Log "  $_" }
            git clean -fd 2>&1 | ForEach-Object { Log "  clean: $_" }

            # Restaurer fichiers trackes depuis origin si existe
            $remote = git remote get-url origin 2>$null
            if ($remote) {
                Log "  remote: $remote"
                git pull origin $branch 2>&1 | ForEach-Object { Log "  $_" }
            }
            Log "  OK"
        } catch {
            Log "  ERREUR: $_"
        } finally {
            Pop-Location
        }
    }

# -----------------------------------------------------------------------------
# ETAPE 2 — Re-cloner Game XClicker Elite (branche corrigee)
# -----------------------------------------------------------------------------
Log ""
Log "=== ETAPE 2: Game XClicker Elite (branche sanctuary) ==="

$GxOld = Join-Path $Root "Game_XClicker_Elite"
$GxNew = Join-Path $Root "Game_XClicker_Elite_Sanctuary"

if (-not (Test-Path (Join-Path $GxNew "CHECK_VERSION.py"))) {
    Log "Clone Game_XClicker_Elite_Sanctuary..."
    git clone -b cursor/sanctuary-diablo-ui-9626 `
        https://github.com/wargriff/Game_XClicker_Elite.git $GxNew 2>&1 |
        ForEach-Object { Log $_ }
} else {
    Log "Game_XClicker_Elite_Sanctuary deja present"
}

if (Test-Path $GxNew) {
    Push-Location $GxNew
    pip install -r requirements.txt 2>&1 | Out-Null
    if (Test-Path "nodejs\package.json") {
        Push-Location nodejs; npm install 2>&1 | Out-Null; Pop-Location
    }
    python CHECK_VERSION.py 2>&1 | ForEach-Object { Log $_ }
    Pop-Location
}

# Tentative recuperation Game_XClicker_Elite original si .git existe
if (Test-Path (Join-Path $GxOld ".git")) {
    Log "Recuperation Game_XClicker_Elite (depot local)..."
    Push-Location $GxOld
    git remote set-url origin https://github.com/wargriff/Game_XClicker_Elite.git 2>$null
    git fetch origin 2>&1 | ForEach-Object { Log $_ }
    git reset --hard HEAD 2>&1 | ForEach-Object { Log $_ }
    git checkout -B cursor/sanctuary-diablo-ui-9626 origin/cursor/sanctuary-diablo-ui-9626 2>&1 |
        ForEach-Object { Log $_ }
    Pop-Location
}

# -----------------------------------------------------------------------------
# ETAPE 3 — Projets sans Git: PyCharm Local History
# -----------------------------------------------------------------------------
Log ""
Log "=== ETAPE 3: Fichiers JAMAIS commites (non recuperables par Git) ==="
Log "Pour Diablo_Translator, ManaCodex, etc. sans .git:"
Log "  1. PyCharm > clic droit dossier > Local History > Show History"
Log "  2. Restaurer les fichiers un par un"
Log "  3. Ou Corbeille Windows (git clean ne met PAS a la corbeille)"
Log "  4. Ou logiciel: Recuva, Windows File Recovery (winfr)"

# -----------------------------------------------------------------------------
# ETAPE 4 — Recreer venv si supprime
# -----------------------------------------------------------------------------
Log ""
Log "=== ETAPE 4: Recreer .venv si manquant ==="

$Venv = Join-Path $Root ".venv"
if (-not (Test-Path $Venv)) {
    Log "Creation .venv..."
    python -m venv $Venv
    & "$Venv\Scripts\pip.exe" install --upgrade pip
}

# -----------------------------------------------------------------------------
# RESUME
# -----------------------------------------------------------------------------
Log ""
Log "=== TERMINE ==="
Log "Ouvre PyCharm sur:"
Log "  $GxNew"
Log "Script: Xmacro_main.py"
Log "Env: PYTHONSTARTUP=$GxNew\utils\autopatch.py"
Log ""
Log "IMPORTANT: ne JAMAIS lancer 'git clean -fd' depuis $Root"
Log "Utilise toujours: cd `"chemin\vers\UN\seul\projet`" avant git clean"

Write-Host ""
Write-Host "Log complet: $LogFile" -ForegroundColor Cyan
Write-Host "Appuie sur une touche..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
