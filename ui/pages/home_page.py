from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.styles.diablo_theme import COLORS
from ui.widgets.device_tile import DeviceTile
from ui.widgets.mural_panel import MuralPanel
from ui.widgets.sensor_panel import SensorPanel


class HomePage(QWidget):
    SIDECAR_URL = "http://127.0.0.1:17840/mission"
    SIDECAR_VERSION = "v2.1.0 · intégré"

    def __init__(self, engine, rgb, sensor_panel: SensorPanel, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.rgb = rgb
        self.sensor_panel = sensor_panel
        self._tiles = {}
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(10)

        banner = QLabel("  🖱  ⌨  🎧  💡  🌀  ")
        banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner.setFixedHeight(48)
        banner.setStyleSheet(
            f"background:rgba(12,10,8,0.85); border:1px solid {COLORS['border']};"
            f"border-radius:6px; color:{COLORS['gold_dim']}; font-size:20px;"
            f"letter-spacing:12px;"
        )
        root.addWidget(banner)

        body = QHBoxLayout()
        body.setSpacing(12)

        left = QVBoxLayout()
        left.addWidget(MuralPanel(self.rgb))
        left.addWidget(self.sensor_panel)
        left.addStretch()
        body.addLayout(left, 1)

        grid = QGridLayout()
        grid.setSpacing(10)

        tiles_def = [
            ("mouse", "SOURIS", "Detection…", "🖱", 0, 0),
            ("keyboard", "CLAVIER", "Bindings clavier", "⌨", 0, 1),
            ("commander", "COMMANDER CORE", "Canaux macro", "⚙", 0, 2),
            ("sidecar", "SIDECAR API", f"{self.SIDECAR_URL}\n{self.SIDECAR_VERSION}", "⬡", 1, 0),
            ("macro1", "MACRO 1", "Auto clic gauche", "⚡", 1, 1),
            ("macro2", "MACRO 2", "Auto clic droit", "⚡", 1, 2),
            ("mission", "MISSION CONTROL", "Vue globale", "◎", 2, 0, 1, 3),
        ]

        for item in tiles_def:
            key, title, sub, icon = item[0], item[1], item[2], item[3]
            row, col = item[4], item[5]
            rowspan = item[6] if len(item) > 6 else 1
            colspan = item[7] if len(item) > 7 else 1
            tile = DeviceTile(title, sub, icon)
            self._tiles[key] = tile
            grid.addWidget(tile, row, col, rowspan, colspan)

        body.addLayout(grid, 3)
        root.addLayout(body, 1)

        footer = QHBoxLayout()
        hint = QLabel(
            "Latéral 2 = pause globale · En pause rien ne démarre · Journal en temps réel"
        )
        hint.setStyleSheet(f"color:{COLORS['parchment_dim']}; font-size:11px;")
        dash_btn = QPushButton("Dashboard complet")
        dash_btn.setStyleSheet(f"font-size:11px; color:{COLORS['gold']};")
        footer.addWidget(hint)
        footer.addStretch()
        footer.addWidget(dash_btn)
        root.addLayout(footer)

    def refresh(self, api_online: bool = False):
        self._tiles["mouse"].set_online(True, "Connecté")
        self._tiles["keyboard"].set_online(True, "Bindings OK")
        self._tiles["commander"].set_online(self.engine.enabled, "Canaux actifs")
        self._tiles["sidecar"].set_online(api_online, f"{self.SIDECAR_URL}\n{self.SIDECAR_VERSION}")

        left_active = self.engine.is_active("left")
        right_active = self.engine.is_active("right")
        self._tiles["macro1"].set_active(
            left_active,
            f"Auto clic gauche · CPS {self.engine.get_real_cps('left')}",
        )
        self._tiles["macro2"].set_active(
            right_active,
            f"Auto clic droit · CPS {self.engine.get_real_cps('right')}",
        )

        active_count = self.engine.count_active_macros()
        self._tiles["mission"].set_active(
            self.engine.enabled and active_count > 0,
            f"{active_count} macro(s) · Moteur {'ON' if self.engine.enabled else 'OFF'}",
        )
