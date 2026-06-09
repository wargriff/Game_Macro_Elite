from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.styles.diablo_theme import COLORS


class SensorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        title = QLabel("SENSORS")
        title.setStyleSheet(
            f"color:{COLORS['gold']}; font-weight:bold; letter-spacing:2px; font-size:11px;"
        )
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(6)

        self.cpu_lbl = self._metric("CPU", "0%")
        self.ram_lbl = self._metric("RAM", "—")
        self.load_lbl = self._metric("Load moteur", "0 macro(s) · CPS 0")
        self.api_lbl = self._metric("API REST", "Hors ligne")

        grid.addWidget(self.cpu_lbl, 0, 0)
        grid.addWidget(self.ram_lbl, 1, 0)
        grid.addWidget(self.load_lbl, 2, 0)
        grid.addWidget(self.api_lbl, 3, 0)
        layout.addLayout(grid)

        self.rescan_btn = QPushButton("Rescan devices")
        self.rescan_btn.setStyleSheet(
            f"font-size:11px; padding:4px 8px; color:{COLORS['parchment_dim']};"
        )
        layout.addWidget(self.rescan_btn)

        self.setStyleSheet(
            f"background:rgba(14,12,10,0.92); border:1px solid {COLORS['border']};"
            f"border-radius:6px; padding:10px;"
        )

    def _metric(self, name: str, value: str) -> QLabel:
        lbl = QLabel(f"{name}: {value}")
        lbl.setStyleSheet(f"color:{COLORS['parchment_dim']}; font-size:11px;")
        lbl.setProperty("metric_name", name)
        return lbl

    def _set(self, lbl: QLabel, name: str, value: str, color: str = None):
        c = color or COLORS["parchment_dim"]
        lbl.setText(f"{name}: {value}")
        lbl.setStyleSheet(f"color:{c}; font-size:11px;")

    def update_stats(
        self,
        cpu: float,
        ram_used: int,
        ram_total: int,
        active_macros: int,
        total_cps: int,
        api_online: bool,
    ):
        self._set(self.cpu_lbl, "CPU", f"{cpu:.0f}%")
        self._set(self.ram_lbl, "RAM", f"{ram_used} / {ram_total} Mo")
        self._set(
            self.load_lbl,
            "Load moteur",
            f"{active_macros} macro(s) · CPS {total_cps}",
        )
        if api_online:
            self._set(self.api_lbl, "API REST", "En ligne", COLORS["success"])
        else:
            self._set(self.api_lbl, "API REST", "Hors ligne", COLORS["warning"])
