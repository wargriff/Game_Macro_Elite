from PyQt6.QtWidgets import QVBoxLayout, QWidget

from ui.tabs.settings_tab import SettingsTab


class SettingsPage(QWidget):
    def __init__(self, engine, profiles, on_profile_loaded=None, on_profile_saved=None, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.tab = SettingsTab(
            engine,
            profiles,
            on_profile_loaded=on_profile_loaded,
            on_profile_saved=on_profile_saved,
        )
        layout.addWidget(self.tab)
