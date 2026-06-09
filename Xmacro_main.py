import signal
import sys
import traceback

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from services.bootstrap import bootstrap
from ui.sanctuary_window import SanctuaryWindow
from ui.splash_screen import SplashScreen

_handling_fatal = False


def handle_exception(exc_type, exc_value, exc_tb):
    global _handling_fatal
    if _handling_fatal:
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return
    _handling_fatal = True
    try:
        print(f"[FATAL] {exc_type.__name__}: {exc_value}", file=sys.stderr)
        traceback.print_exception(exc_type, exc_value, exc_tb, file=sys.stderr)
    finally:
        _handling_fatal = False


sys.excepthook = handle_exception


def safe_stop(ctx):
    if not ctx:
        return
    try:
        ctx.proxy.stop()
        ctx.sidecar.stop()
    except Exception:
        pass


def main():
    print("[XMACRO] Booting unified launcher…")

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setApplicationName("Game XClicker Elite")

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    splash = SplashScreen()
    splash.show()
    app.processEvents()

    ctx = None
    exit_code = 0

    try:
        def on_progress(percent: int, message: str):
            splash.set_progress(percent, message)
            app.processEvents()

        ctx = bootstrap(on_progress)
        splash.set_progress(95, "Ouverture interface iCUE Sanctuary…")
        app.processEvents()

        window = SanctuaryWindow(ctx.proxy, boot=ctx)
        window.show()
        splash.close()

        def shutdown():
            print("[XMACRO] Shutting down…")
            safe_stop(ctx)

        app.aboutToQuit.connect(shutdown)
        exit_code = app.exec()

    except Exception:
        traceback.print_exc()
        splash.set_progress(0, "Erreur au démarrage — voir la console")
        exit_code = 1

    finally:
        safe_stop(ctx)
        print("[XMACRO] Exit complete")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
