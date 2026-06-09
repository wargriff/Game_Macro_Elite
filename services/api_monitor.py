"""Polling API Sidecar sécurisé — remplace l'ancien [API] qui crashait."""

import json
import threading
import urllib.error
import urllib.request
from typing import Optional

from utils.debug import log

try:
    from utils.diagnostic_bot import say
except ImportError:
    def say(msg, level="INFO"):
        print(f"[API-MONITOR] {msg}", flush=True)


class ApiMonitor:
    """Vérifie /api/v1/health sans accéder à master_combo de façon dangereuse."""

    PORT = 17840
    URL = f"http://127.0.0.1:{PORT}/api/v1/health"

    def __init__(self, window=None, interval_ms: int = 5000):
        self.window = window
        self.interval_ms = interval_ms
        self._timer = None
        self._online = False

    def start(self, timer_factory):
        """timer_factory: callable(callback) -> QTimer-like with start(ms)."""
        if self._timer:
            return
        self._timer = timer_factory(self._poll)
        self._timer.start(self.interval_ms)
        say(f"Surveillance API → {self.URL}", "INFO")

    def _poll(self):
        log("API", self.URL)
        try:
            with urllib.request.urlopen(self.URL, timeout=1.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            self._online = data.get("status") == "ok"
            log("API", f"health OK enabled={data.get('enabled')} cps={data.get('total_cps')}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            self._online = False
            log("API", f"health OFF — {exc}")

        if self.window is not None:
            combo = getattr(self.window, "master_combo", None)
            edit = getattr(self.window, "name_edit", None)
            if combo is None or edit is None:
                say(
                    "API OK mais master_combo/name_edit absents sur MainWindow — git pull requis",
                    "WARN",
                )

    @property
    def online(self) -> bool:
        return self._online

    def stop(self):
        if self._timer and hasattr(self._timer, "stop"):
            self._timer.stop()
        self._timer = None
