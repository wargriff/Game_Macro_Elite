"""UI entry points — Sanctuary Edition (imports paresseux = démarrage plus rapide)."""

import utils.legacy_patch  # noqa: F401 — patch QMainWindow avant import fenêtre

__all__ = ["MainWindow", "SanctuaryWindow", "UI"]


def __getattr__(name: str):
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from ui.sanctuary_window import MainWindow, SanctuaryWindow

    if name == "MainWindow":
        return MainWindow
    if name == "SanctuaryWindow":
        return SanctuaryWindow
    return SanctuaryWindow
