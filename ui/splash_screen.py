"""Single-load splash screen — replaces multi-launcher Control Center."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

from ui.styles.diablo_theme import COLORS, GLOBAL_STYLE


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XMacro Game — Control Center")
        self.setFixedSize(520, 340)
        self.setStyleSheet(
            GLOBAL_STYLE
            + f"""
            SplashScreen {{
                background-color: {COLORS['bg_dark']};
            }}
            """
        )
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(12)

        header = QVBoxLayout()
        header.setSpacing(4)

        title_row = QVBoxLayout()
        brand = QLabel("XMACRO GAME")
        brand.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        brand.setStyleSheet(f"color:{COLORS['gold_bright']}; letter-spacing:3px;")

        subtitle = QLabel("Game XClicker Elite · Control Center")
        subtitle.setStyleSheet(f"color:{COLORS['parchment_dim']}; font-size:12px;")

        version = QLabel("v2.1 · iCUE")
        version.setAlignment(Qt.AlignmentFlag.AlignRight)
        version.setStyleSheet(
            f"color:{COLORS['gold']}; font-size:11px; border:1px solid {COLORS['border_gold']};"
            f"border-radius:10px; padding:2px 10px;"
        )

        title_row.addWidget(brand)
        title_row.addWidget(subtitle)
        header.addLayout(title_row)
        layout.addLayout(header)

        status_bar = QLabel("⚡ Lanceur unifié — chargement interface iCUE")
        status_bar.setStyleSheet(
            f"background:rgba(30,60,30,0.5); color:{COLORS['success']};"
            f"padding:8px 12px; border-radius:4px; font-size:11px;"
        )
        layout.addWidget(status_bar)

        hint = QLabel(
            "Un seul démarrage : moteur · profils · API · interface Sanctuary"
        )
        hint.setWordWrap(True)
        hint.setStyleSheet(f"color:{COLORS['parchment_dim']}; font-size:12px; padding:4px 0;")
        layout.addWidget(hint)

        layout.addSpacing(8)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setFixedHeight(22)
        self.progress.setStyleSheet(
            f"""
            QProgressBar {{
                background: {COLORS['bg_panel']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                text-align: center;
                color: {COLORS['parchment']};
                font-size: 11px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {COLORS['gold_dim']}, stop:1 {COLORS['gold_bright']});
                border-radius: 3px;
            }}
            """
        )
        layout.addWidget(self.progress)

        self.status_lbl = QLabel("Prêt — lancement via OUVRE_MOI")
        self.status_lbl.setStyleSheet(f"color:{COLORS['parchment_dim']}; font-size:11px;")
        layout.addWidget(self.status_lbl)

        footer = QLabel("OUVRE_MOI.pyw · un seul lanceur · Sanctuary Edition")
        footer.setStyleSheet(f"color:{COLORS['gold_dim']}; font-size:10px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addStretch()
        layout.addWidget(footer)

    def set_progress(self, percent: int, message: str):
        self.progress.setValue(percent)
        self.status_lbl.setText(message)
