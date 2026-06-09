"""Polling API Sidecar — thread séparé, zéro blocage UI."""

import json
import threading
import urllib.error
import urllib.request

from utils.debug import log, log_verbose


class ApiMonitor:
    PORT = 17840
    URL = f"http://127.0.0.1:{PORT}/api/v1/health"

    def __init__(self, window=None, interval_ms: int = 10000):
        self.window = window
        self.interval_ms = interval_ms
        self._timer = None
        self._online = False
        self._warned_attrs = False
        self._polling = False

    def start(self, timer_factory):
        if self._timer:
            return
        self._timer = timer_factory(self._poll_async)
        self._timer.start(self.interval_ms)
        log_verbose("API", f"monitor → {self.URL} every {self.interval_ms}ms")

    def _poll_async(self):
        if self._polling:
            return
        self._polling = True
        threading.Thread(target=self._poll_network, daemon=True).start()

    def _poll_network(self):
        try:
            with urllib.request.urlopen(self.URL, timeout=1.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            self._online = data.get("status") == "ok"
            log_verbose(
                "API",
                f"OK enabled={data.get('enabled')} cps={data.get('total_cps')}",
            )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            self._online = False
            log_verbose("API", f"OFF — {exc}")
        finally:
            self._polling = False

        if self.window and not self._warned_attrs:
            if not getattr(self.window, "master_combo", None) or not getattr(
                self.window, "name_edit", None
            ):
                log("API", "master_combo/name_edit OK via patch")
            self._warned_attrs = True

    @property
    def online(self) -> bool:
        return self._online

    def stop(self):
        if self._timer and hasattr(self._timer, "stop"):
            self._timer.stop()
        self._timer = None
