"""IA Guardian — analyse le projet via Node.js (C:\\src) et affiche dans le terminal."""

import os
import threading
from typing import Optional

from core.debug_log import log, set_node_forwarder
from services.node_sidecar import forward_log, get_sidecar, start_node_sidecar


class AIGuardian:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.sidecar = None
        self._watch_thread: Optional[threading.Thread] = None
        self._watching = False

    def start(self) -> bool:
        log("AI", "Démarrage IA Guardian...")
        set_node_forwarder(forward_log)

        self.sidecar = start_node_sidecar()
        if not self.sidecar.online:
            log("AI", "Sidecar Node hors ligne — analyse locale uniquement")
            return self._run_local_analysis()

        result = self.sidecar.run_analysis(self.project_root)
        if result.get("ok"):
            log("AI", "Analyse terminée — aucune erreur bloquante")
        else:
            log("AI", "Analyse terminée avec avertissements", detail=result.get("error", ""))

        self._watching = True
        self._watch_thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._watch_thread.start()
        return True

    def stop(self) -> None:
        self._watching = False
        if self.sidecar:
            self.sidecar.stop()

    def _run_local_analysis(self) -> bool:
        import py_compile

        errors = 0
        fixed = 0
        for root, _, files in os.walk(self.project_root):
            if any(skip in root for skip in (".git", "__pycache__", "node_modules")):
                continue
            for name in files:
                if not name.endswith(".py"):
                    continue
                path = os.path.join(root, name)
                try:
                    py_compile.compile(path, doraise=True)
                except py_compile.PyCompileError as exc:
                    errors += 1
                    log("AI", f"Erreur syntaxe: {path}", detail=str(exc))
        log("AI", f"Scan local: {errors} erreur(s), {fixed} correction(s)")
        return errors == 0

    def _watch_loop(self) -> None:
        import time

        while self._watching:
            time.sleep(30)
            if self.sidecar and self.sidecar.online:
                log("AI", "Re-analyse périodique...")
                self.sidecar.run_analysis(self.project_root)


_guardian: Optional[AIGuardian] = None


def start_ai_guardian(project_root: Optional[str] = None) -> AIGuardian:
    global _guardian
    if project_root is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _guardian = AIGuardian(project_root)
    _guardian.start()
    return _guardian


def stop_ai_guardian() -> None:
    global _guardian
    if _guardian:
        _guardian.stop()
        _guardian = None
