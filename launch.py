"""
Logique de lancement — NE PAS importer ui.* ici.
Utilise par run.py, main.py et le .exe PyInstaller.
"""

import argparse
import os
import sys


def run(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="Game XClicker Elite")
    parser.add_argument("--pyqt", action="store_true", help="Interface PyQt legacy")
    parser.add_argument("--browser", action="store_true", help="UI dans le navigateur")
    args = parser.parse_args(argv)

    try:
        from config.asset_system import assets
        missing = assets.verify()
        for m in missing:
            print(f"[LAUNCH] asset manquant: {m}")
    except Exception as exc:
        print(f"[LAUNCH] assets: {exc}")

    if args.pyqt:
        from Xmacro_main import main as pyqt_main
        return pyqt_main()

    if args.browser:
        os.environ["XCLICKER_UI"] = "browser"

    from launcher.desktop_main import main as desktop_main
    return desktop_main()
