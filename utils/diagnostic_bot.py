"""
Sanctuary Bot — assistant diagnostic dans la console PyCharm.
Explique où sont les erreurs et guide la correction.
"""

from __future__ import annotations

import os
import sys
import traceback
from typing import Optional, Type

BOT_NAME = "Sanctuary Bot"
_INSTALLED = False
_ORIGINAL_EXCEPTHOOK = sys.excepthook
_HANDLING = False

# Conseils par type d'erreur
_HINTS = {
    "AttributeError": {
        "master_combo": (
            "Le code cherche window.master_combo mais MainWindow ne l'a pas.\n"
            "  → git pull origin cursor/sanctuary-diablo-ui-9626\n"
            "  → Lance Xmacro_main.py (pas un autre script PyCharm)\n"
            "  → Ajoute PYTHONSTARTUP=utils/autopatch.py dans Run Config"
        ),
        "name_edit": (
            "Même problème que master_combo — version locale trop ancienne.\n"
            "  → python CHECK_VERSION.py pour vérifier"
        ),
    },
    "RecursionError": (
        "Boucle infinie d'erreurs (souvent master_combo qui manque en boucle).\n"
        "  → Corrige d'abord l'AttributeError ci-dessus"
    ),
}


def say(msg: str, level: str = "INFO"):
    prefix = {"INFO": "💬", "WARN": "⚠️", "ERR": "❌", "OK": "✅", "AI": "🤖"}.get(level, "💬")
    print(f"{prefix} [{BOT_NAME}] {msg}", flush=True)


def say_block(title: str, lines: list[str]):
    print(f"\n{'='*60}", flush=True)
    say(title, "AI")
    for line in lines:
        print(f"   {line}", flush=True)
    print(f"{'='*60}\n", flush=True)


def _caller_hint() -> Optional[str]:
    """Retourne fichier:ligne de l'appelant (hors libs internes)."""
    stack = traceback.extract_stack()[:-2]
    skip = ("diagnostic_bot", "legacy_patch", "autopatch", "debug.py")
    for frame in reversed(stack):
        if not any(s in frame.filename.replace("\\", "/") for s in skip):
            rel = frame.filename
            try:
                root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                rel = os.path.relpath(frame.filename, root)
            except Exception:
                pass
            return f"{rel}:{frame.lineno} dans {frame.name}()"
    return None


def trace_access(attr: str, obj) -> None:
    where = _caller_hint()
    cls = type(obj).__name__
    say(f"Accès {cls}.{attr} depuis {where or '?'}", "INFO")


def explain_exception(exc_type, exc_value, exc_tb) -> None:
    name = getattr(exc_type, "__name__", str(exc_type))
    msg = str(exc_value)

    lines = [f"Erreur : {name}", f"Message : {msg}"]

    if exc_tb:
        frames = traceback.extract_tb(exc_tb)
        if frames:
            last = frames[-1]
            try:
                root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                rel = os.path.relpath(last.filename, root)
            except Exception:
                rel = last.filename
            lines.append(f"Fichier : {rel}:{last.lineno}")
            lines.append(f"Fonction : {last.name}()")

    hint = None
    if name == "AttributeError":
        for key, text in _HINTS.get("AttributeError", {}).items():
            if key in msg:
                hint = text
                break
    elif name in _HINTS:
        hint = _HINTS[name]

    if hint:
        lines.append("")
        lines.append("Conseil IA :")
        lines.append(hint)

    if "master_combo" in msg or "name_edit" in msg:
        lines.append("")
        lines.append("Vérification rapide :")
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        checks = [
            ("utils/legacy_patch.py", os.path.join(root, "utils", "legacy_patch.py")),
            ("CHECK_VERSION.py", os.path.join(root, "CHECK_VERSION.py")),
        ]
        for label, path in checks:
            status = "OK" if os.path.isfile(path) else "MANQUANT"
            lines.append(f"  [{status}] {label}")

    say_block("DIAGNOSTIC ERREUR", lines)


def _excepthook(exc_type, exc_value, exc_tb):
    global _HANDLING
    if _HANDLING:
        try:
            os.write(2, b"[Sanctuary Bot] arret boucle recursion\n")
        except Exception:
            pass
        return
    _HANDLING = True
    try:
        explain_exception(exc_type, exc_value, exc_tb)
        _ORIGINAL_EXCEPTHOOK(exc_type, exc_value, exc_tb)
    except Exception:
        pass
    finally:
        _HANDLING = False


def startup_report():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    has_patch = os.path.isfile(os.path.join(root, "utils", "legacy_patch.py"))
    has_node = os.path.isdir(os.path.join(root, "nodejs"))
    launcher = sys.argv[0] if sys.argv else "?"

    say_block(
        "DÉMARRAGE — Je surveille ton app",
        [
            f"Script lancé : {launcher}",
            f"Patch legacy : {'actif' if has_patch else 'MANQUANT — git pull!'}",
            f"Dossier nodejs/ : {'oui' if has_node else 'non'}",
            "Je commente chaque erreur avec fichier + ligne + conseil.",
            "Désactiver : set XMACRO_BOT=0",
        ],
    )


def install():
    global _INSTALLED
    if _INSTALLED:
        return
    if os.environ.get("XMACRO_BOT", "1") != "1":
        return

    sys.excepthook = _excepthook
    _INSTALLED = True

    try:
        import utils.legacy_patch as lp
        lp.set_access_tracer(trace_access)
    except Exception:
        pass

    startup_report()
    say("Prêt. Clique MACROS et regarde mes messages ici.", "OK")


def patch_class_if_mainwindow(cls: Type) -> Type:
    """Patch une classe MainWindow custom (non-QMainWindow)."""
    if getattr(cls, "_xclicker_bot_patched", False):
        return cls
    if cls.__name__ != "MainWindow":
        return cls

    from utils.legacy_patch import ensure_instance_legacy

    _orig_init = cls.__init__

    def _patched_init(self, *args, **kwargs):
        _orig_init(self, *args, **kwargs)
        ensure_instance_legacy(self)

    cls.__init__ = _patched_init
    cls._xclicker_bot_patched = True
    say(f"MainWindow custom patché : {cls.__module__}.{cls.__name__}", "OK")
    return cls
