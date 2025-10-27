import asyncio
import logging
import random
from typing import Optional, Dict, Any, Set

import aiohttp

from ..client.rate_limiter import RateLimiter

_LOGGER = logging.getLogger(__name__)

MAX_ATTEMPTS = 3
RETRY_STATUS_CODES = {429, 504}
INITIAL_BACKOFF = 1
MAX_BACKOFF = 30

rate_limiter = RateLimiter(max_calls=10, period=1.0)  # 10 calls per second
concurrency_semaphore = asyncio.Semaphore(5)  # 5 concurrent calls


async def request(
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Make an HTTP request with retry, rate limiting, and concurrency control.

    Args:
        method: HTTP method (e.g., 'GET', 'POST')
        url: Full URL to call
        headers: Optional HTTP headers
        json_body: Optional JSON body for POST/PUT
    """
    allow_retry_statuses = RETRY_STATUS_CODES

    for attempt in range(1, MAX_ATTEMPTS + 1):
        await rate_limiter.acquire()

        try:
            async with concurrency_semaphore:
                async with aiohttp.ClientSession() as session:
                    async with session.request(
                            method=method,
                            url=url,
                            headers=headers,
                            json=json_body
                    ) as response:

                        if response.status not in allow_retry_statuses:
                            response_body = await response.json()
                            status = response.status
                            if 400 <= response.status < 600:
                                raise aiohttp.ClientResponseError(
                                    request_info=response.request_info,
                                    history=response.history,
                                    status=response.status,
                                    message=str(response_body),
                                    headers=response.headers,
                                )
                            _LOGGER.debug("Response from %s. status_code: %s, body: %s", url, status, response_body)
                            return response_body

                        if attempt == MAX_ATTEMPTS:
                            response_text = await response.text()
                            _LOGGER.warning(f"Request failed after {MAX_ATTEMPTS} attempts. "
                                            f"Status: {response.status}, Body: {response_text}")
                            response.raise_for_status()

        except aiohttp.ClientResponseError as e:
            if attempt == MAX_ATTEMPTS or e.status not in allow_retry_statuses:
                raise e

        # Wait before next attempt
        backoff = min(INITIAL_BACKOFF * 2 ** (attempt - 1), MAX_BACKOFF)
        jitter = random.uniform(0, backoff * 0.3)
        await asyncio.sleep(backoff + jitter)

    raise RuntimeError("Unexpected error in retry logic.")
