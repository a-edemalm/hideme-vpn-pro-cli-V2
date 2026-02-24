import asyncio
from typing import List

from pystemd.systemd1 import Manager, Unit

from src.core.interfaces import IServiceManager
from src.utils.logger import Logger


class SystemdManager(IServiceManager):
    """
    General implementation using pystemd.
    """

    # --- ASYNC CALLS ---
    async def start(self, unit_name: str) -> bool:
        return await asyncio.to_thread(self._execute_unit_action, unit_name, "Start")

    async def stop(self, unit_name: str) -> bool:
        return await asyncio.to_thread(self._execute_unit_action, unit_name, "Stop")

    async def is_active(self, unit_name: str) -> bool:
        return await asyncio.to_thread(self._is_active_sync, unit_name)

    async def list_active(self, pattern: str) -> list[str]:
        return await asyncio.to_thread(self._list_active_sync, pattern)

    # --- SYNC PRIVATE METHODS ---

    def _execute_unit_action(self, unit_name: str, action: str) -> bool:
        try:
            with Unit(unit_name.encode(), _autoload=True) as unit:
                method = getattr(unit.Unit, action)
                method(b"replace")
                return True
        except Exception as e:
            Logger.error(f"Systemd start failed: {e}", True)
            return False

    def _is_active_sync(self, unit_name: str) -> bool:
        try:
            with Unit(unit_name.encode(), _autoload=True) as unit:
                return unit.Unit.ActiveState == b"active"
        except Exception as e:
            Logger.error(f"Systemd status failed: {e}", True)
            return False

    def _list_active_sync(self, pattern: str) -> List[str]:
        try:
            with Manager() as manager:
                manager.load()
                units = manager.Manager.ListUnits()
                b_pattern = pattern.encode()

            return [
                u[0].decode()
                for u in units
                if u[0].startswith(b_pattern) and u[3] == b"active"
            ]
        except Exception as e:
            Logger.error(f"Systemd list actives failed: {e}", True)
            return []
