"""Setup utilitaire — dépendances, déblocage Windows, Node.js (pas de git pull)."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

from scripts.find_python import find_python


def project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_node_exe() -> str | None:
    root = project_root()
    candidates = [
        os.environ.get("XCLICKER_NODE_PATH", ""),
        os.environ.get("NODE", ""),
        r"C:\src\node.exe",
        r"C:\src\node\node.exe",
        os.path.join(root, "nodejs", "node.exe"),
        shutil.which("node") or "",
        r"C:\Program Files\nodejs\node.exe",
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def unblock_windows(root: str | None = None) -> None:
    root = root or project_root()
    if sys.platform != "win32":
        return
    ps = (
        f"Get-ChildItem -LiteralPath '{root}' -Recurse -Force "
        f"| Unblock-File -ErrorAction SilentlyContinue"
    )
    subprocess.call(
        ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps],
        cwd=root,
    )


def install_pip_deps(python: str | None = None, root: str | None = None, *, quiet: bool = True) -> bool:
    root = root or project_root()
    python = python or find_python(root)
    req = os.path.join(root, "requirements.txt")
    if not os.path.isfile(req):
        return True
    flags = ["-q"] if quiet else []
    return subprocess.call([python, "-m", "pip", "install", "-r", req, *flags], cwd=root) == 0


def install_node_deps(root: str | None = None) -> bool:
    root = root or project_root()
    nodejs = os.path.join(root, "nodejs")
    if not os.path.isdir(nodejs):
        return True
    node = find_node_exe()
    if not node:
        print("[setup] Node.js introuvable — interface web limitée")
        return False
    if os.path.isdir(os.path.join(nodejs, "node_modules")):
        return True
    print("[setup] npm install dans nodejs/ ...")
    return subprocess.call(["npm", "install", "--silent"], cwd=nodejs, shell=True) == 0


def needs_pip_install() -> bool:
    try:
        import PyQt6.QtWidgets  # noqa: F401

        return False
    except ImportError:
        return True
