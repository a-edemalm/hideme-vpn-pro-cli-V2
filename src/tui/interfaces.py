from abc import abstractmethod
from typing import Protocol, List, Any
from src.models.server import Server

class AppInterface(Protocol):
    """
    Defines core application functionality for controllers
    """
    vpn_service: Any

    @abstractmethod
    def call_from_thread(self, callback: Any, *args: Any) -> None: 
        """
        Executes a function on the main TUI thread safely

        :param self: Instance reference
        :param callback: The function to be executed
        :param args: Arguments passed to the callback function
        """
        ...
        

    @abstractmethod
    def notify(self, message: str, title: str = "", severity: str = "information") -> None:
        """
        Displays a notification toast in the UI
        
        :param self: Instance reference
        :param message: The text body of the notification
        :param title: Optional headline for the toast
        :param severity: Log level (information, warning, or error)
        """
        ...

class ScreenInterface(Protocol):
    """
    Default interface for screens, displaying ui. 
    """
    @abstractmethod
    def update_list(self, servers: List[Server]) -> None: 
        """
        Updates the server list widget with the new data

        :param self: Instance reference
        :param servers: List of Server objects to dsiplay
        """
        ...
        
