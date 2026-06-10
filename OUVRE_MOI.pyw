"""Double-clic sur ce fichier pour ouvrir Mission Control (pas de .bat)."""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

py = sys.executable.replace("pythonw.exe", "python.exe").replace("pythonw", "python")
gx = os.path.join(ROOT, "GameXClicker.py")

if not os.path.isfile(gx):
    import ctypes
    ctypes.windll.user32.MessageBoxW(
        0,
        "GameXClicker.py absent.\n\nOuvrez PowerShell dans ce dossier:\npython REPARER.py",
        "Game XClicker Elite",
        0x10,
    )
    raise SystemExit(1)

subprocess.Popen([py, gx], cwd=ROOT)
