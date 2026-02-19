from textual.app import App
from tui.screens.browse_servers import BrowseServers
from src.services.favorites_manager import FavoritesManager
from src.services.hide_me_service import HideMeService
from src.services.network import NetworkService
from src.services.systemd import SystemdManager
from src.tui.screens.main_menu import MainMenu
from src.utils.http_client import HttpClient


class AppShell(App):
    """
    Main application controller managing, services, state and screen routing.
    """

    # Global theme and layout configuration
    _STYLE_DIR = f"styles/"
    CSS_PATH = f"{_STYLE_DIR}main.tcss"

    
    SCREENS = { # Static screen registration
        "main": MainMenu,
        "browse": BrowseServers
    }

    def __init__(self):
        super().__init__()

        self.http_client = HttpClient()
        self.sys_mgr = SystemdManager()
        self.net_mon = NetworkService()
        self.fav_mgr = FavoritesManager()

        # VPN backend initialization with injected dependencies
        self.vpn_service = HideMeService(
            self.sys_mgr, 
            self.net_mon, 
            self.http_client
        )

    def on_mount(self) -> None: 
        """
        Loads the main menu screen.
        
        :param self: Instance reference
        """
        self.push_screen("main")

    def on_unmount(self) -> None:
        self.http_client.close()

    def action_show_main(self) -> None:
        """
        Global navigation action to pop the current screen and return to main.
        
        :param self: Instance reference
        """
        if len(self.screen_stack) > 1:
            self.pop_screen()
    