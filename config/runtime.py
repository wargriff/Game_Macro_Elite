"""Racine projet — dev ou PyInstaller."""

import os
import sys

_PKG_ROOT = os.path.dirname(os.path.abspath(__file__))


def project_root() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(_PKG_ROOT)


def exe_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
