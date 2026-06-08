from config_ui import CONFIG, PRESETS, RIGHT_CLICK_PRESETS, UIConfig

WINDOW_TITLE = CONFIG.window_title
WINDOW_SIZE = CONFIG.size

GLOBAL_STYLE = """
QMainWindow, QWidget {
    background-color: #0d0d0d;
    color: #e0e0e0;
    font-family: "Segoe UI", Consolas, sans-serif;
    font-size: 13px;
}
QTabWidget::pane {
    border: 1px solid #1a3a2a;
    border-radius: 8px;
    background: #111111;
    top: -1px;
}
QTabBar::tab {
    background: #151515;
    color: #888888;
    border: 1px solid #1a2a1a;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 10px 18px;
    margin-right: 4px;
    min-width: 90px;
}
QTabBar::tab:selected {
    background: #1a2a1a;
    color: #00ff88;
    border-bottom: 2px solid #00ff88;
}
QTabBar::tab:hover {
    color: #00ff88;
    background: #1a2520;
}
QGroupBox {
    border: 1px solid #1a3a2a;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: bold;
    color: #00ff88;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}
QSlider::groove:horizontal {
    height: 6px;
    background: #222222;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #00ff88;
    width: 16px;
    margin: -6px 0;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background: #33ffaa;
}
QPushButton {
    background: #151515;
    border: 1px solid #00ff88;
    border-radius: 6px;
    padding: 8px 16px;
    color: #00ff88;
    font-weight: bold;
}
QPushButton:hover {
    background: #00ff88;
    color: #0d0d0d;
}
QPushButton:pressed {
    background: #00cc6a;
}
QPushButton:checked {
    background: #00ff88;
    color: #0d0d0d;
}
QComboBox {
    background: #151515;
    border: 1px solid #1a3a2a;
    border-radius: 6px;
    padding: 6px 12px;
    color: #e0e0e0;
}
QComboBox:hover {
    border-color: #00ff88;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox QAbstractItemView {
    background: #151515;
    border: 1px solid #1a3a2a;
    selection-background-color: #00ff88;
    selection-color: #0d0d0d;
}
QLabel.card {
    background: #151515;
    border: 1px solid #1a3a2a;
    border-radius: 8px;
    padding: 16px;
}
QLabel.status-on {
    color: #00ff88;
    font-size: 28px;
    font-weight: bold;
}
QLabel.status-off {
    color: #ff3366;
    font-size: 28px;
    font-weight: bold;
}
QLabel.hint {
    color: #666666;
    font-size: 11px;
    font-style: italic;
}
QScrollArea {
    border: none;
    background: transparent;
}
"""

CARD_STYLE = "background:#151515;border:1px solid #1a3a2a;border-radius:8px;padding:12px;"
