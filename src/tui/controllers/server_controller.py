from src.tui.interfaces import AppInterface, ScreenInterface
from src.models.server import Server

class ServerController:
    """
    Controller handling business logic for server retrieval and connection states.
    """
    
    def __init__(self, app: AppInterface):
        """
        Initialize the controller with application services. 

        :param self: Instance reference
        :param app: Main application interface for service access
        """
        self.app = app

    def load_servers(self, screen: ScreenInterface) -> None:
        """
        Fetches, sorts, and pushes data to the UI.

        :param self: Instance reference
        :param screen: Screen interface to recieve the updated server list
        """
        # Retrievs raw server data
        servers = self.app.vpn_service.fetch_servers()

        # Sorts aplhabetically, by name
        sorted_servers = sorted(servers, key=lambda x: x.DISPLAY_NAME)

        # Thread-safe UI update, call to main thread
        self.app.call_from_thread(screen.update_list, sorted_servers)

    def connect_to(self, server: Server) -> None:
        """
        Initiates a connection to the specified server and notifies the UI.

        :param self: Instance reference
        :param server: Server object to connect to
        """
        if self.app.vpn_service.connect(server):
            self.app.notify(f"The vpn connected successfully.", title="Connected", severity="information")
        else:
            self.app.notify(f"The vpn failed to connect.", title="Connection Failed", severity="error")
