from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ui.styles.diablo_theme import COLORS


class DeviceTile(QWidget):
    clicked = pyqtSignal()

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        icon: str = "",
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("DeviceTile")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(110)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        header = QHBoxLayout()
        self.title_lbl = QLabel(title.upper())
        self.title_lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet(f"color:{COLORS['gold']}; letter-spacing:1px;")

        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet(f"color:{COLORS['parchment_dim']}; font-size:10px;")
        header.addWidget(self.title_lbl)
        header.addStretch()
        header.addWidget(self.status_dot)
        layout.addLayout(header)

        body = QHBoxLayout()
        if icon:
            self.icon_lbl = QLabel(icon)
            self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.icon_lbl.setStyleSheet(f"font-size:28px; color:{COLORS['gold_dim']};")
            body.addWidget(self.icon_lbl)

        self.subtitle_lbl = QLabel(subtitle)
        self.subtitle_lbl.setWordWrap(True)
        self.subtitle_lbl.setStyleSheet(f"color:{COLORS['parchment_dim']}; font-size:12px;")
        body.addWidget(self.subtitle_lbl, 1)
        layout.addLayout(body)

        self.setStyleSheet(
            f"DeviceTile {{ background:rgba(20,16,12,0.9); border:1px solid {COLORS['border']};"
            f"border-radius:6px; }}"
            f"DeviceTile:hover {{ border-color:{COLORS['border_gold']}; }}"
        )

    def set_online(self, online: bool, detail: str = ""):
        color = COLORS["success"] if online else COLORS["parchment_dim"]
        self.status_dot.setStyleSheet(f"color:{color}; font-size:10px;")
        if detail:
            self.subtitle_lbl.setText(detail)

    def set_active(self, active: bool, detail: str = ""):
        color = COLORS["gold_bright"] if active else COLORS["parchment_dim"]
        self.status_dot.setStyleSheet(f"color:{color}; font-size:10px;")
        if detail:
            self.subtitle_lbl.setText(detail)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)
