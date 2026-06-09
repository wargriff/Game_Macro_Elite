#!/usr/bin/env python3
"""
Game XClicker Elite — POINT D'ENTREE UNIQUE
Utilise uniquement via START.bat ou Game XClicker Elite.exe
"""

from __future__ import annotations

import argparse
import os
import sys


def _setup_paths() -> str:
    if getattr(sys, "frozen", False):
        root = sys._MEIPASS  # type: ignore[attr-defined]
        dev = os.path.dirname(sys.executable)
    else:
        root = os.path.dirname(os.path.abspath(__file__))
        dev = root
    if root not in sys.path:
        sys.path.insert(0, root)
    return dev


def _fix_ui_py(dev: str) -> None:
    ui_py = os.path.join(dev, "ui.py")
    ui_dir = os.path.join(dev, "ui")
    if not (os.path.isfile(ui_py) and os.path.isdir(ui_dir)):
        return
    backup = ui_py + ".bak"
    n = 0
    while os.path.exists(backup):
        n += 1
        backup = ui_py + f".bak{n}"
    try:
        os.rename(ui_py, backup)
        print(f"[GX] ui.py renomme -> {os.path.basename(backup)}")
    except OSError as exc:
        print(f"[GX] ERREUR: fermez PyCharm puis ren ui.py ui_old.py ({exc})")
        sys.exit(1)
    if "ui" in sys.modules:
        del sys.modules["ui"]


def _optional_pyc_loader() -> None:
    try:
        import pyc_loader  # type: ignore
        pyc_loader.install()
    except ImportError:
        pass


def main(argv=None) -> int:
    dev = _setup_paths()
    _fix_ui_py(dev)
    _optional_pyc_loader()

    from utils.bootstrap import ensure_project_ready
    ensure_project_ready()

    parser = argparse.ArgumentParser(prog="Game XClicker Elite")
    parser.add_argument("--pyqt", action="store_true", help="Interface PyQt legacy")
    parser.add_argument("--web", "--browser", action="store_true", dest="browser")
    parser.add_argument("--sidecar", action="store_true", help="Sidecar seulement (console)")
    parser.add_argument("--no-splash", action="store_true", help="Sans splash")
    args = parser.parse_args(argv)

    if args.sidecar:
        from services.bootstrap import bootstrap
        ctx = bootstrap()
        print(f"[GX] Sidecar http://127.0.0.1:17840 — Ctrl+C pour quitter")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            ctx.proxy.stop()
            ctx.sidecar.stop()
            if ctx.node:
                ctx.node.stop()
        return 0

    if args.browser:
        os.environ["XCLICKER_UI"] = "browser"

    if args.pyqt:
        from Xmacro_main import main as pyqt_main
        return pyqt_main()

    from launcher.desktop_main import main as desktop_main
    return desktop_main()


if __name__ == "__main__":
    raise SystemExit(main())
