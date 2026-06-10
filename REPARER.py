#!/usr/bin/env python3
"""
Reparation complete — version PYTHON (pas de .bat, pas bloque par Smart App Control).

PyCharm ou PowerShell :
  python REPARER.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.find_python import find_python

REQUIRED = (
    "GameXClicker.py",
    "gxclicker.py",
    "services/bootstrap.py",
    "ui-web/index.html",
)


def _run(cmd: list[str], cwd: str = ROOT) -> int:
    print(">", " ".join(cmd))
    return subprocess.call(cmd, cwd=cwd)


def main() -> int:
    os.chdir(ROOT)
    py = find_python(ROOT)
    print("=" * 60)
    print("  REPARER.py — Game XClicker Elite")
    print(f"  Python: {py}")
    print("=" * 60)

    if sys.platform == "win32":
        print("[0/7] Unblock-File...")
        ps = f"Get-ChildItem -LiteralPath '{ROOT}' -Recurse -Force | Unblock-File -ErrorAction SilentlyContinue"
        subprocess.call(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps])

    if not os.path.isdir(os.path.join(ROOT, ".git")):
        print("ERREUR: pas de depot git. Clonez:")
        print("  git clone https://github.com/wargriff/Game_XClicker_Elite.git")
        input("Entree...")
        return 1

    backup = os.path.join(ROOT, "_backup_local")
    os.makedirs(backup, exist_ok=True)
    for name in ("START.bat", "GameXClicker.py", "profiles/default.json"):
        src = os.path.join(ROOT, name.replace("/", os.sep))
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(backup, os.path.basename(name) + ".bak"))

    print("[1/7] git fetch...")
    if _run(["git", "fetch", "origin", "main"]) != 0:
        input("git fetch echoue — Entree...")
        return 1

    print("[2/7] git reset main...")
    _run(["git", "checkout", "-B", "main", "origin/main"])
    _run(["git", "reset", "--hard", "origin/main"])

    print("[3/7] Verification fichiers...")
    missing = [f for f in REQUIRED if not os.path.isfile(os.path.join(ROOT, f.replace("/", os.sep)))]
    if missing:
        print("MANQUE:", ", ".join(missing))
        input("Entree...")
        return 1
    print("  OK")

    ui_py = os.path.join(ROOT, "ui.py")
    ui_dir = os.path.join(ROOT, "ui")
    if os.path.isfile(ui_py) and os.path.isdir(ui_dir):
        os.rename(ui_py, ui_py + ".bak")
        print("  ui.py -> ui.py.bak")

    print("[4/7] pip install...")
    subprocess.call([py, "-m", "pip", "install", "-r", "requirements.txt", "-q"], cwd=ROOT)

    print("[5/7] Node.js...")
    node = r"C:\src\node.exe"
    nodejs = os.path.join(ROOT, "nodejs")
    if os.path.isfile(node) and os.path.isdir(nodejs):
        subprocess.call([node, "--version"], cwd=nodejs)
        if not os.path.isdir(os.path.join(nodejs, "node_modules")):
            subprocess.call(["npm", "install", "--silent"], cwd=nodejs, shell=True)

    print("[6/7] CHECK_VERSION...")
    subprocess.call([py, "CHECK_VERSION.py"], cwd=ROOT)

    print("[7/7] Lancement Mission Control...")
    print()
    return subprocess.call([py, "GameXClicker.py"], cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
