from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QButtonGroup, QHBoxLayout, QLabel, QPushButton, QWidget

from ui.styles.diablo_theme import COLORS, HEADER_STYLE
from utils.debug import log


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
        self._tab_ids = {}
        self._updating = False
        self._build()
        self.setStyleSheet(HEADER_STYLE)

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(4)

        self._group = QButtonGroup(self)
        self._group.setExclusive(True)

        for idx, (label, key) in enumerate(self.TABS):
            btn = QPushButton(label)
            btn.setObjectName("tab")
            btn.setCheckable(True)
            self._group.addButton(btn, idx)
            self._tab_buttons[key] = btn
            self._tab_ids[idx] = key
            layout.addWidget(btn)

        self._group.idClicked.connect(self._on_tab_id_clicked)

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

        self._select_tab("home", emit=False)

    def _on_tab_id_clicked(self, btn_id: int):
        key = self._tab_ids.get(btn_id)
        log("HEADER", f"idClicked id={btn_id} key={key}")
        if self._updating or not key:
            log("HEADER", "idClicked ignoré (_updating ou key absente)")
            return
        self.tab_changed.emit(key)

    def _select_tab(self, key: str, emit: bool = True):
        if key not in self._tab_buttons:
            log("HEADER", f"_select_tab key={key} INCONNUE")
            return

        log("HEADER", f"_select_tab key={key} emit={emit}")
        self._updating = True
        try:
            self._group.blockSignals(True)
            self._tab_buttons[key].setChecked(True)
            self._group.blockSignals(False)
        finally:
            self._updating = False

        if emit:
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
