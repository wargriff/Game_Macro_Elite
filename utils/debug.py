"""Debug logging — activer avec XMACRO_DEBUG=1 dans PyCharm ou terminal."""

import os
import sys
import traceback
from functools import wraps


DEBUG = os.environ.get("XMACRO_DEBUG", "1") == "1"


def log(tag: str, msg: str):
    if DEBUG:
        print(f"[{tag}] {msg}", flush=True)


def log_exc(tag: str, exc: BaseException):
    if DEBUG:
        print(f"[{tag}] ERREUR: {exc}", flush=True)
        traceback.print_exc()


def trace(tag: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            log(tag, f"→ {fn.__name__}")
            try:
                result = fn(*args, **kwargs)
                log(tag, f"← {fn.__name__} OK")
                return result
            except Exception as exc:
                log_exc(tag, exc)
                raise
        return wrapper
    return decorator
