"""Lance et arrête le serveur Node.js (Mission Control port 5173)."""

import os
import shutil
import subprocess
import sys
import threading
from typing import Optional

from utils.debug import log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODE_DIR = os.path.join(BASE_DIR, "nodejs")

# Chemins Node.js Windows (user: C:\\src)
NODE_CANDIDATES = [
    os.environ.get("XCLICKER_NODE_PATH", ""),
    r"C:\src\node.exe",
    r"C:\src\node\node.exe",
    r"C:\Program Files\nodejs\node.exe",
    shutil.which("node") or "",
]


class NodeBridge:
    PORT = 5173
    URL = f"http://127.0.0.1:{PORT}"

    def __init__(self):
        self._proc: Optional[subprocess.Popen] = None
        self.online = False
        self.node_exe = self._find_node()

    def _find_node(self) -> Optional[str]:
        for path in NODE_CANDIDATES:
            if path and os.path.isfile(path):
                log("NODE", f"Node trouvé: {path}")
                return path
        log("NODE", "Node.js introuvable — installez-le ou définissez XCLICKER_NODE_PATH")
        return None

    def _ensure_deps(self) -> bool:
        node_modules = os.path.join(NODE_DIR, "node_modules")
        if os.path.isdir(node_modules):
            return True
        log(
            "NODE",
            "node_modules absent — lancez d'abord: cd nodejs && npm install\n"
            "         (Node sera ignoré au démarrage, l'app Python fonctionne quand même)",
        )
        return False

    def start(self):
        if not self.node_exe:
            return
        server_js = os.path.join(NODE_DIR, "server.js")
        if not os.path.isfile(server_js):
            log("NODE", f"server.js absent: {server_js}")
            return
        if not self._ensure_deps():
            return
        env = os.environ.copy()
        env["XCLICKER_NODE_PORT"] = str(self.PORT)
        env["XCLICKER_API_URL"] = "http://127.0.0.1:17840"
        try:
            self._proc = subprocess.Popen(
                [self.node_exe, server_js],
                cwd=NODE_DIR,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            self.online = True
            threading.Thread(target=self._read_stdout, daemon=True).start()
            log("NODE", f"Serveur démarré → {self.URL}")
        except Exception as exc:
            self.online = False
            log("NODE", f"Démarrage échoué: {exc}")

    def _read_stdout(self):
        if not self._proc or not self._proc.stdout:
            return
        for line in self._proc.stdout:
            line = line.rstrip()
            if line:
                log("NODE", line)

    def stop(self):
        if self._proc:
            try:
                self._proc.terminate()
                self._proc.wait(timeout=3)
            except Exception:
                try:
                    self._proc.kill()
                except Exception:
                    pass
            self._proc = None
        self.online = False
        log("NODE", "Serveur arrêté")
