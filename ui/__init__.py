"""UI entry points — Sanctuary Edition (imports paresseux = démarrage plus rapide)."""

import utils.legacy_patch  # noqa: F401 — patch QMainWindow avant import fenêtre

__all__ = ["MainWindow", "SanctuaryWindow", "UI", "AssetSystem", "assets"]


def __getattr__(name: str):
    if name in ("AssetSystem", "assets"):
        from ui import asset_system
        return asset_system.AssetSystem if name == "AssetSystem" else asset_system.assets
    if name not in ("MainWindow", "SanctuaryWindow", "UI"):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from ui.sanctuary_window import MainWindow, SanctuaryWindow

    if name == "MainWindow":
        return MainWindow
    if name == "SanctuaryWindow":
        return SanctuaryWindow
    return SanctuaryWindow
