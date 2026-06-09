"""Node.js sidecar — lance le serveur Node et forward les logs de debug."""

import json
import os
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from core.debug_log import log

NODE_PORT = 17841
NODE_URL = f"http://127.0.0.1:{NODE_PORT}"


class NodeSidecar:
    def __init__(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sidecar_dir = os.path.join(base, "nodejs", "sidecar")
        self.server_js = os.path.join(self.sidecar_dir, "server.js")
        self._process: Optional[subprocess.Popen] = None
        self._reader_thread: Optional[threading.Thread] = None
        self.online = False

    def start(self) -> bool:
        if not os.path.exists(self.server_js):
            log("NODE", f"server.js not found at {self.server_js}")
            return False

        node_bin = self._find_node()
        if not node_bin:
            log("NODE", "Node.js not found — install Node.js to use the sidecar")
            return False

        log("NODE", f"starting sidecar with {node_bin}")
        try:
            self._process = subprocess.Popen(
                [node_bin, "server.js"],
                cwd=self.sidecar_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            self._reader_thread = threading.Thread(
                target=self._read_stdout, daemon=True
            )
            self._reader_thread.start()

            if self._wait_health(timeout=5.0):
                self.online = True
                log("NODE", f"sidecar online at {NODE_URL}")
                return True

            log("NODE", "sidecar started but health check failed")
            return False
        except Exception as exc:
            log("NODE", f"failed to start: {exc}")
            return False

    def stop(self):
        if self._process:
            log("NODE", "stopping sidecar")
            self._process.terminate()
            try:
                self._process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._process.kill()
            self._process = None
        self.online = False

    def send_log(self, tag: str, msg: str, extra: Dict[str, Any]):
        if not self.online:
            return
        payload = json.dumps({
            "tag": tag,
            "msg": msg,
            "extra": extra,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{NODE_URL}/api/log",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=0.5)
        except (urllib.error.URLError, TimeoutError):
            pass

    def _read_stdout(self):
        if not self._process or not self._process.stdout:
            return
        for line in self._process.stdout:
            text = line.rstrip()
            if text:
                print(f"[NODE-OUT] {text}", flush=True)

    def _wait_health(self, timeout: float) -> bool:
        import time

        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"{NODE_URL}/health", timeout=0.5) as resp:
                    if resp.status == 200:
                        return True
            except (urllib.error.URLError, TimeoutError):
                time.sleep(0.2)
        return False

    @staticmethod
    def _find_node() -> Optional[str]:
        for candidate in ("node", "nodejs"):
            try:
                result = subprocess.run(
                    [candidate, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    return candidate
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        return None


_sidecar: Optional[NodeSidecar] = None


def start_node_sidecar() -> NodeSidecar:
    global _sidecar
    _sidecar = NodeSidecar()
    _sidecar.start()
    return _sidecar


def get_sidecar() -> Optional[NodeSidecar]:
    return _sidecar


def forward_log(tag: str, msg: str, extra: Dict[str, Any]):
    if _sidecar and _sidecar.online:
        _sidecar.send_log(tag, msg, extra)
