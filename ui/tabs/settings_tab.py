from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.profile_manager import ProfileManager


class SettingsTab(QWidget):
    def __init__(
        self,
        engine,
        profile_manager: ProfileManager,
        on_profile_loaded=None,
        on_profile_saved=None,
        parent=None,
    ):
        super().__init__(parent)
        self.engine = engine
        self.profiles = profile_manager
        self.on_profile_loaded = on_profile_loaded
        self.on_profile_saved = on_profile_saved
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        title = QLabel("Paramètres")
        title.setStyleSheet("font-size:18px;font-weight:bold;color:#00ff88;")
        layout.addWidget(title)

        self.game_safe = QCheckBox("Mode Game Safe (CPS limité + micro-jitter)")
        self.game_safe.toggled.connect(self.engine.set_game_safe)
        layout.addWidget(self.game_safe)

        profile_box = QWidget()
        profile_box.setStyleSheet(
            "background:#151515;border:1px solid #1a3a2a;border-radius:8px;padding:16px;"
        )
        profile_layout = QVBoxLayout(profile_box)

        profile_lbl = QLabel("Profils")
        profile_lbl.setStyleSheet("color:#00ffaa;font-weight:bold;")
        profile_layout.addWidget(profile_lbl)

        row = QHBoxLayout()
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(self.profiles.list_profiles())
        self.profile_combo.setCurrentText(self.profiles.current_name)
        row.addWidget(self.profile_combo)

        load_btn = QPushButton("Charger")
        load_btn.clicked.connect(self._load_profile)
        save_btn = QPushButton("Sauvegarder")
        save_btn.clicked.connect(self._save_profile)
        row.addWidget(load_btn)
        row.addWidget(save_btn)
        profile_layout.addLayout(row)

        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet("color:#888;")
        profile_layout.addWidget(self.status_lbl)
        layout.addWidget(profile_box)

        hotkeys = QLabel(
            "Raccourcis:\n"
            "• Clic gauche/droit relâché → toggle macro correspondante\n"
            "• XButton1 → toggle macros clavier\n"
            "• XButton2 → toggle global ON/OFF"
        )
        hotkeys.setStyleSheet(
            "background:#151515;border:1px solid #1a3a2a;border-radius:8px;"
            "padding:16px;color:#aaaaaa;"
        )
        layout.addWidget(hotkeys)
        layout.addStretch()

    def _load_profile(self):
        name = self.profile_combo.currentText()
        self.profiles.load(name)
        self.profiles.apply_to_engine(self.engine.manager)
        self.status_lbl.setText(f"Profil '{name}' chargé.")
        if self.on_profile_loaded:
            self.on_profile_loaded()

    def _save_profile(self):
        name = self.profile_combo.currentText()
        self.profiles.capture_from_engine(self.engine.manager)
        if self.on_profile_saved:
            self.on_profile_saved()
        self.profiles.save(name)
        self.status_lbl.setText(f"Profil '{name}' sauvegardé.")
