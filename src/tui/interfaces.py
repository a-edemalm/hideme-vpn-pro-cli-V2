from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from services.config_manager import ConfigManager
    from services.config_service import ConfigService
    from tui.widgets.ip_check import IpCheckWidget


class AppInterface(Protocol):
    """
    Defines core application functionality for controllers
    """

    vpn_service: Any
    conf_mgr: "ConfigManager"
    conf_ser: "ConfigService"
    ip_check: "IpCheckWidget"

    @abstractmethod
    def notify(
        self, message: str, title: str = "", severity: str = "information"
    ) -> None:
        """
        Displays a notification toast in the UI

        :param self: Instance reference
        :param message: The text body of the notification
        :param title: Optional headline for the toast
        :param severity: Log level (information, warning, or error)
        """
        ...

    @abstractmethod
    def trigger_ip_refresh(self) -> None: ...
