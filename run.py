#!/usr/bin/env python3
"""
Entree UNIQUE — PyCharm, START.bat, .exe
Ne jamais importer main.py (evite ui.asset_system sur anciennes versions).
"""

import os
import sys

# ── 1. Chemin projet ──
if getattr(sys, "frozen", False):
    _ROOT = sys._MEIPASS  # type: ignore[attr-defined]
else:
    _ROOT = os.path.dirname(os.path.abspath(__file__))

if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# ── 2. Fix ui.py conflit AVANT tout import projet ──
_dev = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else _ROOT
_ui_py = os.path.join(_dev, "ui.py")
_ui_dir = os.path.join(_dev, "ui")
if os.path.isfile(_ui_py) and os.path.isdir(_ui_dir):
    _bak = _ui_py + ".bak"
    n = 0
    while os.path.exists(_bak):
        n += 1
        _bak = _ui_py + f".bak{n}"
    try:
        os.rename(_ui_py, _bak)
        print(f"[RUN] ui.py -> {os.path.basename(_bak)}")
    except OSError as e:
        print(f"[RUN] Fermez PyCharm puis: ren ui.py ui_old.py  ({e})")
        sys.exit(1)
    if "ui" in sys.modules:
        del sys.modules["ui"]

# ── 3. Bootstrap + lancement ──
from utils.bootstrap import ensure_project_ready

ensure_project_ready(_ROOT)

from launch import run

if __name__ == "__main__":
    sys.exit(run())
