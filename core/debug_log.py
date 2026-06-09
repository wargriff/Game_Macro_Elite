"""Debug logging — prints in PyCharm terminal + forwards to Node.js sidecar."""

from datetime import datetime
from typing import Any, Dict, Optional

_node_forwarder = None


def set_node_forwarder(forwarder):
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


def log_state(tag: str, key: str, old: Any, new: Any) -> None:
    if old != new:
        log(tag, f"{key} changed", old=old, new=new)
