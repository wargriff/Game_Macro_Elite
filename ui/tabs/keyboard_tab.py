from PyQt6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget

from config_ui import PRESETS
from ui.widgets.macro_panel import MacroPanel
from ui.widgets.status_card import StatusCard


class KeyboardTab(QWidget):
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Macro Clavier")
        title.setStyleSheet("font-size:18px;font-weight:bold;color:#00ff88;")
        layout.addWidget(title)

        hint = QLabel(
            "Bouton latéral souris (XButton1) pour activer/désactiver toutes les touches."
        )
        hint.setStyleSheet("color:#666;font-style:italic;")
        layout.addWidget(hint)

        sel_row = QVBoxLayout()
        sel_lbl = QLabel("Touche:")
        sel_lbl.setStyleSheet("color:#00ffaa;font-weight:bold;")
        self.selector = QComboBox()
        self.selector.addItems(["1", "2", "3", "4"])
        self.selector.currentTextChanged.connect(self._on_key_changed)
        sel_row.addWidget(sel_lbl)
        sel_row.addWidget(self.selector)
        layout.addLayout(sel_row)

        self.status = StatusCard("Touche")
        layout.addWidget(self.status)

        presets = {k: (c, int(d * 1000)) for k, (c, d) in PRESETS.items()}
        self.panel = MacroPanel(self.engine, "1", presets=presets)
        layout.addWidget(self.panel)
        layout.addStretch()
        self._current = "1"

    def _on_key_changed(self, key: str):
        self._current = key
        self.panel.key = key
        self.panel.sync_from_engine()
        self.status.title.setText(f"Touche {key}")
        self.refresh()

    def refresh(self):
        key = self.selector.currentText()
        self.status.set_active(self.engine.is_active(key))
        self.panel.key = key
        self.panel.update_live_cps()
