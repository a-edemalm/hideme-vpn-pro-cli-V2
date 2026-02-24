from textual.app import App

from services.config_manager import ConfigManager
from services.config_service import ConfigService
from services.hide_me_service import HideMeService
from services.network import NetworkService
from services.systemd import SystemdManager
from tui.screens.browse_favorites import BrowseFavorites
from tui.screens.browse_servers import BrowseAllServers
from tui.screens.main_menu import MainMenu
from tui.widgets.ip_check import IpCheckWidget
from utils.http_client import HttpClient


class AppShell(App):
    """
    Main application controller managing, services, state and screen routing.
    """

    # Global theme and layout configuration
    _STYLE_DIR = "styles/"
    CSS_PATH = f"{_STYLE_DIR}main.tcss"

    SCREENS = {  # Static screen registration
        "main": MainMenu,
        "browse_servers": BrowseAllServers,
        "browse_servers_fav": BrowseFavorites,
    }

    def __init__(self):
        super().__init__()

        self.sys_mgr = SystemdManager()
        self.net_mon = NetworkService()
        self.http_client = HttpClient()

        self.conf_mgr = ConfigManager()
        self.conf_ser = ConfigService(self.conf_mgr)

        # VPN backend initialization with injected dependencies
        self.vpn_service = HideMeService(self.sys_mgr, self.net_mon, self.http_client)

        self.ip_check: IpCheckWidget | None = None

    def on_mount(self) -> None:
        """
        Loads the main menu screen.

        :param self: Instance reference
        """
        self.push_screen("main")

    async def on_unmount(self) -> None:
        await self.http_client.close()

    def action_show_main(self) -> None:
        """
        Global navigation action to pop the current screen and return to main.

        :param self: Instance reference
        """
        if len(self.screen_stack) > 1:
            self.pop_screen()

    def trigger_ip_refresh(self) -> None:
        if self.ip_check:
            self.ip_check.refresh_details()
