"""Double-clic sur ce fichier pour ouvrir Mission Control (pas de .bat)."""

from __future__ import annotations

import os
import sys
import traceback

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def _show_error(message: str) -> None:
    if sys.platform == "win32":
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(0, message, "Game XClicker Elite", 0x10)
            return
        except Exception:
            pass
    print(message, file=sys.stderr)


gx = os.path.join(ROOT, "GameXClicker.py")
if not os.path.isfile(gx):
    _show_error(
        "GameXClicker.py absent.\n\nOuvrez PowerShell dans ce dossier:\npython REPARER.py"
    )
    raise SystemExit(1)

try:
    from GameXClicker import main

    raise SystemExit(main())
except SystemExit:
    raise
except Exception:
    _show_error(traceback.format_exc())
    raise SystemExit(1)
