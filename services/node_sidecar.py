"""Node.js sidecar — lance le serveur Node et forward les logs."""

import json
import os
import subprocess
import threading
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from core.debug_log import log

NODE_PORT = 17841
NODE_URL = f"http://127.0.0.1:{NODE_PORT}"


class NodeSidecar:
    def __init__(self, node_dir: str):
        self.node_dir = node_dir
        self.server_js = os.path.join(node_dir, "server.js")
        self._process: Optional[subprocess.Popen] = None
        self._reader_thread: Optional[threading.Thread] = None
        self.online = False

    def start(self) -> bool:
        if not os.path.exists(self.server_js):
            log("NODE", f"server.js introuvable: {self.server_js}")
            return False

        node_bin = find_node_binary()
        if not node_bin:
            log("NODE", "Node.js introuvable — installez Node.js ou placez-le dans C:\\src")
            return False

        log("NODE", f"Démarrage sidecar ({node_bin}) depuis {self.node_dir}")
        try:
            self._process = subprocess.Popen(
                [node_bin, "server.js"],
                cwd=self.node_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            self._reader_thread = threading.Thread(
                target=self._read_stdout, daemon=True
            )
            self._reader_thread.start()

            if self._wait_health(timeout=6.0):
                self.online = True
                log("NODE", f"Sidecar en ligne sur {NODE_URL}")
                return True

            log("NODE", "Sidecar démarré mais health check échoué")
            return False
        except Exception as exc:
            log("NODE", f"Échec démarrage: {exc}")
            return False

    def stop(self) -> None:
        if self._process:
            log("NODE", "Arrêt du sidecar")
            self._process.terminate()
            try:
                self._process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._process.kill()
            self._process = None
        self.online = False

    def send_log(self, tag: str, msg: str, extra: Dict[str, Any]) -> None:
        if not self.online:
            return
        payload = json.dumps({"tag": tag, "msg": msg, "extra": extra}).encode("utf-8")
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

    def run_analysis(self, project_root: str) -> Dict[str, Any]:
        analyzer = os.path.join(self.node_dir, "analyzer.js")
        if not os.path.exists(analyzer):
            return {"ok": False, "error": "analyzer.js introuvable"}

        node_bin = find_node_binary()
        if not node_bin:
            return {"ok": False, "error": "Node.js introuvable"}

        try:
            result = subprocess.run(
                [node_bin, "analyzer.js", "--project", project_root, "--fix"],
                cwd=self.node_dir,
                capture_output=True,
                text=True,
                timeout=120,
            )
            for line in (result.stdout or "").splitlines():
                if line.strip():
                    print(f"[AI-OUT] {line}", flush=True)
            for line in (result.stderr or "").splitlines():
                if line.strip():
                    print(f"[AI-ERR] {line}", flush=True)
            return {
                "ok": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "Analyse timeout"}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def _read_stdout(self) -> None:
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


_sidecar: Optional[NodeSidecar] = None


def find_node_binary() -> Optional[str]:
    import platform

    candidates = []

    if platform.system() == "Windows":
        candidates.extend([
            r"C:\src\node.exe",
            r"C:\src\node\node.exe",
            r"C:\Program Files\nodejs\node.exe",
        ])
    candidates.extend(["node", "nodejs"])

    for candidate in candidates:
        try:
            result = subprocess.run(
                [candidate, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return candidate
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            continue
    return None


def resolve_node_dir() -> str:
    import platform
    import shutil

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_dir = os.path.join(base, "nodejs", "ai-guardian")

    if platform.system() == "Windows":
        src_dir = r"C:\src\ai-guardian"
        if os.path.isdir(src_dir) and os.path.exists(os.path.join(src_dir, "server.js")):
            return src_dir
        os.makedirs(r"C:\src\ai-guardian", exist_ok=True)
        if os.path.isdir(local_dir):
            for name in os.listdir(local_dir):
                src = os.path.join(local_dir, name)
                dst = os.path.join(src_dir, name)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
            if os.path.exists(os.path.join(src_dir, "server.js")):
                log("AI", f"Modules copiés vers {src_dir}")
                return src_dir

    return local_dir


def start_node_sidecar() -> NodeSidecar:
    global _sidecar
    node_dir = resolve_node_dir()
    _sidecar = NodeSidecar(node_dir)
    _sidecar.start()
    return _sidecar


def get_sidecar() -> Optional[NodeSidecar]:
    return _sidecar


def forward_log(tag: str, msg: str, extra: Dict[str, Any]) -> None:
    if _sidecar and _sidecar.online:
        _sidecar.send_log(tag, msg, extra)
