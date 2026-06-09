#!/usr/bin/env python3
"""
Compat PyCharm — NE PAS MODIFIER.
Redirige vers gxclicker.py (sans ui.asset_system).
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Fix conflit ui.py / dossier ui/
_ui = os.path.join(ROOT, "ui.py")
if os.path.isfile(_ui) and os.path.isdir(os.path.join(ROOT, "ui")):
    _bak = _ui + ".bak"
    n = 0
    while os.path.exists(_bak):
        n += 1
        _bak = _ui + f".bak{n}"
    try:
        os.rename(_ui, _bak)
        print(f"[run.py] ui.py -> {os.path.basename(_bak)}")
    except OSError:
        pass
if "ui" in sys.modules:
    del sys.modules["ui"]

from gxclicker import main

if __name__ == "__main__":
    raise SystemExit(main())
