import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.widgets.status_card import StatusCard


class DashboardTab(QWidget):
    def __init__(self, engine, image_path: str, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.image_path = image_path
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        left = QVBoxLayout()
        self.global_card = StatusCard("GLOBAL")
        self.global_card.set_global(self.engine.enabled)

        self.summary = QLabel()
        self.summary.setWordWrap(True)
        self.summary.setStyleSheet(
            "background:#151515;border:1px solid #1a3a2a;border-radius:8px;"
            "padding:16px;color:#aaaaaa;"
        )
        self.summary.setMinimumHeight(120)

        toggle_btn = QPushButton("TOGGLE GLOBAL")
        toggle_btn.setFixedHeight(48)
        toggle_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        toggle_btn.clicked.connect(self.engine.toggle)

        left.addWidget(self.global_card)
        left.addWidget(self.summary)
        left.addWidget(toggle_btn)
        left.addStretch()

        center = QVBoxLayout()
        self.img = QLabel()
        self.img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._load_image()
        center.addWidget(self.img)
        center.addStretch()

        right = QGridLayout()
        self.macro_cards = {}
        keys = [
            ("left", "Clic Gauche"),
            ("right", "Clic Droit"),
            ("1", "Touche 1"),
            ("2", "Touche 2"),
        ]
        for i, (key, label) in enumerate(keys):
            card = StatusCard(label)
            card.set_active(self.engine.is_active(key), f"CPS: {self.engine.get_cps(key)}")
            self.macro_cards[key] = card
            right.addWidget(card, i // 2, i % 2)

        layout.addLayout(left, 2)
        layout.addLayout(center, 2)
        layout.addLayout(right, 2)

    def _load_image(self):
        if os.path.exists(self.image_path):
            pix = QPixmap(self.image_path)
            self.img.setPixmap(
                pix.scaled(280, 360, Qt.AspectRatioMode.KeepAspectRatio,
                           Qt.TransformationMode.SmoothTransformation)
            )
        else:
            self.img.setText("XMacro Elite")
            self.img.setStyleSheet("font-size:24px;color:#00ff88;")

    def refresh(self):
        self.global_card.set_global(self.engine.enabled)
        active = []
        for key, card in self.macro_cards.items():
            is_on = self.engine.is_active(key)
            cps = self.engine.get_real_cps(key)
            card.set_active(is_on, f"CPS réel: {cps}")
            if is_on:
                active.append(key)
        if active:
            self.summary.setText("Macros actives: " + ", ".join(active))
        else:
            self.summary.setText("Aucune macro active.\nClic droit une fois pour activer le spam.")
