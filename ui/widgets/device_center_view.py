from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QColor, QPen
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.styles.icue_theme import ICUE, ICUE_DEVICE_VIEW


class DeviceCenterView(QWidget):
    """Vue centrale Commander Pro style iCUE — repaint uniquement si device change."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DeviceCenterView")
        self._device_key = "commander"
        self._device_name = "COMMANDER CORE XT"
        self._build()
        self.setStyleSheet(ICUE_DEVICE_VIEW)
        self.setMinimumHeight(260)

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 8, 24, 8)
        self.name_lbl = QLabel(self._device_name)
        self.name_lbl.setObjectName("deviceName")
        layout.addWidget(self.name_lbl)
        layout.addStretch()

    def set_device(self, key: str):
        if key == self._device_key:
            return
        self._device_key = key
        names = {
            "keyboard": "K70 RGB PRO",
            "mouse": "M65 RGB ELITE — Souris Elite",
            "headset": "HS80 RGB WIRELESS",
            "commander": "COMMANDER PRO",
            "lighting": "Lighting Node PRO",
        }
        self._device_name = names.get(key, "Périphérique")
        self.name_lbl.setText(self._device_name)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2 + 30

        # Boitier principal
        painter.setPen(QPen(QColor(ICUE["border"]), 2))
        painter.setBrush(QColor("#2a2a2a"))
        painter.drawRoundedRect(cx - 140, cy - 55, 280, 110, 6, 6)

        # Ports style iCUE: TEMP, USB, LED
        port_labels = ("TEMP", "USB", "LED", "FAN")
        painter.setFont(QFont("Segoe UI", 8))
        for i, label in enumerate(port_labels):
            x = cx - 105 + i * 70
            painter.setPen(QPen(QColor(ICUE["yellow"]), 2))
            painter.setBrush(QColor("#1a1a1a"))
            painter.drawRoundedRect(x, cy - 22, 50, 44, 4, 4)
            painter.setPen(QColor(ICUE["text_dim"]))
            painter.drawText(x, cy - 8, 50, 20, Qt.AlignmentFlag.AlignCenter, label)
            painter.setPen(QColor(ICUE["text"]))
            painter.drawText(x, cy + 10, 50, 20, Qt.AlignmentFlag.AlignCenter, "●")

        painter.end()
