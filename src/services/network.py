import os
from pathlib import Path
from typing import Optional
from src.core.interfaces import INetworkMonitor
from src.models.enums import HideMeConfig
from src.utils.logger import Logger

class NetworkService(INetworkMonitor):
    """Detects VPN interfaces via the Linux filesystem directly."""
    
    SYS_NET = Path("/sys/class/net")

    def is_tunnel_interface(self) -> bool:
        """
        Scans /sys/class/net to find virtual tunnels.
        """
        
        try: 

            for iface in self.SYS_NET.iterdir():
                if iface.name.startswith(('tun', HideMeConfig.IFACE.TUNNEL)):
                    
                    state_file = iface / "operstate"
                    if state_file.exists():
                        current_status = state_file.read_text().strip()
                        
                        if  current_status in HideMeConfig.IFACE.IS_STATE_UP: 
                            return True
        
        except Exception as e:
            Logger.warning(f"Failed retrieving tunnel interface: {e}", True)
            return False
        
        return False
        