from core.debug_log import log
from core.engine import MacroManager


class EngineProxy:
    def __init__(self, manager: MacroManager):
        self.manager = manager
        self.buttons = {
            **manager.mouse.buttons,
            **manager.keyboard.buttons,
        }
        log("PROXY", "EngineProxy created", buttons=list(self.buttons.keys()))

    @property
    def enabled(self):
        return self.manager.mouse.enabled and self.manager.keyboard.enabled

    @property
    def running(self):
        return self.manager.mouse.running and self.manager.keyboard.running

    @running.setter
    def running(self, state: bool):
        log("PROXY", f"running -> {state}")
        self.manager.mouse.running = state
        self.manager.keyboard.running = state

    def toggle(self):
        log("PROXY", "toggle() called from UI")
        self.manager.toggle_all()

    def stop(self):
        log("PROXY", "stop() called")
        self.manager.stop()

    def set_game_safe(self, state: bool):
        log("PROXY", f"game_safe -> {state}")
        self.manager.mouse.game_safe = state
        self.manager.keyboard.game_safe = state

    def set_on_toggle(self, callback):
        self.manager.set_on_toggle(callback)

    def _get_engine(self, key):
        if key in self.manager.mouse.buttons:
            return self.manager.mouse
        return self.manager.keyboard

    def set_cps(self, key, value):
        log("PROXY", f"set_cps {key}={value}")
        self._get_engine(key).set_cps(key, value)

    def set_delay(self, key, value):
        log("PROXY", f"set_delay {key}={value}")
        self._get_engine(key).set_delay(key, value)

    def set_burst_count(self, key, value):
        self._get_engine(key).set_burst_count(key, value)

    def get_burst_count(self, key):
        return self._get_engine(key).get_burst_count(key)

    def get_cps(self, key):
        return self._get_engine(key).get_cps(key)

    def get_real_cps(self, key):
        return self._get_engine(key).get_real_cps(key)

    def set_active(self, key, state: bool):
        engine = self._get_engine(key)
        if key in engine.buttons:
            log("PROXY", f"set_active {key}={state}")
            engine.buttons[key].active = state

    def is_active(self, key) -> bool:
        btn = self.buttons.get(key)
        return btn.active if btn else False

    def count_active_macros(self) -> int:
        return sum(1 for b in self.buttons.values() if b.active)

    def get_total_cps(self) -> int:
        total = 0
        for key in self.buttons:
            if self.is_active(key):
                total += self.get_real_cps(key)
        return total
