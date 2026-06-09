import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional


class SidecarAPI:
    PORT = 17840
    VERSION = "2.1.0"

    def __init__(self, engine_proxy):
        self.engine = engine_proxy
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None
        self.online = False

    def start(self):
        engine = self.engine
        version = self.VERSION

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def _json(self, code: int, data: dict):
                body = json.dumps(data).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                if self.path in ("/", "/health", "/api/health"):
                    self._json(200, {
                        "status": "ok",
                        "version": version,
                        "enabled": engine.enabled,
                        "active_macros": engine.count_active_macros(),
                        "total_cps": engine.get_total_cps(),
                    })
                elif self.path == "/api/status":
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
                else:
                    self._json(404, {"error": "not found"})

        try:
            self._server = HTTPServer(("127.0.0.1", self.PORT), Handler)
            self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
            self._thread.start()
            self.online = True
            print(f"[SIDECAR] API en ligne sur http://127.0.0.1:{self.PORT}")
        except OSError as exc:
            self.online = False
            print(f"[SIDECAR] API hors ligne: {exc}")

    def stop(self):
        if self._server:
            self._server.shutdown()
            self.online = False
