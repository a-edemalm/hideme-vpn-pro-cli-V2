from abc import ABC, abstractmethod
from typing import List, Optional

from core.dtos import IpCheckDto, ServerDto


class IServiceManager(ABC):
    """
    Interface for service management system.
    """

    @abstractmethod
    async def start(self, unit_name: str) -> bool: ...

    @abstractmethod
    async def stop(self, unit_name: str) -> bool: ...

    @abstractmethod
    async def is_active(self, unit_name: str) -> bool: ...

    @abstractmethod
    async def list_active(self, pattern: str) -> List[str]: ...


class INetworkMonitor(ABC):
    """
    Interface for checking network state.
    """

    @abstractmethod
    async def is_tunnel_interface(self) -> bool: ...


class IVpnProvider(ABC):
    """
    Interface for VPN provider.
    """

    @abstractmethod
    async def fetch_servers(self) -> List[ServerDto]: ...

    @abstractmethod
    async def connect(self, server: ServerDto) -> bool: ...

    @abstractmethod
    async def disconnect(self) -> bool: ...

    @abstractmethod
    async def get_connectivity(self) -> Optional[IpCheckDto]: ...

    @abstractmethod
    async def is_connected(self) -> bool: ...
