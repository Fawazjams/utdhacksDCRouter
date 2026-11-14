"""Protects the NVIDIA key's quota on the public deploy. When a caller is over a limit (or sends an
oversized request), the endpoint just runs without Nemotron: the same offline path as having no key,
so rehearsed requests still work and nothing errors.

In-memory, so limits are per server instance (good enough to stop one visitor looping requests).
"""
import os
import threading
import time
from collections import deque

from fastapi import Request

MAX_TEXT_CHARS = int(os.getenv("LLM_MAX_TEXT_CHARS", "400"))
PER_IP_LIMIT = int(os.getenv("LLM_PER_IP_LIMIT", "8"))          # Nemotron runs per IP per window
PER_IP_WINDOW_S = int(os.getenv("LLM_PER_IP_WINDOW_S", "600"))  # 10 min
GLOBAL_LIMIT = int(os.getenv("LLM_GLOBAL_LIMIT", "120"))        # Nemotron runs per instance per hour
GLOBAL_WINDOW_S = 3600

_lock = threading.Lock()
_by_ip: dict[str, deque[float]] = {}
_global: deque[float] = deque()


def _client_ip(request: Request) -> str:
    # Vercel sets x-real-ip / x-forwarded-for itself (clients can't spoof them there).
    fwd = request.headers.get("x-real-ip") or request.headers.get("x-forwarded-for", "").split(",")[0]
    return fwd.strip() or (request.client.host if request.client else "unknown")


def _prune(q: deque[float], now: float, window: float) -> None:
    while q and now - q[0] > window:
        q.popleft()


def allow(request: Request, text: str = "") -> bool:
    """True = this call may use Nemotron (and counts against the limits)."""
    if len(text) > MAX_TEXT_CHARS:
        return False
    now = time.monotonic()
    ip = _client_ip(request)
    with _lock:
        q = _by_ip.setdefault(ip, deque())
        _prune(q, now, PER_IP_WINDOW_S)
        _prune(_global, now, GLOBAL_WINDOW_S)
        if len(q) >= PER_IP_LIMIT or len(_global) >= GLOBAL_LIMIT:
            return False
        q.append(now)
        _global.append(now)
        if len(_by_ip) > 10_000:  # bound memory
            for k in [k for k, v in _by_ip.items() if not v]:
                del _by_ip[k]
        return True


def reset() -> None:
    with _lock:
        _by_ip.clear()
        _global.clear()
