import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QFrame


class BackgroundWidget(QFrame):
    """Central container with Diablo-themed background image."""

    def __init__(self, bg_path: str, parent=None):
        super().__init__(parent)
        self.setObjectName("BackgroundWidget")
        self._bg = QPixmap()
        if os.path.exists(bg_path):
            self._bg = QPixmap(bg_path)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.black)
        if not self._bg.isNull() and self.width() > 0 and self.height() > 0:
            scaled = self._bg.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.setOpacity(0.35)
            painter.drawPixmap(x, y, scaled)
        painter.end()
