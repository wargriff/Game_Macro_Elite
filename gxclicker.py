#!/usr/bin/env python3
"""Game XClicker Elite — entree unique (START.bat / .exe). Interface web iCUE."""

from __future__ import annotations

import os
import sys
import time
import webbrowser


def _root() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.abspath(__file__))


def _dev_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _prepare() -> None:
    root = _root()
    dev = _dev_dir()
    if root not in sys.path:
        sys.path.insert(0, root)

    ui_py = os.path.join(dev, "ui.py")
    ui_dir = os.path.join(dev, "ui")
    if os.path.isfile(ui_py) and os.path.isdir(ui_dir):
        bak = ui_py + ".bak"
        n = 0
        while os.path.exists(bak):
            n += 1
            bak = ui_py + f".bak{n}"
        try:
            os.rename(ui_py, bak)
        except OSError:
            pass
    if "ui" in sys.modules:
        mod = sys.modules["ui"]
        if (getattr(mod, "__file__", "") or "").replace("\\", "/").endswith("/ui.py"):
            del sys.modules["ui"]


def _run_app() -> int:
    from services.bootstrap import bootstrap

    APP_TITLE = "Game XClicker Elite — SOURIS WARGRIFF"
    ctx = None
    url = "http://127.0.0.1:17840"
    try:
        ctx = bootstrap()
        url = "http://127.0.0.1:5173"
        if ctx.node:
            deadline = time.time() + 6
            while time.time() < deadline and not ctx.node.online:
                time.sleep(0.2)
            if not ctx.node.online:
                url = "http://127.0.0.1:17840"

        import webview
        webview.create_window(
            APP_TITLE, url,
            width=1280, height=820,
            min_size=(1024, 640),
            background_color="#1a1a1a",
        )
        webview.start()
    except ImportError:
        webbrowser.open(url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    except Exception as exc:
        print(f"[GX] Erreur: {exc}")
        input("Entree pour fermer...")
        return 1
    finally:
        if ctx:
            ctx.proxy.stop()
            ctx.sidecar.stop()
            if ctx.node:
                ctx.node.stop()
    return 0


def main() -> int:
    _prepare()
    return _run_app()


if __name__ == "__main__":
    raise SystemExit(main())
