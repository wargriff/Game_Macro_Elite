#!/usr/bin/env python3
"""
Routeur interne — modes avancés uniquement.

  (défaut)              → Control Panel
  --native               → interface PyQt6
  --web                  → interface web
  --build [--desktop]    → compile .exe
  --repair               → REPARER.py (sans relancer)

Usage quotidien : OUVRE_MOI.py / OUVRE_MOI.pyw
"""

from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    from launcher import prepare

    prepare(ROOT)
    args = sys.argv[1:]

    if "--repair" in args:
        from REPARER import main as repair_main

        return repair_main(launch=False)

    if "--native" in args:
        from native_app import main as native_main

        return native_main()

    if "--web" in args:
        from gxclicker import main as web_main

        return web_main()

    if "--build" in args:
        script = os.path.join(ROOT, "scripts", "build_exe.py")
        extra = ["--desktop"] if "--desktop" in args else []
        return subprocess.call([sys.executable, script, *extra], cwd=ROOT)

    from ui.control_panel import main as panel_main

    return panel_main()


if __name__ == "__main__":
    raise SystemExit(main())
