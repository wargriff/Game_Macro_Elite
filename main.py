"""
Point d'entrée principal — Game XClicker Elite v3.0

Usage:
  python main.py              # Interface JS iCUE (défaut)
  python main.py --pyqt       # PyQt Sanctuary legacy
  python main.py --browser    # Ouvre le navigateur
"""

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import utils.autopatch  # noqa: F401


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Game XClicker Elite — SOURIS WARGRIFF")
    parser.add_argument(
        "--pyqt",
        action="store_true",
        help="Interface PyQt Sanctuary (legacy)",
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Ouvre l'UI web dans le navigateur",
    )
    args = parser.parse_args(argv)

    from ui.asset_system import assets

    missing = assets.verify()
    if missing:
        print("[MAIN] Assets manquants (non bloquant):")
        for m in missing:
            print(f"  - {m}")

    if args.pyqt:
        from Xmacro_main import main as pyqt_main
        return pyqt_main()

    if args.browser:
        os.environ["XCLICKER_UI"] = "browser"

    from launcher.desktop_main import main as desktop_main
    return desktop_main()


if __name__ == "__main__":
    raise SystemExit(main())
