#!/usr/bin/env python3
"""
Lanceur unique PYTHON — contourne le blocage des .bat par Smart App Control.

  python GO.py

PyCharm : Run GO.py  (ou GameXClicker.py directement)
"""

from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.find_python import find_python


def main() -> int:
    os.chdir(ROOT)
    py = find_python(ROOT)

    if not os.path.isfile(os.path.join(ROOT, "GameXClicker.py")):
        print("GameXClicker.py absent — lancez: python REPARER.py")
        input("Entree...")
        return 1

    if sys.platform == "win32" and os.path.isfile(os.path.join(ROOT, "DEBLOQUER.py")):
        subprocess.call(
            ["powershell", "-ExecutionPolicy", "Bypass", "-Command",
             f"Get-ChildItem -LiteralPath '{ROOT}' -Recurse -Force | Unblock-File -ErrorAction SilentlyContinue"],
            cwd=ROOT,
        )

    if os.path.isdir(os.path.join(ROOT, ".git")):
        print("git pull origin main...")
        subprocess.call(["git", "pull", "origin", "main"], cwd=ROOT)

    subprocess.call([py, "-m", "pip", "install", "-r", "requirements.txt", "-q"], cwd=ROOT)
    print("Lancement Mission Control...\n")
    return subprocess.call([py, "GameXClicker.py"], cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
