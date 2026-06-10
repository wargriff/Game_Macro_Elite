#!/usr/bin/env python3
"""
Debloque les fichiers Windows (Marque du Web) — evite le blocage Smart App Control sur .bat.

Lancez avec Python (PAS double-clic sur .bat) :
  python DEBLOQUER.py

PyCharm : Run DEBLOQUER.py
"""

from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    print("=" * 60)
    print("  DEBLOQUER — Game XClicker Elite")
    print(f"  Dossier: {ROOT}")
    print("=" * 60)
    print()

    if sys.platform != "win32":
        print("Windows uniquement — rien a debloquer.")
        return 0

    ps = f"""
$root = '{ROOT.replace("'", "''")}'
$count = 0
Get-ChildItem -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {{
    try {{
        Unblock-File -LiteralPath $_.FullName -ErrorAction SilentlyContinue
        $count++
    }} catch {{ }}
}}
Write-Host "Fichiers debloques: $count"
"""
    print("[1/2] Unblock-File sur tout le projet...")
    r = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps],
        cwd=ROOT,
    )

    print()
    print("[2/2] Si Smart App Control bloque ENCORE les .bat :")
    print()
    print("  Option A — Utilisez Python (recommande, pas bloque) :")
    print(f'    cd "{ROOT}"')
    print("    python OUVRE_MOI.py")
    print("    python REPARER.py")
    print()
    print("  Option B — Desactiver Smart App Control (une fois) :")
    print("    Parametres Windows > Confidentialite et securite")
    print("    > Securite Windows > Controle des applications et du navigateur")
    print("    > Parametres de Controle intelligent des applications")
    print("    > Desactiver")
    print()
    print("  Option C — Proprietes d'un fichier .bat :")
    print("    Clic droit > Proprietes > cocher Debloquer > OK")
    print()

    if r.returncode == 0:
        print("OK — Relancez: python OUVRE_MOI.py")
    input("Entree pour fermer...")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
