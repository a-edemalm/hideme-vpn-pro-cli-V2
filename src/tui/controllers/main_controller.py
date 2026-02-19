from tui.interfaces import AppInterface


class MainController:
    """
    Controller handling business logic for server retrieval and connection states.
    """
    def __init__(self, app: AppInterface):
        """
        Initialize the controller with application services.

        :param self: Instance reference
        :param app: Application interface for service access
        """
        self.app = app

    def disconnect(self) -> None:
        """
        Terminates active VPN session and notifies user. 

        :param self: Instance reference
        """
        if self.app.vpn_service.disconnect():
            self.app.notify(f"The vpn has successfully disconnect.", title="Disconnected", severity="information")
        else:
            self.app.notify(f"The vpn failed to disconnect.", title="Failed to disconnect", severity="information")