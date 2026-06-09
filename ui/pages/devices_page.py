from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QWidget

from ui.tabs.rgb_tab import RGBTab
from ui.widgets.device_tile import DeviceTile


class DevicesPage(QWidget):
    def __init__(self, engine, rgb, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.rgb = rgb
        self._tiles = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        grid = QGridLayout()
        grid.setSpacing(10)
        devices = [
            ("mouse", "SOURIS", "Macro clic gauche/droit", "🖱"),
            ("keyboard", "CLAVIER", "Touches 1-4", "⌨"),
            ("side1", "LATÉRAL 1", "Toggle clavier", "◀"),
            ("side2", "LATÉRAL 2", "Pause globale", "▶"),
        ]
        for i, (key, title, sub, icon) in enumerate(devices):
            tile = DeviceTile(title, sub, icon)
            self._tiles[key] = tile
            grid.addWidget(tile, i // 2, i % 2)

        layout.addLayout(grid)
        self.rgb_section = RGBTab(self.rgb)
        layout.addWidget(self.rgb_section)
        layout.addStretch()

    def refresh(self):
        self._tiles["mouse"].set_online(True, "Win32 OK")
        self._tiles["keyboard"].set_online(True, "4 touches")
        self._tiles["side1"].set_active(
            any(self.engine.is_active(k) for k in ("1", "2", "3", "4")),
            "XButton1",
        )
        self._tiles["side2"].set_active(self.engine.enabled, "XButton2 — toggle global")
        self.rgb_section.refresh()
