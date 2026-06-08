from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from config_ui import RIGHT_CLICK_PRESETS
from ui.widgets.macro_panel import MacroPanel
from ui.widgets.status_card import StatusCard


class RightClickTab(QWidget):
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Macro Clic Droit")
        title.setStyleSheet("font-size:18px;font-weight:bold;color:#00ff88;")
        layout.addWidget(title)

        hint = QLabel(
            "Clic droit une fois pour activer — la macro spamme ensuite automatiquement "
            "des clics droits au CPS configuré. Re-cliquez pour désactiver."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color:#888;font-style:italic;padding:8px;")
        layout.addWidget(hint)

        self.status = StatusCard("Clic Droit")
        self.status.set_active(
            self.engine.is_active("right"),
            f"CPS cible: {self.engine.get_cps('right')}",
        )
        layout.addWidget(self.status)

        self.panel = MacroPanel(
            self.engine,
            "right",
            presets=RIGHT_CLICK_PRESETS,
            show_burst=True,
        )
        layout.addWidget(self.panel)
        layout.addStretch()

    def refresh(self):
        active = self.engine.is_active("right")
        real_cps = self.engine.get_real_cps("right")
        self.status.set_active(
            active,
            f"CPS réel: {real_cps} | Cible: {self.engine.get_cps('right')}",
        )
        self.panel.update_live_cps()
