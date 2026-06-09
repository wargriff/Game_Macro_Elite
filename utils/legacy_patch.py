"""Correctifs legacy — master_combo / name_edit sur TOUT QMainWindow + QWidget."""

from __future__ import annotations

_APPLIED = False
_LEGACY_NAMES = ("master_combo", "name_edit")
_ACCESS_TRACER = None


def set_access_tracer(fn):
    global _ACCESS_TRACER
    _ACCESS_TRACER = fn


def _trace(name: str, obj):
    if _ACCESS_TRACER:
        try:
            _ACCESS_TRACER(name, obj)
        except Exception:
            pass


def _create_legacy(name: str):
    from PyQt6.QtWidgets import QComboBox, QLineEdit

    if name == "name_edit":
        edit = QLineEdit("default")
        edit.setReadOnly(True)
        return edit

    combo = QComboBox()
    try:
        from ui.pages.macros_page import MACRO_KEYS

        for _, label in MACRO_KEYS:
            combo.addItem(label)
    except Exception:
        combo.addItem("Macro 1 — Clic gauche")
        combo.addItem("Macro 2 — Clic droit")
    return combo


def ensure_instance_legacy(obj) -> None:
    """Injecte master_combo/name_edit sur n'importe quel objet window."""
    for name in _LEGACY_NAMES:
        try:
            val = getattr(obj, name)
            if val is not None:
                continue
        except AttributeError:
            pass
        widget = _create_legacy(name)
        try:
            setattr(obj, name, widget)
        except Exception:
            key = f"_xclicker_legacy_{name}"
            obj.__dict__[key] = widget
        _trace(name, obj)


def _resolve_legacy(self, name: str):
    storage = f"_xclicker_legacy_{name}"
    data = object.__getattribute__(self, "__dict__")
    if storage not in data:
        data[storage] = _create_legacy(name)
        _trace(name, self)

    macros = data.get("macros")
    if macros is not None and hasattr(macros, name):
        return getattr(macros, name)
    return data[storage]


def _patch_qt_class(qt_cls) -> bool:
    if getattr(qt_cls, "_xclicker_legacy_patch", False):
        return True

    _orig = qt_cls.__getattribute__

    def _patched_getattribute(self, name: str):
        if name in _LEGACY_NAMES:
            try:
                return _orig(self, name)
            except AttributeError:
                return _resolve_legacy(self, name)
        return _orig(self, name)

    qt_cls.__getattribute__ = _patched_getattribute
    qt_cls._xclicker_legacy_patch = True
    return True


def apply_legacy_patch() -> bool:
    global _APPLIED
    if _APPLIED:
        return True

    try:
        from PyQt6.QtWidgets import QMainWindow, QWidget
    except Exception:
        return False

    ok = _patch_qt_class(QMainWindow) and _patch_qt_class(QWidget)
    _APPLIED = ok
    return ok


def hook_mainwindow_import():
    try:
        import ui.main_window as mw

        cls = getattr(mw, "MainWindow", None)
        if cls and cls.__name__ == "MainWindow":
            from utils.diagnostic_bot import patch_class_if_mainwindow
            patch_class_if_mainwindow(cls)
    except Exception:
        pass


apply_legacy_patch()
