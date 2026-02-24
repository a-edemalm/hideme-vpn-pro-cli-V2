from typing import Any, Dict, Optional

import httpx

from src.utils.logger import Logger


class HttpClient:
    """
    Wrapper for httpx to handle synchronous requests.
    """

    def __init__(self, timeout: int = 10):
        self._timeout = timeout

        self._async_client = httpx.AsyncClient(timeout=timeout)

    async def get_async(self, url: str, params: Optional[Dict] = None) -> Any:
        """
        Executes GET request.
        :param url: Target endpoint
        :param params: Optional query parameters
        """
        try:
            response = await self._async_client.get(url, params=params)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            Logger.error(f"Async HTTP request failed: {e}")
            return None

    async def close(self):
        """
        Cleanup client resources.
        """
        await self._async_client.aclose()
