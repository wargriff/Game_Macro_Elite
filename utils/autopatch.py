"""
Auto-patch — chargé via PYTHONSTARTUP ou en premier dans Xmacro_main.
Applique legacy_patch + Sanctuary Bot même si PyCharm lance un autre script.
"""

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

try:
    import utils.legacy_patch  # noqa: F401
except Exception as _exc:
    print(f"[autopatch] legacy_patch failed: {_exc}", flush=True)

try:
    import utils.diagnostic_bot as bot
    bot.install()
except Exception as _exc:
    print(f"[autopatch] diagnostic_bot failed: {_exc}", flush=True)
