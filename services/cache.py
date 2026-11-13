"""
In-memory TTL (Time-To-Live) Cache for live financial data.
Prevents upstream rate limiting while ensuring data freshness (< 30s).
"""
import time
import threading
from typing import Any, Optional


class TTLCache:
    def __init__(self, default_ttl: int = 30):
        self.default_ttl = default_ttl
        self._cache: dict[str, tuple[float, Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key in self._cache:
                expiry, value = self._cache[key]
                if time.time() < expiry:
                    return value
                del self._cache[key]
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        duration = ttl if ttl is not None else self.default_ttl
        with self._lock:
            self._cache[key] = (time.time() + duration, value)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        """Return the number of non-expired entries."""
        now = time.time()
        with self._lock:
            return sum(1 for expiry, _ in self._cache.values() if now < expiry)

    def cleanup(self) -> int:
        """Remove expired entries. Returns count of entries removed."""
        now = time.time()
        with self._lock:
            expired = [k for k, (expiry, _) in self._cache.items() if now >= expiry]
            for k in expired:
                del self._cache[k]
            return len(expired)


# Global cache instance: 30-second TTL
cache = TTLCache(default_ttl=30)
