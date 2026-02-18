import time
import httpx
from typing import Any, Optional, Dict
from src.utils.logger import Logger

class HttpClient:
    """
    
    """
    def __init__(self, timeout: int = 10):
        self._client = httpx.Client(timeout=timeout)
        self._timeout = timeout
        
    def get(self, url: str, params: Optional[Dict] = None) -> Any:
        try:
            response = self._client.get(url, params=params, timeout=self._timeout)
            response.raise_for_status()

            return response.json()
        
        except httpx.HTTPError as e:
            Logger.error(f"HTTP request failed: {e}", True)
            raise
        
    def close(self): 
        self._client.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
