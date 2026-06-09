#!/usr/bin/env python3
"""Script build .exe — appele par le centre de controle."""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def main() -> int:
    py = sys.executable
    subprocess.check_call([py, "-m", "pip", "install", "-r", "requirements.txt", "pyinstaller", "-q"])
    icon_script = os.path.join(ROOT, "scripts", "generate_icon.py")
    if os.path.isfile(icon_script):
        subprocess.call([py, icon_script])
    subprocess.check_call([py, "-m", "PyInstaller", "build.spec", "--noconfirm"])
    if sys.platform == "win32":
        ps = (
            "Get-ChildItem 'dist\\Game XClicker Elite' -Recurse -ErrorAction SilentlyContinue "
            "| Unblock-File"
        )
        subprocess.call(["powershell", "-Command", ps], cwd=ROOT)
    print("OK: dist\\Game XClicker Elite\\Game XClicker Elite.exe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
