import os

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSlider, QPushButton, QComboBox
)

from core.debug_log import log


class UI(QWidget):
    def __init__(self, engine, image, rgb=None):
        super().__init__()

        self.engine = engine
        self.rgb = rgb

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = image if os.path.isabs(image) else os.path.join(base_dir, image)

        self.setWindowTitle("XMacro Elite PRO")
        self.resize(1100, 650)

        self.setStyleSheet("""
            QWidget{background:#0a0a0a;color:#00ff88;font-family:Consolas;}
            QSlider::groove:horizontal{height:6px;background:#222;border-radius:3px;}
            QSlider::handle:horizontal{background:#00ff88;width:14px;margin:-5px 0;border-radius:7px;}
            QPushButton{background:#111;border:1px solid #00ff88;padding:6px;}
            QPushButton:hover{background:#00ff88;color:black;}
        """)

        main = QHBoxLayout()

        left = QVBoxLayout()
        left.addWidget(self._title("RGB"))

        self.rgb_labels = []
        self.rgb_zone_names = ["left", "right", "wheel", "dpi", "side1", "side2"]
        for name in self.rgb_zone_names:
            lbl = QLabel("■")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(QFont("Consolas", 14))
            lbl.setObjectName(name)
            self.rgb_labels.append(lbl)
            left.addWidget(lbl)

        center = QVBoxLayout()

        self.status = QLabel("OFF")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setFont(QFont("Consolas", 26, QFont.Weight.Bold))
        center.addWidget(self.status)

        self.img = QLabel()
        self.img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._load_image()
        center.addWidget(self.img)

        toggle_btn = QPushButton("TOGGLE")
        toggle_btn.clicked.connect(self._on_toggle)
        toggle_btn.setFixedHeight(40)
        center.addWidget(toggle_btn)

        right = QVBoxLayout()
        right.addWidget(self._title("CONTROLS"))

        self.selector = QComboBox()
        self.selector.addItems(["left", "right", "1", "2", "3", "4"])
        right.addWidget(self.selector)

        right.addWidget(self._control())
        right.addStretch()

        main.addLayout(left, 1)
        main.addLayout(center, 2)
        main.addLayout(right, 2)

        self.setLayout(main)

        self.selector.currentTextChanged.connect(self._sync_sliders)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(200)

        self._sync_sliders()
        log("UI", "interface ready")

    def _on_toggle(self):
        log("UI", "TOGGLE button clicked")
        self.engine.toggle()

    def _title(self, text):
        w = QWidget()
        l = QVBoxLayout(w)

        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size:14px;color:#00ffaa;font-weight:bold;")

        line = QLabel()
        line.setFixedHeight(2)
        line.setStyleSheet("background:#00ff88;")

        l.addWidget(lbl)
        l.addWidget(line)
        return w

    def _control(self):
        container = QWidget()
        box = QVBoxLayout(container)

        title = QLabel("GLOBAL")
        title.setStyleSheet("color:#00ffaa;font-weight:bold;")

        self.cps_label = QLabel()
        self.cps_slider = QSlider(Qt.Orientation.Horizontal)
        self.cps_slider.setRange(1, 200)

        self.delay_label = QLabel()
        self.delay_slider = QSlider(Qt.Orientation.Horizontal)
        self.delay_slider.setRange(1, 1000)

        self.micro_label = QLabel("fine 0 µs")
        self.micro_slider = QSlider(Qt.Orientation.Horizontal)
        self.micro_slider.setRange(0, 1000)

        self.slow_btn = QPushButton("ULTRA SLOW")
        self.slow_btn.setCheckable(True)

        def update_all():
            key = self.selector.currentText()
            cps = self.cps_slider.value()
            delay = self.delay_slider.value() / 1000
            micro = self.micro_slider.value() / 1_000_000

            if self.slow_btn.isChecked():
                cps = max(1, cps // 10)

            log("UI", f"slider change {key}", cps=cps, delay_ms=int(delay * 1000))
            self.engine.set_cps(key, cps)
            self.engine.set_delay(key, delay + micro)

            self.cps_label.setText(f"CPS {cps}")
            self.delay_label.setText(f"{int(delay * 1000)} ms")
            self.micro_label.setText(f"fine {self.micro_slider.value()} µs")

        self.cps_slider.valueChanged.connect(update_all)
        self.delay_slider.valueChanged.connect(update_all)
        self.micro_slider.valueChanged.connect(update_all)
        self.slow_btn.toggled.connect(update_all)

        presets = QHBoxLayout()
        PRESETS = {
            "SAFE": (4, 150),
            "SLOW": (2, 300),
            "ULTRA": (1, 600),
            "FAST": (20, 10),
        }

        for name, (c, d) in PRESETS.items():
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, c=c, d=d, n=name: self._apply_preset(c, d, n))
            presets.addWidget(btn)

        self.live = QLabel("REAL CPS: 0")

        box.addWidget(title)

        row1 = QHBoxLayout()
        row1.addWidget(self.cps_label)
        row1.addWidget(self.cps_slider)

        row2 = QHBoxLayout()
        row2.addWidget(self.delay_label)
        row2.addWidget(self.delay_slider)

        row3 = QHBoxLayout()
        row3.addWidget(self.micro_label)
        row3.addWidget(self.micro_slider)

        box.addLayout(row1)
        box.addLayout(row2)
        box.addLayout(row3)
        box.addWidget(self.slow_btn)
        box.addLayout(presets)
        box.addWidget(self.live)

        return container

    def _sync_sliders(self):
        key = self.selector.currentText()
        btn = self.engine.buttons.get(key)

        if not btn:
            log("UI", f"sync skipped — unknown key {key}")
            return

        log("UI", f"sync sliders for {key}", cps=btn.cps, delay=btn.delay)
        self.cps_slider.blockSignals(True)
        self.delay_slider.blockSignals(True)

        self.cps_slider.setValue(btn.cps)
        self.delay_slider.setValue(int(btn.delay * 1000))

        self.cps_label.setText(f"CPS {btn.cps}")
        self.delay_label.setText(f"{int(btn.delay * 1000)} ms")

        self.cps_slider.blockSignals(False)
        self.delay_slider.blockSignals(False)

    def _apply_preset(self, c, d, name):
        log("UI", f"preset {name}", cps=c, delay_ms=d)
        self.cps_slider.setValue(c)
        self.delay_slider.setValue(d)

    def _load_image(self):
        if os.path.exists(self.image_path):
            pix = QPixmap(self.image_path)
            self.img.setPixmap(
                pix.scaled(320, 420, Qt.AspectRatioMode.KeepAspectRatio)
            )
        else:
            self.img.setText("NO IMAGE")

    def closeEvent(self, event):
        log("UI", "window closing — stopping engine")
        self.engine.stop()
        event.accept()

    def update_ui(self):
        enabled = self.engine.enabled

        self.status.setText("ON" if enabled else "OFF")
        self.status.setStyleSheet(
            "color:#00ff88;" if enabled else "color:#ff2222;"
        )

        key = self.selector.currentText()
        cps = self.engine.get_real_cps(key)
        self.live.setText(f"REAL CPS: {cps}")

        if self.rgb:
            self.rgb.update()
            for lbl, zone in zip(self.rgb_labels, self.rgb_zone_names):
                color = self.rgb.get_color(zone)
                lbl.setStyleSheet(f"color: rgb({color.red()},{color.green()},{color.blue()});")
