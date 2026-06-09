import signal
import sys
import traceback

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from core.debug_log import log, set_node_forwarder
from core.engine import MacroManager
from rgb_engine import RGBEngine
from services.engine_proxy import EngineProxy
from services.node_sidecar import forward_log, get_sidecar, start_node_sidecar
from services.profile_manager import ProfileManager
from ui import UI


def handle_exception(exc_type, exc_value, exc_tb):
    log("FATAL", f"{exc_type.__name__}: {exc_value}")
    traceback.print_exception(exc_type, exc_value, exc_tb)


sys.excepthook = handle_exception


def safe_stop(proxy, node_sidecar):
    if proxy:
        try:
            proxy.stop()
        except Exception as exc:
            log("SHUTDOWN", f"proxy stop error: {exc}")
    if node_sidecar:
        try:
            node_sidecar.stop()
        except Exception as exc:
            log("SHUTDOWN", f"node stop error: {exc}")


def main():
    log("XMACRO", "Booting XMacro Elite PRO…")

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    proxy = None
    node_sidecar = None
    exit_code = 0

    try:
        log("XMACRO", "Starting Node.js sidecar…")
        node_sidecar = start_node_sidecar()
        set_node_forwarder(forward_log)

        log("XMACRO", "Initializing macro engine…")
        manager = MacroManager()
        proxy = EngineProxy(manager)

        log("XMACRO", "Loading profile…")
        profiles = ProfileManager()
        profiles.load("default")
        profiles.apply_to_engine(manager)

        rgb = RGBEngine()
        profiles.apply_to_rgb(rgb)

        def on_toggle(key, active):
            log("RGB", f"reactive trigger {key} active={active}")
            rgb.trigger_reactive(key if key in rgb.zones else "left")

        proxy.set_on_toggle(on_toggle)

        log("XMACRO", "Opening UI…")
        ui = UI(proxy, "assets/mouse.png", rgb=rgb)
        ui.show()

        def shutdown():
            log("XMACRO", "Shutting down…")
            safe_stop(proxy, node_sidecar)

        app.aboutToQuit.connect(shutdown)
        exit_code = app.exec()

    except Exception:
        traceback.print_exc()
        exit_code = 1

    finally:
        safe_stop(proxy, node_sidecar or get_sidecar())
        log("XMACRO", "Exit complete")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
