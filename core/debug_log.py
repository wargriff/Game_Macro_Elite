"""Debug logging — affiche dans le terminal PyCharm + forward vers Node.js."""

from datetime import datetime
from typing import Any, Callable, Optional

_node_forwarder: Optional[Callable[[str, str, dict], None]] = None


def set_node_forwarder(forwarder: Callable[[str, str, dict], None]) -> None:
    global _node_forwarder
    _node_forwarder = forwarder


def log(tag: str, msg: str, **kwargs: Any) -> None:
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    extra = " ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
    line = f"[{ts}] [{tag}] {msg}"
    if extra:
        line = f"{line} | {extra}"
    print(line, flush=True)

    if _node_forwarder is not None:
        try:
            _node_forwarder(tag, msg, kwargs)
        except Exception as exc:
            print(f"[{ts}] [DEBUG] node forward failed: {exc}", flush=True)
