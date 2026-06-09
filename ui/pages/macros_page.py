from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.styles.diablo_theme import COLORS
from ui.tabs.keyboard_tab import KeyboardTab
from ui.tabs.mouse_tab import MouseTab
from ui.tabs.right_click_tab import RightClickTab


MACRO_SLOTS = [
    ("left", "Macro 1 — Clic gauche"),
    ("right", "Macro 2 — Clic droit"),
    ("keyboard", "Clavier — touches 1-4"),
]


class MacrosPage(QWidget):
    """Macros page with master_combo / name_edit for Sanctuary compatibility."""

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._updating = False
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("MACROS")
        title.setStyleSheet(
            f"color:{COLORS['gold_bright']}; font-size:16px; font-weight:bold;"
            f"letter-spacing:2px;"
        )
        layout.addWidget(title)

        top = QHBoxLayout()
        top.setSpacing(12)

        name_lbl = QLabel("Nom:")
        name_lbl.setStyleSheet(f"color:{COLORS['parchment_dim']};")
        self.name_edit = QLineEdit("default")
        self.name_edit.setReadOnly(True)
        self.name_edit.setPlaceholderText("Nom du profil macro")
        self.name_edit.setStyleSheet(
            f"background:rgba(18,16,14,0.95); border:1px solid {COLORS['border']};"
            f"padding:6px; color:{COLORS['parchment']};"
        )

        master_lbl = QLabel("Canal:")
        master_lbl.setStyleSheet(f"color:{COLORS['parchment_dim']};")
        self.master_combo = QComboBox()
        for _, label in MACRO_SLOTS:
            self.master_combo.addItem(label)
        self.master_combo.setStyleSheet(
            f"background:rgba(18,16,14,0.95); border:1px solid {COLORS['border']};"
            f"padding:4px; color:{COLORS['parchment']}; min-width:220px;"
        )

        top.addWidget(name_lbl)
        top.addWidget(self.name_edit, 1)
        top.addWidget(master_lbl)
        top.addWidget(self.master_combo, 1)
        layout.addLayout(top)

        self.stack = QStackedWidget()
        self.mouse_tab = MouseTab(self.engine)
        self.right_tab = RightClickTab(self.engine)
        self.keyboard_tab = KeyboardTab(self.engine)
        self.stack.addWidget(self.mouse_tab)
        self.stack.addWidget(self.right_tab)
        self.stack.addWidget(self.keyboard_tab)
        layout.addWidget(self.stack, 1)

        self.master_combo.currentIndexChanged.connect(self._on_master_changed)

    def _on_master_changed(self, index: int):
        if self._updating:
            return
        self.stack.setCurrentIndex(index)

    def set_profile_name(self, name: str):
        self.name_edit.setText(name or "default")

    def focus_section(self, section: str):
        mapping = {
            "macro1": 0,
            "macro2": 1,
            "channel1": 0,
            "channel2": 1,
            "keyboard": 2,
        }
        idx = mapping.get(section, 0)
        self._updating = True
        try:
            self.master_combo.blockSignals(True)
            self.master_combo.setCurrentIndex(idx)
            self.master_combo.blockSignals(False)
            self.stack.setCurrentIndex(idx)
        finally:
            self._updating = False

    def refresh(self):
        try:
            self.mouse_tab.refresh()
            self.right_tab.refresh()
            self.keyboard_tab.refresh()
            self.mouse_tab.panel.sync_from_engine()
            self.right_tab.panel.sync_from_engine()
            self.keyboard_tab.panel.sync_from_engine()
        except Exception as exc:
            print(f"[MACROS] refresh skipped: {exc}")
