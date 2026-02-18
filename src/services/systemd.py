import time
from typing import List
from pystemd.systemd1 import Unit, Manager
from src.core.interfaces import IServiceManager
from src.utils.logger import Logger

class SystemdManager(IServiceManager):
    """
    General implementation using pystemd.
    """
    def start(self, unit_name: str) -> bool:
        try:
            with Unit(unit_name.encode(), _autoload= True) as unit:
                unit.Unit.Start(b'replace')
                
                return True
        except Exception as e:
            Logger.error(f"Systemd start failed: {e}", True)
            return False
    
    def stop(self, unit_name: str) -> bool:
        try:
            with Unit(unit_name.encode(), _autoload=True) as unit:
                unit.Unit.Stop(b'replace')
                return True
        except Exception as e:
            Logger.error(f"Systemd stop failed: {e}", True)
            return False
        
    def is_active(self, unit_name: str) -> bool:
        try: 
            with Unit(unit_name.encode(), _autoload=True) as unit:
                return unit.Unit.ActiveState == b'active'
        except Exception as e:
            Logger.error(f"Systemd status failed: {e}", True)
            return False
    
    def list_active(self, pattern: str) -> List[str]:
        try: 
            with Manager() as manager:
                manager.load()
                units = manager.Manager.ListUnits()
                b_pattern = pattern.encode()

            return [
                u[0].decode() for u in units

                if u[0].startswith(b_pattern) and u[3] == b'active'
            ]
        except Exception as e:
            Logger.error(f"Systemd list actives failed: {e}", True)
            return []