import random
import threading
import time
from typing import Callable, Dict, Optional

from core.debug_log import log, log_state
from core.models import Btn, Stats
from core.win32_input import (
    MOUSEEVENTF_LEFTDOWN,
    MOUSEEVENTF_LEFTUP,
    MOUSEEVENTF_RIGHTDOWN,
    MOUSEEVENTF_RIGHTUP,
    VK_LBUTTON,
    VK_RBUTTON,
    VK_XBUTTON1,
    VK_XBUTTON2,
    send_key,
    send_mouse,
    user32,
)

GAME_SAFE_MAX_CPS = 30
IGNORE_LEFT_MS = 0.05
IGNORE_RIGHT_MS = 0.08


class BaseEngine:
    def __init__(self, name: str):
        self.name = name
        self.enabled = True
        self.running = True
        self.game_safe = False
        self.buttons: Dict[str, Btn] = {}
        self.stats: Dict[str, Stats] = {}
        self._threads = []
        self._on_toggle: Optional[Callable[[str, bool], None]] = None
        self._loop_active: Dict[str, bool] = {}
        log("ENGINE", f"{name} initialized")

    def set_on_toggle(self, callback: Callable[[str, bool], None]):
        self._on_toggle = callback

    def get_cps(self, key):
        return self.buttons.get(key, Btn()).cps

    def set_cps(self, key, value):
        if key in self.buttons:
            max_cps = GAME_SAFE_MAX_CPS if self.game_safe else 200
            old = self.buttons[key].cps
            self.buttons[key].cps = max(1, min(max_cps, value))
            log_state("CPS", key, old, self.buttons[key].cps)

    def set_delay(self, key, value):
        if key in self.buttons:
            old = self.buttons[key].delay
            self.buttons[key].delay = max(0.0, value)
            log_state("DELAY", key, old, self.buttons[key].delay)

    def set_burst_count(self, key, value):
        if key in self.buttons:
            old = self.buttons[key].burst_count
            self.buttons[key].burst_count = max(0, value)
            log_state("BURST", key, old, self.buttons[key].burst_count)

    def get_burst_count(self, key):
        return self.buttons.get(key, Btn()).burst_count

    def get_real_cps(self, key):
        return self.stats.get(key, Stats()).cps

    def stop(self):
        log("ENGINE", f"{self.name} stopping")
        self.running = False

    def toggle_global(self):
        old = self.enabled
        self.enabled = not self.enabled
        log_state("GLOBAL", self.name, old, self.enabled)

    def _register(self, key):
        s = self.stats[key]
        now = time.perf_counter()
        with s.lock:
            s.timestamps.append(now)
            while s.timestamps and now - s.timestamps[0] > 1:
                s.timestamps.popleft()
            s.cps = len(s.timestamps)

    def _effective_interval(self, btn: Btn) -> float:
        cps = btn.cps
        if self.game_safe:
            cps = min(cps, GAME_SAFE_MAX_CPS)
        interval = max(1 / cps, btn.delay)
        if self.game_safe:
            interval += random.uniform(0, 0.008)
        return interval

    def _loop(self, key, action):
        log("WORKER", f"{self.name}/{key} thread started")
        tick = 0
        self._loop_active[key] = False

        while self.running:
            active = self.enabled and self.buttons[key].active
            if active != self._loop_active.get(key):
                self._loop_active[key] = active
                log("WORKER", f"{self.name}/{key} active={active}")

            if not active:
                time.sleep(0.01)
                continue

            interval = self._effective_interval(self.buttons[key])
            start = time.perf_counter()
            action(key)
            self._register(key)
            tick += 1

            if tick % 50 == 0:
                log("TICK", f"{self.name}/{key}", tick=tick, real_cps=self.stats[key].cps)

            sleep = interval - (time.perf_counter() - start)
            if sleep > 0:
                time.sleep(sleep)

        log("WORKER", f"{self.name}/{key} thread stopped")

    def _start_worker(self, key, action):
        t = threading.Thread(target=self._loop, args=(key, action), daemon=True)
        t.start()
        self._threads.append(t)

    def _notify_toggle(self, key: str, active: bool):
        log("TOGGLE", f"{self.name}/{key} -> {active}")
        if self._on_toggle:
            self._on_toggle(key, active)


class MouseEngine(BaseEngine):
    def __init__(self):
        super().__init__("MOUSE")
        self.buttons = {"left": Btn(), "right": Btn(cps=15, delay=0.019)}
        self.stats = {k: Stats() for k in self.buttons}
        self._last_state = {"left": False, "right": False}
        self._press_time = {"left": 0.0, "right": 0.0}
        self._ignore_until = {"left": 0.0, "right": 0.0}
        self._ignore_ms = {"left": IGNORE_LEFT_MS, "right": IGNORE_RIGHT_MS}
        self._start()
        self._listener()

    def _click(self, key):
        now = time.perf_counter()
        self._ignore_until[key] = now + self._ignore_ms[key]
        if key == "left":
            send_mouse(MOUSEEVENTF_LEFTDOWN)
            send_mouse(MOUSEEVENTF_LEFTUP)
        else:
            send_mouse(MOUSEEVENTF_RIGHTDOWN)
            send_mouse(MOUSEEVENTF_RIGHTUP)

    def _fire_burst(self, key: str):
        burst = self.buttons[key].burst_count
        if burst <= 0:
            return
        log("BURST", f"firing {burst} clicks on {key}")
        for i in range(burst):
            self._click(key)
            self._register(key)
            log("BURST", f"{key} click {i + 1}/{burst}")
            time.sleep(0.01)

    def _toggle_button(self, key: str):
        btn = self.buttons[key]
        old = btn.active
        btn.active = not btn.active
        log("MOUSE", f"toggle {key}", was=old, now=btn.active)
        if btn.active:
            self._fire_burst(key)
        self._notify_toggle(key, btn.active)

    def _start(self):
        for k in self.buttons:
            self._start_worker(k, self._click)

    def _listener(self):
        def loop():
            log("LISTENER", "MOUSE listener started")
            while self.running:
                now = time.perf_counter()
                l = bool(user32.GetAsyncKeyState(VK_LBUTTON) & 0x8000)
                r = bool(user32.GetAsyncKeyState(VK_RBUTTON) & 0x8000)

                for key, pressed in (("left", l), ("right", r)):
                    if now <= self._ignore_until[key]:
                        if pressed != self._last_state[key]:
                            log("IGNORE", f"{key} input ignored (fake click window)")
                        continue

                    if pressed and not self._last_state[key]:
                        self._press_time[key] = now
                        log("INPUT", f"{key} pressed")

                    if not pressed and self._last_state[key]:
                        hold = now - self._press_time[key]
                        log("INPUT", f"{key} released", hold_ms=round(hold * 1000, 1))
                        if hold > 0.02:
                            self._toggle_button(key)
                        else:
                            log("INPUT", f"{key} release too short — no toggle")

                self._last_state["left"] = l
                self._last_state["right"] = r
                time.sleep(0.005)

        threading.Thread(target=loop, daemon=True).start()


class KeyEngine(BaseEngine):
    def __init__(self):
        super().__init__("KEYBOARD")
        self.buttons = {"1": Btn(), "2": Btn(), "3": Btn(), "4": Btn()}
        self.stats = {k: Stats() for k in self.buttons}
        self.vk = {"1": 0x31, "2": 0x32, "3": 0x33, "4": 0x34}
        self._start()
        self._listener()

    def _press(self, key):
        vk = self.vk[key]
        send_key(vk, True)
        send_key(vk, False)

    def _start(self):
        for k in self.buttons:
            self._start_worker(k, self._press)

    def _listener(self):
        def loop():
            log("LISTENER", "KEYBOARD listener started (XBUTTON1)")
            last = False
            while self.running:
                p = user32.GetAsyncKeyState(VK_XBUTTON1) & 0x8000 != 0
                if p and not last:
                    active = not any(b.active for b in self.buttons.values())
                    log("KEYBOARD", f"XBUTTON1 -> all keys active={active}")
                    for k, b in self.buttons.items():
                        b.active = active
                        self._notify_toggle(k, active)
                last = p
                time.sleep(0.02)

        threading.Thread(target=loop, daemon=True).start()


class MacroManager:
    def __init__(self):
        log("MANAGER", "creating MacroManager")
        self.mouse = MouseEngine()
        self.keyboard = KeyEngine()
        self._listener()
        log("MANAGER", "MacroManager ready")

    def toggle_all(self):
        log("MANAGER", "toggle_all called")
        self.mouse.toggle_global()
        self.keyboard.toggle_global()

    def stop(self):
        log("MANAGER", "stop called")
        self.mouse.stop()
        self.keyboard.stop()

    def set_on_toggle(self, callback: Callable[[str, bool], None]):
        self.mouse.set_on_toggle(callback)
        self.keyboard.set_on_toggle(callback)

    def _listener(self):
        def loop():
            log("LISTENER", "GLOBAL listener started (XBUTTON2)")
            last = False
            while self.mouse.running:
                p = user32.GetAsyncKeyState(VK_XBUTTON2) & 0x8000 != 0
                if p and not last:
                    log("MANAGER", "XBUTTON2 pressed -> toggle_all")
                    self.toggle_all()
                last = p
                time.sleep(0.02)

        threading.Thread(target=loop, daemon=True).start()
