# Game XClicker Elite — PowerShell
# Clic droit > Executer avec PowerShell  OU  dans PowerShell:  .\GO.ps1

$ErrorActionPreference = "Continue"

# Ce script doit etre dans le dossier du projet
$Root = $PSScriptRoot
if (-not (Test-Path (Join-Path $Root "GameXClicker.py"))) {
    Write-Host ""
    Write-Host "ERREUR: GameXClicker.py introuvable dans $Root" -ForegroundColor Red
    Write-Host ""
    Write-Host "1) Ouvrez PowerShell DANS le dossier du projet, ou"
    Write-Host "2) Clonez le projet:"
    Write-Host ""
    Write-Host '   Set-Location "C:\Users\wargriff\Pycharm_Project_v 3.12"'
    Write-Host '   git clone https://github.com/wargriff/Game_XClicker_Elite.git'
    Write-Host '   Set-Location ".\Game_XClicker_Elite"'
    Write-Host '   .\GO.ps1'
    Write-Host ""
    Read-Host "Entree pour fermer"
    exit 1
}

Set-Location $Root
Write-Host "Dossier projet: $Root" -ForegroundColor Green

if (Test-Path ".git") {
    Write-Host "git pull origin main..."
    $env:GIT_MERGE_AUTOEDIT = "no"
    git pull --no-edit origin main
} else {
    Write-Host "Pas de .git — clonez le depot GitHub d'abord." -ForegroundColor Yellow
}

$Py = $null
$venv1 = Join-Path (Split-Path $Root -Parent) ".venv\Scripts\python.exe"
$venv2 = Join-Path $Root ".venv\Scripts\python.exe"
if (Test-Path $venv1) { $Py = $venv1 }
elseif (Test-Path $venv2) { $Py = $venv2 }
else { $Py = "python" }

Write-Host "Python: $Py"
& $Py -m pip install -r requirements.txt -q 2>$null

Write-Host ""
Write-Host "Lancement Mission Control..." -ForegroundColor Cyan
& $Py GameXClicker.py
