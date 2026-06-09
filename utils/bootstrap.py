"""
Bootstrap — corrige ui.py vs dossier ui/ (cause #1 des crashes Windows).
"""

import os
import sys

from config.runtime import exe_dir, project_root


def ensure_project_ready(root: str | None = None) -> bool:
    root = root or project_root()
    dev_root = exe_dir()

    if root not in sys.path:
        sys.path.insert(0, root)

    # Conflit ui.py dans le dossier dev (pas dans le .exe)
    _fix_ui_py_conflict(dev_root)
    _purge_bad_ui_module()
    _ensure_asset_system(root)
    return True


def _fix_ui_py_conflict(root: str):
    ui_py = os.path.join(root, "ui.py")
    ui_dir = os.path.join(root, "ui")
    if not (os.path.isfile(ui_py) and os.path.isdir(ui_dir)):
        return

    backup = ui_py + ".bak"
    n = 1
    while os.path.exists(backup):
        backup = ui_py + f".bak{n}"
        n += 1

    try:
        os.rename(ui_py, backup)
        print(f"[BOOT] ui.py renomme -> {os.path.basename(backup)}")
    except OSError as exc:
        print(f"[BOOT] ERREUR ui.py: {exc}")
        print("[BOOT] Fermez PyCharm puis: ren ui.py ui_old.py")


def _purge_bad_ui_module():
    if "ui" not in sys.modules:
        return
    mod = sys.modules["ui"]
    mod_file = (getattr(mod, "__file__", "") or "").replace("\\", "/")
    if mod_file.endswith("/ui.py"):
        del sys.modules["ui"]


def _ensure_asset_system(root: str):
    cfg = os.path.join(root, "config", "asset_system.py")
    if os.path.isfile(cfg):
        return
    ui_copy = os.path.join(root, "ui", "asset_system.py")
    if os.path.isfile(ui_copy):
        import shutil
        os.makedirs(os.path.dirname(cfg), exist_ok=True)
        shutil.copy2(ui_copy, cfg)
