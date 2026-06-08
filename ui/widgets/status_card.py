from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.styles import CARD_STYLE


class StatusCard(QWidget):
    def __init__(self, title: str = "STATUS", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        self.title = QLabel(title)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color:#00ff88;font-weight:bold;font-size:12px;")

        self.status = QLabel("OFF")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))

        self.detail = QLabel("")
        self.detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detail.setStyleSheet("color:#888888;font-size:12px;")

        layout.addWidget(self.title)
        layout.addWidget(self.status)
        layout.addWidget(self.detail)
        self.setStyleSheet(CARD_STYLE)

    def set_global(self, enabled: bool):
        if enabled:
            self.status.setText("ON")
            self.status.setStyleSheet("color:#00ff88;")
        else:
            self.status.setText("OFF")
            self.status.setStyleSheet("color:#ff3366;")

    def set_active(self, active: bool, label: str = ""):
        if active:
            self.status.setText("ACTIF")
            self.status.setStyleSheet("color:#00ff88;")
        else:
            self.status.setText("INACTIF")
            self.status.setStyleSheet("color:#ff3366;")
        if label:
            self.detail.setText(label)

    def set_detail(self, text: str):
        self.detail.setText(text)
