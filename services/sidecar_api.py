import json
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MISSION_HTML = os.path.join(BASE_DIR, "web", "mission-control", "index.html")


class SidecarAPI:
    PORT = 17840
    VERSION = "2.1.0"
    MISSION_URL = f"http://127.0.0.1:{PORT}/mission"

    def __init__(self, engine_proxy):
        self.engine = engine_proxy
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None
        self.online = False
        self._mission_html: Optional[bytes] = None

    def _load_mission_html(self) -> bytes:
        if self._mission_html is not None:
            return self._mission_html
        if os.path.exists(MISSION_HTML):
            with open(MISSION_HTML, "r", encoding="utf-8") as f:
                self._mission_html = f.read().encode("utf-8")
        else:
            self._mission_html = b"<html><body>Mission Control unavailable</body></html>"
        return self._mission_html

    def start(self):
        engine = self.engine
        version = self.VERSION
        sidecar = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def _json(self, code: int, data: dict):
                body = json.dumps(data).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _html(self, code: int, body: bytes):
                self.send_response(code)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                path = self.path.split("?")[0]

                if path in ("/mission", "/mission/"):
                    self._html(200, sidecar._load_mission_html())
                    return

                if path in ("/health", "/api/health"):
                    self._json(200, {
                        "status": "ok",
                        "version": version,
                        "enabled": engine.enabled,
                        "active_macros": engine.count_active_macros(),
                        "total_cps": engine.get_total_cps(),
                    })
                    return

                if path == "/api/status":
                    self._json(200, {
                        "engine": "active" if engine.enabled else "stasis",
                        "macros": {
                            k: {
                                "active": engine.is_active(k),
                                "cps": engine.get_real_cps(k),
                            }
                            for k in engine.buttons
                        },
                    })
                    return

                if path == "/":
                    self.send_response(302)
                    self.send_header("Location", "/mission")
                    self.end_headers()
                    return

                self._json(404, {"error": "not found"})

        try:
            self._server = HTTPServer(("127.0.0.1", self.PORT), Handler)
            self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
            self._thread.start()
            self.online = True
            print(f"[SIDECAR] API + Mission Control sur http://127.0.0.1:{self.PORT}")
        except OSError as exc:
            self.online = False
            print(f"[SIDECAR] API hors ligne: {exc}")

    def stop(self):
        if self._server:
            self._server.shutdown()
            self.online = False
