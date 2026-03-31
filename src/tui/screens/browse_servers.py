from typing import cast

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Mount, ScreenResume, ScreenSuspend
from textual.screen import Screen  # Correct import
from textual.widgets import Button, Footer, Header

from core.dtos import Server
from tui.controllers.server_controller import ServerController
from tui.interfaces import AppInterface
from tui.widgets.favorite_button import FavoriteButton
from tui.widgets.nordic_logo import NordicLogo
from tui.widgets.server_details_widget import ServerDetailsWidget
from tui.widgets.ServerList import ServerListWidget


class BrowseAllServers(Screen):
    app_ref: AppInterface
    controller: ServerController
    selected_server: Server | None = None
    fav_button: FavoriteButton

    # --- LAYOUT ---

    def compose(self) -> ComposeResult:

        yield Header(show_clock=False)

        with Horizontal():
            # Sidebar
            with Container(id="sidebar"):
                # Logo
                yield NordicLogo()
                # Server List
                yield ServerListWidget()

            # Main Panel
            with Container(id="main-panel"):
                # ServerDetails
                yield ServerDetailsWidget()
                # Menu frame
                with Container(classes="menu-card"):
                    # actions
                    yield Button("Connect", id="btn-connect", classes="btn-connect")
                    yield FavoriteButton(id="btn-favorite")
                    yield Button("Back to Menu", id="btn-return")
        yield Footer()

    # --- SCRREN STATES ---

    @on(Mount)
    def on_mount(self) -> None:
        """Initializes screen and controller"""
        self.app_ref = cast(
            AppInterface, self.app
        )  # Type-cast, to access shared services
        self.controller = ServerController(self.app_ref)

        # Cache freq. accessed widgets
        self.server_list = self.query_one(ServerListWidget)
        self.details_label = self.query_one(ServerDetailsWidget)
        self.fav_button = self.query_one(FavoriteButton)

    @on(ScreenResume)
    def handle_resume(self, event: ScreenResume) -> None:
        """Refresh data on resume"""
        self._run_refresh_data()

        # Accessed widgets
        self.details_label.display = True
        self.fav_button.display = False

    @on(ScreenSuspend)
    def handle_suspend(self, event: ScreenSuspend) -> None:
        """Clean screen state on leave"""
        self.selected_server = None

        # Reset widgets
        self.server_list.reset_list()
        self.details_label.reset_details()

    # --- UI INTERACTION ---

    @on(ServerListWidget.ServerSelected)
    def handle_selection(self, event: ServerListWidget.ServerSelected) -> None:
        """
        Update UI with selection
        :param event: Selection event containing server object
        """
        self.selected_server = event.server

        self.details_label.display = True
        self.details_label.selected_server = self.selected_server

        self.fav_button.server = self.selected_server
        self.fav_button.is_favorite = self.selected_server.IS_FAVORITE
        self.fav_button.display = True

    @on(FavoriteButton.ToggleRequest)
    def on_favorite_toggled(self, event: FavoriteButton.ToggleRequest) -> None:
        """
        Forward toggle request
        :param event: Request event containing server object
        """
        self._run_toggle_favorite(event.server)

    # --- on BUTTON Press ---

    @on(Button.Pressed, "#btn-connect")
    def on_connect_pressed(self, event: Button.Pressed) -> None:
        """Handle connection button"""
        if not self.selected_server:
            return

        self._run_connect(self.selected_server)

    # --- NAVIGATION ---

    @on(Button.Pressed, "#btn-return")
    def on_return_pressed(self, event: Button.Pressed) -> None:
        """Back to menu"""
        self.app.pop_screen()

    # --- BACKGROUND TASKS ---

    @work(exclusive=True)  # PREVENTS SPAM CLICKING
    async def _run_refresh_data(self) -> None:
        """Reload all servers"""
        self.server_list.servers = await self.controller.load_servers()

    @work(exclusive=True)  # PREVENTS SPAM CLICKING
    async def _run_connect(self, server: Server) -> None:
        """
        Execute connection
        :param server: Server to connect to
        """
        is_connected = await self.controller.connect_to(server)

        if is_connected:
            self.notify(
                "The VPN is connected.", title="VPN Online", severity="information"
            )
            self.app_ref.ip_check.refresh_details()
        else:
            self.notify(
                "The VPN failed to connect.", title="VPN Failed", severity="error"
            )

    @work(exclusive=True)
    async def _run_toggle_favorite(self, server: Server) -> None:
        """
        Process server favorite toggle
        :param server: Server object to toggle
        """
        is_now_fav = await self.controller.toggle_favorite(server)
        self.fav_button.is_favorite = is_now_fav
        status = "Added to" if is_now_fav else "Removed from"
        self.notify(f"{status} favorites.")
