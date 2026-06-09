import os
import signal
import sys
import traceback

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from core.debug_log import log
from core.engine import MacroManager
from services.ai_guardian import start_ai_guardian, stop_ai_guardian
from services.engine_proxy import EngineProxy
from ui.main_window import MainWindow

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


_original_excepthook = sys.excepthook
_handling_fatal = False


def handle_exception(exc_type, exc_value, exc_tb):
    global _handling_fatal
    if _handling_fatal:
        _original_excepthook(exc_type, exc_value, exc_tb)
        return
    _handling_fatal = True
    try:
        print(f"[FATAL] {exc_type.__name__}: {exc_value}")
        traceback.print_exception(exc_type, exc_value, exc_tb)
    except Exception:
        _original_excepthook(exc_type, exc_value, exc_tb)
    finally:
        _handling_fatal = False


sys.excepthook = handle_exception


def safe_stop(engine):
    if not engine:
        return
    try:
        engine.stop()
    except Exception:
        pass


def main():
    log("XMACRO", "Booting...")
    log("XMACRO", f"Projet: {PROJECT_ROOT}")

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    guardian = None
    try:
        guardian = start_ai_guardian(PROJECT_ROOT)
    except Exception as exc:
        log("AI", f"Guardian non démarré: {exc}")

    app = QApplication(sys.argv)

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    proxy = None
    exit_code = 0

    try:
        log("XMACRO", "Initialisation moteur...")
        manager = MacroManager()
        proxy = EngineProxy(manager)
        log("XMACRO", "Ouverture interface...")
        window = MainWindow(proxy, "assets/mouse.svg")
        window.show()
        log("XMACRO", "Application prête")

        def shutdown():
            log("XMACRO", "Shutting down...")
            safe_stop(proxy)
            stop_ai_guardian()

        app.aboutToQuit.connect(shutdown)
        exit_code = app.exec()

    except Exception:
        traceback.print_exc()
        exit_code = 1

    finally:
        safe_stop(proxy)
        stop_ai_guardian()
        log("XMACRO", "Exit complete")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
