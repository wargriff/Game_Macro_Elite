"""
Game XClicker Elite — Launcher bureau (interface JS iCUE + moteur Python).
Fonctionne sans Node.js : UI servie par Sidecar sur port 17840.
"""

import os
import sys
import time
import webbrowser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import utils.autopatch  # noqa: F401

from config.paths import resolve_icon
from services.bootstrap import bootstrap
from utils.debug import log

APP_TITLE = "Game XClicker Elite — SOURIS WARGRIFF"
NODE_URL = "http://127.0.0.1:5173"
SIDECAR_URL = "http://127.0.0.1:17840"


def _wait_node(node, timeout=8.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if node and node.online:
            return True
        time.sleep(0.2)
    return bool(node and node.online)


def _pick_ui_url(node) -> str:
    if node and _wait_node(node, timeout=6.0):
        return NODE_URL
    log("LAUNCHER", "Node.js absent — UI via Sidecar Python (17840)")
    return SIDECAR_URL


def _run_webview(url: str):
    import webview

    icon = resolve_icon()
    window = webview.create_window(
        APP_TITLE,
        url,
        width=1280,
        height=820,
        min_size=(1024, 640),
        background_color="#1a1a1a",
    )
    webview.start(debug=os.environ.get("XMACRO_DEBUG") == "1")


def _run_browser(url: str):
    webbrowser.open(url)
    print(f"[LAUNCHER] Navigateur → {url}")
    print("[LAUNCHER] Ctrl+C pour quitter")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


def main() -> int:
    print("[LAUNCHER] Game XClicker Elite v3.1")
    ctx = None
    try:
        ctx = bootstrap()
        url = _pick_ui_url(ctx.node)
        print(f"[LAUNCHER] Interface → {url}")

        mode = os.environ.get("XCLICKER_UI", "webview").lower()
        if mode == "browser":
            _run_browser(url)
        else:
            try:
                _run_webview(url)
            except ImportError:
                print("[LAUNCHER] pip install pywebview")
                _run_browser(url)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print(f"[LAUNCHER] Erreur: {exc}")
        input("Appuyez Entree pour fermer...")
        return 1
    finally:
        if ctx:
            ctx.proxy.stop()
            ctx.sidecar.stop()
            if ctx.node:
                ctx.node.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
