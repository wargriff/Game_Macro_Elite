"""
Game XClicker Elite — lanceur unique.

Utilisateur :
  - Windows : double-clic OUVRE_MOI.pyw
  - Terminal : python OUVRE_MOI.py  ou  python launcher.py

Mission Control (interface) gère ensuite native / web / build / .exe.
Maintenance seule : python REPARER.py
"""

from __future__ import annotations

import os
import subprocess
import sys
import traceback

ROOT = os.path.dirname(os.path.abspath(__file__))
ENTRY = "GameXClicker.py"


def prepare(root: str | None = None) -> str:
    root = root or ROOT
    os.chdir(root)
    if root not in sys.path:
        sys.path.insert(0, root)
    from utils.bootstrap import ensure_project_ready

    ensure_project_ready(root)
    return root


def show_error(message: str, *, title: str = "Game XClicker Elite") -> None:
    if sys.platform == "win32":
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)
            return
        except Exception:
            pass
    print(message, file=sys.stderr)


def verify_installation(root: str | None = None) -> str | None:
    root = root or ROOT
    if os.path.isfile(os.path.join(root, ENTRY)):
        return None
    return (
        "Fichiers du projet incomplets.\n\n"
        "Ouvrez PowerShell dans ce dossier et lancez :\n"
        "  python REPARER.py"
    )


def ensure_dependencies(*, quiet: bool = True) -> bool:
    from scripts.setup import install_pip_deps, needs_pip_install

    if not needs_pip_install():
        return True
    print("[launcher] Installation des dépendances Python...")
    return install_pip_deps(quiet=quiet)


def run(argv: list[str] | None = None) -> int:
    """Prépare l'environnement puis ouvre Mission Control (ou mode CLI)."""
    prepare()
    err = verify_installation()
    if err:
        show_error(err)
        return 1
    if not ensure_dependencies():
        show_error(
            "Impossible d'installer les dépendances.\n\n"
            "python -m pip install -r requirements.txt"
        )
        return 1

    if argv is not None:
        saved = sys.argv
        sys.argv = [ENTRY, *argv]
        try:
            from GameXClicker import main

            return main()
        finally:
            sys.argv = saved

    from GameXClicker import main

    return main()


def run_safe(argv: list[str] | None = None) -> int:
    """Comme run(), avec boîte d'erreur pour pythonw (double-clic)."""
    try:
        return run(argv)
    except SystemExit:
        raise
    except Exception:
        show_error(traceback.format_exc())
        return 1


def main() -> int:
    if len(sys.argv) > 1:
        return run(sys.argv[1:])
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
