from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from ui.styles.diablo_theme import COLORS, HEADER_STYLE


class HeaderBar(QWidget):
    tab_changed = pyqtSignal(str)
    seal_clicked = pyqtSignal()
    stasis_clicked = pyqtSignal()

    TABS = [
        ("HOME", "home"),
        ("DASHBOARD", "dashboard"),
        ("DEVICES", "devices"),
        ("MACROS", "macros"),
        ("SETTINGS", "settings"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HeaderBar")
        self.setFixedHeight(52)
        self._tab_buttons = {}
        self._cps_lbl = None
        self._engine_lbl = None
        self._build()
        self.setStyleSheet(HEADER_STYLE)

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(4)

        for label, key in self.TABS:
            btn = QPushButton(label)
            btn.setObjectName("tab")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, k=key: self._select_tab(k))
            self._tab_buttons[key] = btn
            layout.addWidget(btn)

        layout.addStretch()

        self._engine_lbl = QLabel("MOTEUR — STASE")
        self._engine_lbl.setStyleSheet(
            f"color:{COLORS['parchment_dim']}; font-size:11px; padding:0 8px;"
        )
        layout.addWidget(self._engine_lbl)

        self._cps_lbl = QLabel("CPS Σ 0")
        self._cps_lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self._cps_lbl.setStyleSheet(f"color:{COLORS['gold']}; padding:0 12px;")
        layout.addWidget(self._cps_lbl)

        stasis = QPushButton("SCEAU DE STASE")
        stasis.setStyleSheet(
            f"border:1px solid {COLORS['blood']}; color:{COLORS['gold']};"
            f"padding:6px 12px; font-size:11px;"
        )
        stasis.clicked.connect(self.stasis_clicked.emit)
        layout.addWidget(stasis)

        seal = QPushButton("Sceller")
        seal.setObjectName("danger")
        seal.setFixedHeight(34)
        seal.clicked.connect(self.seal_clicked.emit)
        layout.addWidget(seal)

        self._select_tab("home")

    def _select_tab(self, key: str):
        for k, btn in self._tab_buttons.items():
            btn.setChecked(k == key)
        self.tab_changed.emit(key)

    def update_engine(self, enabled: bool):
        if enabled:
            self._engine_lbl.setText("MOTEUR — ACTIF")
            self._engine_lbl.setStyleSheet(
                f"color:{COLORS['success']}; font-size:11px; padding:0 8px;"
            )
        else:
            self._engine_lbl.setText("MOTEUR — STASE")
            self._engine_lbl.setStyleSheet(
                f"color:{COLORS['parchment_dim']}; font-size:11px; padding:0 8px;"
            )

    def update_cps(self, total: int):
        self._cps_lbl.setText(f"CPS Σ {total}")
