#!/usr/bin/env python3
"""
Point d'entrée unique — Centre de contrôle.

  main.py              → hub visuel (défaut)
  main.py --native     → interface PyQt6 directe
  main.py --web        → interface web
  main.py --build      → build .exe (console)
"""

from __future__ import annotations

import sys


def main() -> int:
    args = sys.argv[1:]

    if "--native" in args:
        from native_app import main as native_main

        return native_main()

    if "--web" in args:
        from gxclicker import main as web_main

        return web_main()

    if "--build" in args:
        import os
        import subprocess

        root = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(root, "scripts", "build_exe.py")
        return subprocess.call([sys.executable, script], cwd=root)

    from ui.control_center import main as hub_main

    return hub_main()


if __name__ == "__main__":
    raise SystemExit(main())
