from abc import ABC, abstractmethod
from typing import List, Optional
from models.connection_info import ConnectionInfo
from src.models.server import Server

class IServiceManager(ABC):
    """
    Interface for service management system
    """
    @abstractmethod
    def start(self, unit_name: str) -> bool: ...

    @abstractmethod
    def stop(self, unit_name: str) -> bool: ...

    @abstractmethod
    def is_active(self, unit_name: str) -> bool: ...

    @abstractmethod 
    def list_active(self, pattern: str) -> List[str]: ...

class INetworkMonitor(ABC):
    """
    Interface for checking network state.
    """
    @abstractmethod
    def is_tunnel_interface(self) -> bool: ...

class IVpnProvider(ABC):
    """
    Interface for VPN provider
    """
    @abstractmethod
    def fetch_servers(self) -> List[Server]: ...

    @abstractmethod
    def connect(self, server: Server) -> bool: ...

    @abstractmethod
    def disconnect(self) -> bool: ...

    @abstractmethod
    def get_connectivity(self) -> Optional[ConnectionInfo]: ...

    @abstractmethod
    def is_connected(self) -> bool: ...
