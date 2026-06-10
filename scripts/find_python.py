"""Trouve l'interprete Python du projet."""

from __future__ import annotations

import os
import shutil
import sys


def find_python(root: str | None = None) -> str:
    root = root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parent = os.path.dirname(root)
    candidates = [
        os.path.join(parent, ".venv", "Scripts", "python.exe"),
        os.path.join(root, ".venv", "Scripts", "python.exe"),
        os.path.join(root, "venv", "Scripts", "python.exe"),
        shutil.which("python") or "",
        shutil.which("python3") or "",
        sys.executable,
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return sys.executable
