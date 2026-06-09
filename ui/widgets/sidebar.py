from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QComboBox, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.styles.diablo_theme import COLORS, SIDEBAR_STYLE


class Sidebar(QWidget):
    section_changed = pyqtSignal(str)

    SECTIONS = [
        ("PERFORMANCE", "performance"),
        ("GRAPHING", "graphing"),
        ("LIGHTING SETUP", "lighting"),
        ("LIGHTING CHANNEL 1", "channel1"),
        ("LIGHTING CHANNEL 2", "channel2"),
        ("MACRO 1", "macro1"),
        ("MACRO 2", "macro2"),
    ]

    def __init__(self, profiles: list, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(200)
        self._buttons = {}
        self._build(profiles)
        self.setStyleSheet(SIDEBAR_STYLE)

    def _build(self, profiles: list):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(4)

        logo = QLabel("★")
        logo.setFont(QFont("Segoe UI", 22))
        logo.setStyleSheet(f"color:{COLORS['gold_bright']};")
        brand = QLabel("XCLICKER ELITE\nSANCTUARY EDITION")
        brand.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        brand.setStyleSheet(
            f"color:{COLORS['gold']}; letter-spacing:1px; line-height:140%;"
        )
        layout.addWidget(logo)
        layout.addWidget(brand)
        layout.addSpacing(12)

        prof_lbl = QLabel("PROFILES")
        prof_lbl.setStyleSheet(
            f"color:{COLORS['parchment_dim']}; font-size:10px; letter-spacing:1px;"
        )
        layout.addWidget(prof_lbl)

        self.profile_combo = QComboBox()
        self.profile_combo.addItems(profiles)
        layout.addWidget(self.profile_combo)
        layout.addSpacing(16)

        for label, key in self.SECTIONS:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setProperty("section", key)
            btn.setStyleSheet(self._nav_style(False))
            btn.clicked.connect(lambda checked, k=key, b=btn: self._select(k, b))
            self._buttons[key] = btn
            layout.addWidget(btn)

        layout.addStretch()
        self._select("lighting", self._buttons["lighting"])

    def _nav_style(self, active: bool) -> str:
        if active:
            return (
                f"QPushButton {{ text-align:left; padding:8px 10px; border:none;"
                f"border-left:3px solid {COLORS['gold']};"
                f"background:rgba(60,45,20,0.35); color:{COLORS['gold_bright']};"
                f"font-weight:600; border-radius:0; }}"
            )
        return (
            f"QPushButton {{ text-align:left; padding:8px 10px; border:none;"
            f"border-left:3px solid transparent; background:transparent;"
            f"color:{COLORS['parchment_dim']}; border-radius:0; }}"
            f"QPushButton:hover {{ color:{COLORS['gold']};"
            f"background:rgba(30,24,16,0.4); }}"
        )

    def _select(self, key: str, btn: QPushButton):
        for k, b in self._buttons.items():
            b.setChecked(k == key)
            b.setStyleSheet(self._nav_style(k == key))
        self.section_changed.emit(key)

    def set_profiles(self, profiles: list):
        current = self.profile_combo.currentText()
        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        self.profile_combo.addItems(profiles)
        if current in profiles:
            self.profile_combo.setCurrentText(current)
        self.profile_combo.blockSignals(False)
