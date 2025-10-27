import asyncio
import time
from collections import deque


class RateLimiter:
    """
    Async rate limiter to allow up to `max_calls` within `period` seconds.
    """

    def __init__(self, max_calls: int, period: float):
        """
        Args:
            max_calls: Max number of allowed calls in the period.
            period: Time window in seconds.
        """

        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self._lock = asyncio.Lock()

    async def acquire(self):
        """Wait until the rate limit allows a new call."""
        async with self._lock:
            now = time.monotonic()
            while len(self.calls) >= self.max_calls:
                oldest = self.calls[0]
                if now - oldest > self.period:
                    self.calls.popleft()
                else:
                    sleep_time = self.period - (now - oldest)
                    await asyncio.sleep(sleep_time)
                    now = time.monotonic()
            self.calls.append(now)
