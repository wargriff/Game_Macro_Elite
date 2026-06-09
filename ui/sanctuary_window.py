"""Sanctuary Edition main window — iCUE-style layout with Diablo 4 theme."""

import os

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QStackedWidget, QVBoxLayout

from rgb_engine import RGBEngine
from services.profile_manager import ProfileManager
from services.sidecar_api import SidecarAPI
from ui.pages.dashboard_page import DashboardPage
from ui.pages.devices_page import DevicesPage
from ui.pages.home_page import HomePage
from ui.pages.macros_page import MacrosPage
from ui.pages.settings_page import SettingsPage
from ui.styles.diablo_theme import FOOTER_STYLE, GLOBAL_STYLE, WINDOW_SIZE, WINDOW_TITLE
from ui.widgets.background_widget import BackgroundWidget
from ui.widgets.header_bar import HeaderBar
from ui.widgets.sensor_panel import SensorPanel
from ui.widgets.sidebar import Sidebar

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG_PATH = os.path.join(BASE_DIR, "assets", "bg", "diablo_bg.svg")
ICON_PATH = os.path.join(BASE_DIR, "assets", "favicon", "favicon.svg")


class SanctuaryWindow(QMainWindow):
    PAGE_MAP = {
        "home": 0,
        "dashboard": 1,
        "devices": 2,
        "macros": 3,
        "settings": 4,
    }

    def __init__(self, engine, image_path: str = "assets/mouse.svg"):
        super().__init__()
        self.engine = engine
        self.rgb = RGBEngine()
        self.profiles = ProfileManager()
        self.profiles.load("default")
        self.profiles.apply_to_engine(engine.manager)
        self.profiles.apply_to_rgb(self.rgb)

        self.sidecar = SidecarAPI(engine)
        self.sidecar.start()

        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*WINDOW_SIZE)
        self.setStyleSheet(GLOBAL_STYLE)
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        bg = BackgroundWidget(BG_PATH)
        self.setCentralWidget(bg)

        root = QVBoxLayout(bg)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.header = HeaderBar()
        root.addWidget(self.header)

        body = QHBoxLayout()
        body.setSpacing(0)

        self.sidebar = Sidebar(self.profiles.list_profiles())
        body.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.sensor_panel = SensorPanel()
        self.home = HomePage(engine, self.rgb, self.sensor_panel)
        self.dashboard = DashboardPage(engine)
        self.devices = DevicesPage(engine, self.rgb)
        self.macros = MacrosPage(engine)
        self.settings = SettingsPage(
            engine,
            self.profiles,
            on_profile_loaded=self._on_profile_loaded,
            on_profile_saved=lambda: self.profiles.capture_from_rgb(self.rgb),
        )

        for page in (self.home, self.dashboard, self.devices, self.macros, self.settings):
            self.stack.addWidget(page)

        body.addWidget(self.stack, 1)
        root.addLayout(body, 1)

        self.footer = QLabel(
            "Latéral 2 = pause globale · En pause rien ne démarre · Journal en temps réel"
        )
        self.footer.setFixedHeight(28)
        self.footer.setStyleSheet(FOOTER_STYLE + " padding-left:12px;")
        root.addWidget(self.footer)

        self.header.tab_changed.connect(self._on_tab)
        self.header.seal_clicked.connect(self.close)
        self.header.stasis_clicked.connect(self.engine.toggle)
        self.sidebar.section_changed.connect(self._on_section)
        self.sidebar.profile_combo.currentTextChanged.connect(self._on_profile_change)
        self.sensor_panel.rescan_btn.clicked.connect(self._rescan_devices)

        engine.set_on_toggle(self._on_macro_toggle)

        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.refresh_all)
        self.ui_timer.start(250)

        self.rgb_timer = QTimer()
        self.rgb_timer.timeout.connect(self._update_rgb)
        self.rgb_timer.start(50)

    def _on_tab(self, tab: str):
        idx = self.PAGE_MAP.get(tab, 0)
        self.stack.setCurrentIndex(idx)

    def _on_section(self, section: str):
        if section in ("performance", "graphing"):
            self.stack.setCurrentIndex(self.PAGE_MAP["dashboard"])
            self.header._select_tab("dashboard")
        elif section in ("lighting", "channel1", "channel2"):
            self.stack.setCurrentIndex(self.PAGE_MAP["devices"])
            self.header._select_tab("devices")
        elif section in ("macro1", "macro2"):
            self.stack.setCurrentIndex(self.PAGE_MAP["macros"])
            self.header._select_tab("macros")
            self.macros.focus_section(section)

    def _on_profile_change(self, name: str):
        self.profiles.load(name)
        self.profiles.apply_to_engine(self.engine.manager)
        self.profiles.apply_to_rgb(self.rgb)
        self._on_profile_loaded()

    def _on_profile_loaded(self):
        self.profiles.apply_to_rgb(self.rgb)
        self.refresh_all()

    def _on_macro_toggle(self, key: str, active: bool):
        zone_map = {
            "left": "left", "right": "right",
            "1": "side1", "2": "side2", "3": "dpi", "4": "wheel",
        }
        zone = zone_map.get(key)
        if zone and active:
            self.rgb.trigger_reactive(zone)

    def _update_rgb(self):
        self.rgb.update()
        if self.stack.currentWidget() == self.devices:
            self.devices.refresh()

    def _rescan_devices(self):
        self.sidebar.set_profiles(self.profiles.list_profiles())

    def _get_system_stats(self):
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            return cpu, mem.used // (1024 * 1024), mem.total // (1024 * 1024)
        except ImportError:
            return 0.0, 0, 0

    def refresh_all(self):
        cpu, ram_used, ram_total = self._get_system_stats()
        total_cps = self.engine.get_total_cps()
        active = self.engine.count_active_macros()

        self.header.update_engine(self.engine.enabled)
        self.header.update_cps(total_cps)
        self.sensor_panel.update_stats(
            cpu, ram_used, ram_total, active, total_cps, self.sidecar.online
        )
        self.home.refresh(api_online=self.sidecar.online)
        self.dashboard.refresh()
        self.devices.refresh()
        self.macros.refresh()

    def closeEvent(self, event):
        self.engine.running = False
        self.sidecar.stop()
        event.accept()
