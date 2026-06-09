from collections import deque

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ui.styles.diablo_theme import COLORS
from ui.widgets.status_card import StatusCard


class DashboardPage(QWidget):
    HISTORY_LEN = 60

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._cps_history = deque(maxlen=self.HISTORY_LEN)
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        left = QVBoxLayout()
        self.global_card = StatusCard("GLOBAL")
        self.summary = QLabel()
        self.summary.setWordWrap(True)
        self.summary.setMinimumHeight(100)
        self.summary.setStyleSheet(
            f"background:rgba(18,16,14,0.9); border:1px solid {COLORS['border']};"
            f"border-radius:6px; padding:14px; color:{COLORS['parchment_dim']};"
        )
        left.addWidget(self.global_card)
        left.addWidget(self.summary)
        left.addStretch()
        layout.addLayout(left, 1)

        right = QVBoxLayout()
        graph_title = QLabel("GRAPHING — CPS temps réel")
        graph_title.setStyleSheet(
            f"color:{COLORS['gold']}; font-weight:bold; letter-spacing:1px;"
        )
        self.graph = QLabel()
        self.graph.setMinimumHeight(200)
        self.graph.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        self.graph.setStyleSheet(
            f"background:rgba(10,8,6,0.9); border:1px solid {COLORS['border']};"
            f"border-radius:6px; padding:8px;"
        )
        right.addWidget(graph_title)
        right.addWidget(self.graph)
        right.addStretch()
        layout.addLayout(right, 2)

    def refresh(self):
        enabled = self.engine.enabled
        self.global_card.set_global(enabled)

        keys = ["left", "right", "1", "2", "3", "4"]
        lines = []
        total_cps = 0
        for k in keys:
            real = self.engine.get_real_cps(k)
            total_cps += real
            if self.engine.is_active(k):
                lines.append(f"• {k}: ACTIF — CPS {real}")

        self.summary.setText(
            f"Moteur: {'ACTIF' if enabled else 'STASE'}\n"
            f"Macros actives: {self.engine.count_active_macros()}\n"
            f"CPS total: {total_cps}\n\n"
            + ("\n".join(lines) if lines else "Aucune macro active.")
        )

        self._cps_history.append(total_cps)
        self._draw_graph()

    def _draw_graph(self):
        if not self._cps_history:
            self.graph.setText("")
            return

        max_val = max(max(self._cps_history), 1)
        w = max(self.graph.width() - 16, 200)
        bar_w = max(w // len(self._cps_history), 2)
        bars = []
        for v in self._cps_history:
            h = int((v / max_val) * 12)
            bars.append("▁▂▃▄▅▆▇"[min(h, 7)] if v > 0 else "▁")
        self.graph.setText(" ".join(bars))
        self.graph.setStyleSheet(
            f"background:rgba(10,8,6,0.9); border:1px solid {COLORS['border']};"
            f"border-radius:6px; padding:8px; color:{COLORS['gold']};"
            f"font-family:Consolas; font-size:14px;"
        )
