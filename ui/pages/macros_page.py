from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from ui.tabs.keyboard_tab import KeyboardTab
from ui.tabs.mouse_tab import MouseTab
from ui.tabs.right_click_tab import RightClickTab


class MacrosPage(QWidget):
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        self.tabs = QTabWidget()
        self.mouse_tab = MouseTab(engine)
        self.right_tab = RightClickTab(engine)
        self.keyboard_tab = KeyboardTab(engine)

        self.tabs.addTab(self.mouse_tab, "Macro 1 — Clic Gauche")
        self.tabs.addTab(self.right_tab, "Macro 2 — Clic Droit")
        self.tabs.addTab(self.keyboard_tab, "Clavier")
        layout.addWidget(self.tabs)

    def refresh(self):
        self.mouse_tab.refresh()
        self.right_tab.refresh()
        self.keyboard_tab.refresh()
        self.mouse_tab.panel.sync_from_engine()
        self.right_tab.panel.sync_from_engine()
        self.keyboard_tab.panel.sync_from_engine()

    def focus_section(self, section: str):
        mapping = {"macro1": 0, "macro2": 1, "channel1": 0, "channel2": 1}
        idx = mapping.get(section, 0)
        self.tabs.setCurrentIndex(idx)
