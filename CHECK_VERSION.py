"""Vérifie gxclicker.py + START.bat + assets."""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

REQUIRED = [
    ("gxclicker.py", "_fix_ui_py"),
    ("START.bat", "Game XClicker Elite.exe"),
    ("BUILD.bat", "PyInstaller"),
    ("config/asset_system.py", "AssetSystem"),
    ("ui-web/index.html", "Game XClicker Elite"),
    ("assets/brand/favicon.ico", None),
    ("services/sidecar_api.py", "_serve_static"),
]


def main() -> int:
    print("=== Game XClicker Elite — verification ===")
    ok = True

    if os.path.isfile(os.path.join(ROOT, "ui.py")) and os.path.isdir(os.path.join(ROOT, "ui")):
        print("[WARN] ui.py present — START.bat le renomme auto en ui.py.bak")

    for rel, needle in REQUIRED:
        path = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.isfile(path):
            print(f"[FAIL] manquant: {rel}")
            ok = False
            continue
        if needle:
            with open(path, encoding="utf-8", errors="ignore") as f:
                if needle not in f.read():
                    print(f"[FAIL] {rel} obsolete — git pull requis")
                    ok = False
                else:
                    print(f"[ OK ] {rel}")
        else:
            print(f"[ OK ] {rel}")

    if ok:
        print("\nPRET — double-clic START.bat")
        print("Build .exe — START.bat build")
        return 0
    print("\nINCOMPLET — git pull origin cursor/icue-web-launcher-9626")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
