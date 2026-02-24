import asyncio
from typing import List, Optional

from core import converters
from core.dtos import IpCheckDto, ServerDto
from core.interfaces import INetworkMonitor, IServiceManager, IVpnProvider
from utils.http_client import HttpClient
from utils.logger import Logger


class HideMeService(IVpnProvider):
    """ """

    _PREFIX = "hide.me@"
    _URL_SERVERS = "https://api.hide.me/v1/network/free/en"
    _URL_IP_CHECK = "https://api.hide.me/ip"
    _RE_ATTEMPTS = 3
    _WAIT_INTERVAL = 2.0

    def __init__(
        self, sys_mgr: IServiceManager, net_mon: INetworkMonitor, http: HttpClient
    ):

        self._sys_mgr = sys_mgr
        self._net_mon = net_mon
        self._http = http
        self._cached_servers: List[ServerDto] = []

    async def fetch_servers(self) -> List[ServerDto]:
        if self._cached_servers:
            return self._cached_servers

        try:
            if data := await self._http.get_async(self._URL_SERVERS):
                self._cached_servers = [
                    converters.dict_to_server_dto(item) for item in data
                ]

            return self._cached_servers
        except Exception as e:
            Logger.error(f"Server fetch failed: {e}")
            return []

    async def is_connected(self) -> bool:
        if await self._wait_for_tunnel(timeout=6):
            if info := await self.get_connectivity():
                return info.IS_PROTECTED

        return False

    async def get_connectivity(self) -> Optional[IpCheckDto]:
        try:
            if not (data := await self._http.get_async(self._URL_IP_CHECK)):
                Logger.error("Connectivity check, retrieved no data")
                return None

            return converters.dict_to_ip_check(data)
        except Exception as e:
            Logger.error(f"Connectivity check failed: {e}")
            return None

    async def connect(self, server: ServerDto) -> bool:
        unit = f"{self._PREFIX}{server.FLAG}.service"

        try:
            if not await self.disconnect():
                return False

            if not await self._sys_mgr.start(unit):
                return False

            if await self._wait_for_tunnel(timeout=20):
                return True

            raise TimeoutError("Network interface timeout")
        except Exception as e:
            Logger.error(f"Connection failed: {e}")
            await self._sys_mgr.stop(unit)
            return False

    async def disconnect(self) -> bool:
        if not (active_units := await self._sys_mgr.list_active(self._PREFIX)):
            return True

        results = []

        for unit in active_units:
            results.append(await self._stop_unit_with_retry(unit))

        return all(results)

    async def _stop_unit_with_retry(self, unit: str) -> bool:
        for attempt in range(1, self._RE_ATTEMPTS + 1):
            await self._sys_mgr.stop(unit)

            await asyncio.sleep(self._WAIT_INTERVAL)

            if not await self._sys_mgr.is_active(unit):
                return True

            Logger.warning(
                f"Retry {attempt}/{self._RE_ATTEMPTS}: {unit} still active..."
            )

        Logger.error(
            f"CRITICAL: Failed to stop {unit} after {self._RE_ATTEMPTS} attempts."
        )
        return False

    async def _wait_for_tunnel(self, timeout: int = 6) -> bool:
        """Helper to poll network monitor until tunnel is up."""
        loop = asyncio.get_running_loop()
        start = loop.time()
        while (loop.time() - start) < timeout:
            if self._net_mon.is_tunnel_interface():
                return True
            await asyncio.sleep(0.5)
        return False
