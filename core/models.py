import collections
import threading
from dataclasses import dataclass, field


@dataclass
class Btn:
    cps: int = 10
    delay: float = 0.01
    active: bool = False
    burst_count: int = 0


@dataclass
class Stats:
    timestamps: collections.deque = field(
        default_factory=lambda: collections.deque(maxlen=200)
    )
    cps: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)
