# Obsolète — redirige vers le lanceur unique OUVRE_MOI.py
$Root = $PSScriptRoot
Set-Location $Root

$Py = $null
$venv1 = Join-Path (Split-Path $Root -Parent) ".venv\Scripts\python.exe"
$venv2 = Join-Path $Root ".venv\Scripts\python.exe"
if (Test-Path $venv1) { $Py = $venv1 }
elseif (Test-Path $venv2) { $Py = $venv2 }
else { $Py = "python" }

& $Py (Join-Path $Root "OUVRE_MOI.py")
exit $LASTEXITCODE
