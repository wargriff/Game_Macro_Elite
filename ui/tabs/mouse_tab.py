from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from config_ui import PRESETS
from ui.widgets.macro_panel import MacroPanel
from ui.widgets.status_card import StatusCard


class MouseTab(QWidget):
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Macro Clic Gauche")
        title.setStyleSheet("font-size:18px;font-weight:bold;color:#00ff88;")
        layout.addWidget(title)

        hint = QLabel(
            "Relâchez le bouton gauche de la souris pour activer/désactiver la macro."
        )
        hint.setProperty("class", "hint")
        hint.setStyleSheet("color:#666;font-style:italic;")
        layout.addWidget(hint)

        self.status = StatusCard("Clic Gauche")
        self.status.set_active(self.engine.is_active("left"))
        layout.addWidget(self.status)

        presets = {k: (c, int(d * 1000)) for k, (c, d) in PRESETS.items()}
        self.panel = MacroPanel(self.engine, "left", presets=presets)
        layout.addWidget(self.panel)
        layout.addStretch()

    def refresh(self):
        self.status.set_active(self.engine.is_active("left"))
        self.panel.update_live_cps()
