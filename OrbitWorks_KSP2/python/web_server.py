#!/usr/bin/env python3
"""Serve OrbitWorks web UI (3D catalog) from project root."""

from __future__ import annotations

import subprocess
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORT = 8777


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self.path = "/web/index.html"
        elif path == "/catalog.json":
            self.path = "/web/catalog.json"
        return super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        print("[web]", fmt % args)


def main() -> int:
    gen = ROOT / "python" / "generate_crafts.py"
    subprocess.check_call([sys.executable, str(gen)])
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}/"
    print("=" * 56, flush=True)
    print(" OrbitWorks KSP2 — UI 3D", flush=True)
    print(f" {url}", flush=True)
    print(" Blueprints: /export/Blueprints/", flush=True)
    print("=" * 56, flush=True)
    try:
        # Don't auto-open browser in headless cloud agents
        if sys.platform == "win32":
            import webbrowser

            threading.Timer(0.4, partial(webbrowser.open, url)).start()
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStop.")
        server.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
