"""Verification START.bat + gxclicker.py."""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

FILES = [
    "START.bat",
    "gxclicker.py",
    "build.spec",
    "config/asset_system.py",
    "ui-web/index.html",
    "assets/brand/favicon.ico",
    "services/sidecar_api.py",
]

DEAD = [
    "run.py", "main.py", "launch.py", "BUILD.bat", "FIX_START.bat",
    "launchers/START.bat", "Xmacro_main.bat", "xmacro_game.bat",
]


def main() -> int:
    print("=== Verification ===")
    ok = True
    for f in FILES:
        p = os.path.join(ROOT, f.replace("/", os.sep))
        if os.path.isfile(p):
            print(f"[ OK ] {f}")
        else:
            print(f"[FAIL] {f}")
            ok = False
    for f in DEAD:
        if os.path.isfile(os.path.join(ROOT, f.replace("/", os.sep))):
            print(f"[WARN] a supprimer: {f}")
            ok = False
    if os.path.isfile(os.path.join(ROOT, "ui.py")):
        print("[WARN] ui.py present — START.bat le renomme")
    print("\nPRET" if ok else "\nINCOMPLET")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
