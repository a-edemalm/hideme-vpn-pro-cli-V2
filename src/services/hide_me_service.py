import time
from typing import List, Optional

from src.core.interfaces import IVpnProvider, IServiceManager, INetworkMonitor
from src.models.server import Server
from src.models.connection_info import ConnectionInfo
from src.models.enums import HideMeConfig
from src.utils.http_client import HttpClient
from src.utils.logger import Logger

class HideMeService(IVpnProvider):
    """
    """
    def __init__(self, 
                 sys_mgr: IServiceManager,
                 net_mon: INetworkMonitor,
                 http: HttpClient):

        self._sys_mgr = sys_mgr
        self._net_mon = net_mon
        self._http = http
        self._cached_servers: List[Server] = []

    def fetch_servers(self) -> List[Server]:
        if self._cached_servers: return self._cached_servers
        
        try:
            data = self._http.get(HideMeConfig.URL.SERVERS)

            self._cached_servers = [Server.from_dict(item) for item in data]

            return self._cached_servers
        
        except Exception as e:
            Logger.error(f"Server fetch failed: {e}")
            return []

    def is_connected(self) -> bool:

        if self._wait_for_tunnel(timeout=3):

            info = self.get_connectivity()

            if info and info.IS_PROTECTED:
                return True
            
        return False
    
    def get_connectivity(self) -> Optional[ConnectionInfo]:
        try:
            data = self._http.get(HideMeConfig.URL.IP_CHECK)
            info = ConnectionInfo.from_dict(data)

            if not info.IS_PROTECTED:
                Logger.warning(f"Verified: UNPROTECTED! Real IP {info.IP} leaked.")

            return info
        
        except Exception as e:
            Logger.error(f"Connectivity check failed: {e}")
            return None
        
    def connect(self, server: Server) -> bool:
        unit = f"{HideMeConfig.SERVICE.PREFIX}{server.FLAG}.service"

        self.disconnect()

        if not self._sys_mgr.start(unit):
            return False
        
        if self._wait_for_tunnel(timeout=10):
            return True
        
        Logger.error("Systemd started, but no network interface appeard.")
        
        self._sys_mgr.stop(unit)
        return False

    def disconnect(self) -> bool:
        active_units = self._sys_mgr.list_active(HideMeConfig.SERVICE.PREFIX)

        if not active_units:
            return True
        
        all_stopped = True
        
        for unit in active_units:
            unit_stopped = False

            for _ in range(1, HideMeConfig.RE_ATTEMPTS + 1):
                    
                self._sys_mgr.stop(unit)

                if not self._sys_mgr.is_active(unit):
                    unit_stopped = True
                    break
                
                time.sleep(2)

            if not unit_stopped:
                Logger.error(f"CRITICAL: Failed to stop {unit}, after \
                            {HideMeConfig.RE_ATTEMPTS} attempts.",)
                all_stopped = False
        
        return all_stopped
    
    def _wait_for_tunnel(self, timeout: int = 10) -> bool:
        """Helper to poll network monitor until tunnel is up."""
        start = time.time()
        while time.time() - start < timeout:
            if self._net_mon.is_tunnel_interface():
                return True
            time.sleep(0.5)
        return False