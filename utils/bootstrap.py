"""Bootstrap — corrige conflit ui.py / dossier ui/."""

import os
import sys

from config.runtime import exe_dir, project_root


def ensure_project_ready(root: str | None = None) -> bool:
    root = root or project_root()
    if root not in sys.path:
        sys.path.insert(0, root)
    _fix_ui_py_conflict(exe_dir())
    _purge_bad_ui_module()
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
        print(f"[BOOT] ui.py -> {os.path.basename(backup)}")
    except OSError as exc:
        print(f"[BOOT] ren ui.py ui_old.py ({exc})")


def _purge_bad_ui_module():
    if "ui" not in sys.modules:
        return
    mod = sys.modules["ui"]
    if (getattr(mod, "__file__", "") or "").replace("\\", "/").endswith("/ui.py"):
        del sys.modules["ui"]
