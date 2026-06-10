#!/usr/bin/env python3
"""
OUVRE MOI — un seul fichier pour tout lancer.

Windows : double-clic OUVRE_MOI.pyw  (recommande)
PyCharm  : Run OUVRE_MOI.py
PowerShell:
  Set-Location "C:/Users/wargriff/Pycharm_Project_v 3.12/Game_XClicker_Elite"
  python OUVRE_MOI.py
"""

from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def main() -> int:
    print("=" * 50)
    print("  Game XClicker Elite — Ouverture...")
    print("=" * 50)

    go = os.path.join(ROOT, "GO.py")
    if os.path.isfile(go):
        return subprocess.call([sys.executable, go], cwd=ROOT)

    gx = os.path.join(ROOT, "GameXClicker.py")
    if os.path.isfile(gx):
        subprocess.call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        return subprocess.call([sys.executable, gx], cwd=ROOT)

    print("Fichiers manquants — git pull origin main")
    input("Entree...")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
