"""Centre de contrôle — tout en 1 avant de lancer l'app."""

from __future__ import annotations

import os
import subprocess
import sys
from typing import Optional

from PyQt6.QtCore import QProcess, Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from config.runtime import exe_dir, project_root
from ui.styles.icue_theme import ICUE

ROOT = project_root()


class ActionCard(QFrame):
    def __init__(
        self,
        title: str,
        subtitle: str,
        icon: str,
        on_click=None,
        parent=None,
    ):
        super().__init__(parent)
        self._on_click = on_click
        self.setObjectName("ActionCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumSize(220, 130)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(6)

        top = QHBoxLayout()
        ic = QLabel(icon)
        ic.setFont(QFont("Segoe UI", 22))
        ic.setStyleSheet(f"color:{ICUE['yellow']};")
        top.addWidget(ic)
        top.addStretch()
        lay.addLayout(top)

        t = QLabel(title)
        t.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        t.setStyleSheet(f"color:{ICUE['text']}; letter-spacing:0.5px;")
        lay.addWidget(t)

        sub = QLabel(subtitle)
        sub.setWordWrap(True)
        sub.setStyleSheet(f"color:{ICUE['text_dim']}; font-size:10px;")
        lay.addWidget(sub)
        lay.addStretch()

        self.setStyleSheet(
            f"ActionCard {{ background:{ICUE['bg_panel']}; border:1px solid {ICUE['border']};"
            f"border-radius:6px; }}"
            f"ActionCard:hover {{ border-color:{ICUE['yellow_dim']}; }}"
        )

    def mousePressEvent(self, event):
        if self._on_click and self.isEnabled():
            self._on_click()
        super().mousePressEvent(event)


class ControlCenterWindow(QMainWindow):
    EXE_REL = os.path.join("dist", "Game XClicker Elite", "Game XClicker Elite.exe")

    def __init__(self):
        super().__init__()
        self._build_proc: Optional[QProcess] = None
        self.setWindowTitle("Game XClicker Elite — Centre de contrôle")
        self.resize(720, 560)
        self.setStyleSheet(f"background:{ICUE['bg_main']}; color:{ICUE['text']};")
        self._build_ui()
        self.refresh_status()
        QTimer.singleShot(500, self.refresh_status)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(14)

        head = QLabel("GAME XCLICKER ELITE — CENTRE DE CONTRÔLE")
        head.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        head.setStyleSheet(f"color:{ICUE['yellow']}; letter-spacing:1px;")
        root.addWidget(head)

        hint = QLabel(
            "Choisissez un mode ci-dessous. Tout est regroupé ici — un seul programme à lancer (main.py / START.bat)."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet(f"color:{ICUE['text_dim']}; font-size:11px;")
        root.addWidget(hint)

        status_row = QHBoxLayout()
        self.status_labels = {}
        for key, label in (
            ("py", "Python"),
            ("node", "Node.js"),
            ("exe", ".exe"),
            ("deps", "Deps"),
        ):
            box = QFrame()
            box.setStyleSheet(
                f"background:{ICUE['bg_panel']}; border:1px solid {ICUE['border']};"
                f"border-radius:4px; padding:8px 12px;"
            )
            bl = QVBoxLayout(box)
            bl.setSpacing(2)
            t = QLabel(label)
            t.setStyleSheet(f"color:{ICUE['text_dim']}; font-size:9px;")
            v = QLabel("…")
            v.setStyleSheet(f"color:{ICUE['text']}; font-size:11px; font-weight:600;")
            bl.addWidget(t)
            bl.addWidget(v)
            self.status_labels[key] = v
            status_row.addWidget(box, 1)
        root.addLayout(status_row)

        grid = QGridLayout()
        grid.setSpacing(12)

        self.card_native = ActionCard(
            "INTERFACE NATIVE",
            "PyQt6 iCUE — fenêtre Windows, macros, devices",
            "🖥",
            on_click=self._launch_native,
        )
        self.card_web = ActionCard(
            "INTERFACE WEB",
            "Preview HTML iCUE dans le navigateur / pywebview",
            "🌐",
            on_click=self._launch_web,
        )
        self.card_build = ActionCard(
            "BUILD .EXE",
            "Compile Game XClicker Elite.exe (PyInstaller)",
            "📦",
            on_click=self._start_build,
        )
        self.card_exe = ActionCard(
            "LANCER .EXE",
            "Ouvre le programme compilé (après build)",
            "▶",
            on_click=self._launch_exe,
        )

        for i, card in enumerate(
            (self.card_native, self.card_web, self.card_build, self.card_exe)
        ):
            grid.addWidget(card, i // 2, i % 2)

        root.addLayout(grid)

        log_title = QLabel("JOURNAL")
        log_title.setStyleSheet(
            f"color:{ICUE['text_dim']}; font-size:10px; letter-spacing:1px;"
        )
        root.addWidget(log_title)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(120)
        self.log.setStyleSheet(
            f"background:{ICUE['bg_input']}; border:1px solid {ICUE['border']};"
            f"color:{ICUE['text_dim']}; font-family:Consolas;font-size:10px;"
        )
        root.addWidget(self.log)

        foot = QHBoxLayout()
        btn_refresh = QPushButton("Actualiser statut")
        btn_refresh.clicked.connect(self.refresh_status)
        btn_repair = QPushButton("REPARER (git pull)")
        btn_repair.clicked.connect(self._run_repair)
        foot.addWidget(btn_refresh)
        foot.addStretch()
        foot.addWidget(btn_repair)
        root.addLayout(foot)

    def _log(self, msg: str):
        self.log.append(msg)

    def _python(self) -> str:
        return sys.executable

    def _exe_path(self) -> str:
        return os.path.join(exe_dir(), self.EXE_REL)

    def _node_path(self) -> Optional[str]:
        for p in (
            os.environ.get("XCLICKER_NODE_PATH", ""),
            r"C:\src\node.exe",
            r"C:\Program Files\nodejs\node.exe",
        ):
            if p and os.path.isfile(p):
                return p
        return None

    def refresh_status(self):
        py_ok = os.path.isfile(self._python())
        self.status_labels["py"].setText("OK" if py_ok else "Manquant")
        self.status_labels["py"].setStyleSheet(
            f"color:{'#4caf50' if py_ok else '#e53935'}; font-size:11px; font-weight:600;"
        )

        node = self._node_path()
        self.status_labels["node"].setText("OK" if node else "Optionnel")
        self.status_labels["node"].setStyleSheet(
            f"color:{'#4caf50' if node else ICUE['text_dim']}; font-size:11px; font-weight:600;"
        )

        exe = self._exe_path()
        exe_ok = os.path.isfile(exe)
        self.status_labels["exe"].setText("Prêt" if exe_ok else "Pas build")
        self.status_labels["exe"].setStyleSheet(
            f"color:{'#4caf50' if exe_ok else ICUE['yellow']}; font-size:11px; font-weight:600;"
        )

        req = os.path.join(ROOT, "requirements.txt")
        deps_ok = os.path.isfile(req) and os.path.isfile(os.path.join(ROOT, "main.py"))
        self.status_labels["deps"].setText("OK" if deps_ok else "Incomplet")
        self.status_labels["deps"].setStyleSheet(
            f"color:{'#4caf50' if deps_ok else '#e53935'}; font-size:11px; font-weight:600;"
        )

        self.card_exe.setEnabled(exe_ok)
        if not exe_ok:
            self.card_exe.setStyleSheet(
                f"ActionCard {{ background:{ICUE['bg_row']}; border:1px solid {ICUE['border']};"
                f"border-radius:6px; }}"
            )
        else:
            self.card_exe.setStyleSheet(
                f"ActionCard {{ background:{ICUE['bg_panel']}; border:1px solid {ICUE['yellow_dim']};"
                f"border-radius:6px; }}"
            )

    def _launch_native(self):
        self._log("→ Lancement interface native PyQt6…")
        self.hide()
        from native_app import main as native_main

        code = native_main()
        self.show()
        self.refresh_status()
        if code != 0:
            self._log(f"Native terminé avec code {code}")

    def _launch_web(self):
        self._log("→ Lancement interface web…")
        os.environ["GX_BROWSER"] = "1"
        self.hide()
        from gxclicker import main as web_main

        code = web_main()
        self.show()
        self.refresh_status()
        if code != 0:
            self._log(f"Web terminé avec code {code}")

    def _start_build(self):
        if self._build_proc and self._build_proc.state() != QProcess.ProcessState.NotRunning:
            self._log("Build déjà en cours…")
            return

        self._log("→ Build .exe démarré (patience 2-5 min)…")
        self._build_proc = QProcess(self)
        self._build_proc.setWorkingDirectory(ROOT)
        self._build_proc.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self._build_proc.readyReadStandardOutput.connect(self._on_build_output)
        self._build_proc.finished.connect(self._on_build_finished)

        py = self._python()
        script = os.path.join(ROOT, "scripts", "build_exe.py")
        if os.path.isfile(script):
            self._build_proc.start(py, [script])
        else:
            self._build_proc.start(
                py,
                ["-m", "PyInstaller", "build.spec", "--noconfirm"],
            )

    def _on_build_output(self):
        if not self._build_proc:
            return
        data = self._build_proc.readAllStandardOutput().data().decode("utf-8", errors="replace")
        for line in data.strip().splitlines():
            if line.strip():
                self.log.append(line.strip())

    def _on_build_finished(self, code: int, _status):
        if code == 0:
            self._log("✓ Build OK — dist\\Game XClicker Elite\\Game XClicker Elite.exe")
        else:
            self._log(f"✗ Build échoué (code {code})")
        self.refresh_status()

    def _launch_exe(self):
        path = self._exe_path()
        if not os.path.isfile(path):
            self._log("✗ .exe absent — cliquez BUILD .EXE d'abord")
            return
        self._log(f"→ Lancement {path}")
        try:
            if sys.platform == "win32":
                os.startfile(path)  # type: ignore[attr-defined]
            else:
                subprocess.Popen([path], cwd=os.path.dirname(path))
        except OSError as exc:
            self._log(f"✗ Erreur lancement: {exc}")

    def _run_repair(self):
        repair = os.path.join(ROOT, "REPARER.bat")
        if not os.path.isfile(repair):
            self._log("REPARER.bat introuvable")
            return
        self._log("→ REPARER.bat (fenêtre séparée)…")
        subprocess.Popen(["cmd", "/c", repair], cwd=ROOT, creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0))


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Game XClicker Elite Control")
    win = ControlCenterWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
