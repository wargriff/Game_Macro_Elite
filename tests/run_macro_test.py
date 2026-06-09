"""Test headless — reproduit clic MACROS et vérifie master_combo / name_edit."""

import os
import sys
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("XMACRO_DEBUG", "1")

import utils.autopatch  # noqa: F401

from PyQt6.QtWidgets import QApplication

from services.bootstrap import bootstrap
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    errors = []

    print("=== TEST MACROS TAB ===")
    ctx = bootstrap()
    window = MainWindow(ctx.proxy, boot=ctx)
    window.show()
    app.processEvents()

    # Check attrs on window
    for attr in ("master_combo", "name_edit", "macros"):
        try:
            val = getattr(window, attr)
            print(f"[OK] window.{attr} = {type(val).__name__}")
        except Exception as exc:
            errors.append(f"window.{attr}: {exc}")
            print(f"[FAIL] window.{attr}: {exc}")

    # Simulate MACROS tab click
    print("\n=== CLIC ONGLET MACROS ===")
    try:
        window.header._select_tab("macros", emit=True)
        app.processEvents()
        print(f"[OK] stack index = {window.stack.currentIndex()}")
    except Exception as exc:
        errors.append(f"tab macros: {exc}")
        print(f"[FAIL] tab macros: {exc}")
        traceback.print_exc()

    # Simulate sidebar MACRO 1
    print("\n=== CLIC SIDEBAR MACRO 1 ===")
    try:
        window.sidebar._select("macro1", emit=True)
        app.processEvents()
        window.macros.focus_section("macro1")
        app.processEvents()
        print("[OK] focus_section macro1")
    except Exception as exc:
        errors.append(f"macro1: {exc}")
        print(f"[FAIL] macro1: {exc}")
        traceback.print_exc()

    # Refresh loop (like ui_timer)
    print("\n=== REFRESH x5 ===")
    for i in range(5):
        try:
            window.refresh_all()
            app.processEvents()
        except Exception as exc:
            errors.append(f"refresh {i}: {exc}")
            print(f"[FAIL] refresh {i}: {exc}")
            traceback.print_exc()
            break
    else:
        print("[OK] refresh_all x5")

    # Combo switch
    print("\n=== COMBO SWITCH ===")
    try:
        combo = window.master_combo
        for i in range(combo.count()):
            combo.setCurrentIndex(i)
            app.processEvents()
        print(f"[OK] combo {combo.count()} items")
    except Exception as exc:
        errors.append(f"combo: {exc}")
        print(f"[FAIL] combo: {exc}")
        traceback.print_exc()

    window.close()
    ctx.proxy.stop()
    ctx.sidecar.stop()
    if ctx.node:
        ctx.node.stop()

    print("\n=== RESULTAT ===")
    if errors:
        print(f"ECHEC — {len(errors)} erreur(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("SUCCES — pas de bug master_combo/name_edit sur branche Git")
    return 0


if __name__ == "__main__":
    sys.exit(main())
