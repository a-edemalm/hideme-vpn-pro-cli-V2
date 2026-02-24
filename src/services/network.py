import asyncio
from pathlib import Path

from src.core.interfaces import INetworkMonitor
from src.utils.logger import Logger


class NetworkService(INetworkMonitor):
    """Detects VPN interfaces via the Linux filesystem directly."""

    _TUNNEL = "vpn"
    _UP_STATES = ["up", "unknown"]
    _SYS_NET_PATH = Path("/sys/class/net")

    async def is_tunnel_interface(self) -> bool:
        return await asyncio.to_thread(self._is_tunnel_interface_sync)

    def _is_tunnel_interface_sync(self) -> bool:
        """
        Scans /sys/class/net to find virtual tunnels.
        """
        prefixes = ("tun", self._TUNNEL)

        try:
            for iface in self._SYS_NET_PATH.iterdir():
                if not iface.name.startswith(prefixes):
                    continue

                file = iface / "opperstate"
                if not file.is_file():
                    continue

                status = file.read_text().strip().lower()
                if status in self._UP_STATES:
                    return True

        except Exception as e:
            Logger.warning(
                f"Unexpected error, failed retrieving tunnel interface: {e}", True
            )
            return False

        return False
