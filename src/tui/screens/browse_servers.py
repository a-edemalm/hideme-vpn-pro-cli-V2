from typing import cast
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, OptionList, Label, Button
from src.tui.widgets.nordic_logo import NordicLogo
from tui.controllers.server_controller import ServerController
from tui.widgets.ServerList import ServerList
from tui.interfaces import AppInterface
from src.models.server import Server


class BrowseServers(Screen): 

    controller: ServerController 
    selected_server: Server | None = None

    def compose(self) -> ComposeResult:
        """
        Defines the visual layout

        :param self: Instance reference
        """
        yield Header(show_clock=True) 

        with Horizontal(): # Main layout

            with Container(id="sidebar"): # Sidebar
                # Logo
                yield NordicLogo()
                # Sub-title
                yield Label("SERVERS", id="list-title")
                # Server List
                yield ServerList(id="server-list")

            with Container(id="main-panel"): # Main panel
                # Sub-title
                yield Label("SERVER DETAILS", id="details-title")
                # Server details
                yield Label("Select a server to see options.", id="details-msg")
                # Menu frame
                with Container(classes="menu-card"):
                    # Actions
                    yield Button("Connect", id="btn-connect-selected", classes="btn-connect")
                    yield Button("Add Favorite", id="btn-fav-selected")
                    yield Button("Back to Menu", id="btn-back")

            yield Footer()

    def on_mount(self) -> None:
        """
        Initializes the screen controller on mount.
        Additionally, starts background server fetch.

        :param self: Instance reference
        """
        app_ref = cast(AppInterface, self.app) # Type-cast, to access shared services
        self.controller = ServerController(app_ref)   

        # Offloading, fetching of servers list
        self.run_worker(lambda: self.controller.load_servers(self), thread=True, exclusive=True)

        # Cache freq. accessed widgets
        self.details_label = self.query_one("#details-msg", Label)
        self.server_list = self.query_one("#server-list", ServerList)

    def update_list(self, servers: list[Server]) -> None:
        """
        UI Callback used by the controller to populate the list

        :param self: Instance reference
        :param servers: List of Server objects to display 
        """
        self.server_list.populate(servers)

    @on(ServerList.ServerSelected)
    def on_list_server_selected(self, event: ServerList.ServerSelected) -> None:
        """
        Updates the detail view when a new server is selected.

        :param self: Instance reference
        :param event: Custom selection event contains the server object
        """
        self.selected_server = event.server
        
        self.details_label.update( # Update details panel
            f"Targeting: {self.selected_server.DISPLAY_NAME}\n"
            f"Location: {self.selected_server.CITY}, {self.selected_server.COUNTRY_CODE}\n"
            f"Continent: {self.selected_server.CONTINENT}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Button interaction logic and routing.

        :param self: Instance reference
        :param event: Button click event data
        """
        btn_id = event.button.id # Clicked button event-id

        if btn_id == "btn-back": # Route actions
            self.app.pop_screen() # back to main-screen

        elif btn_id == "btn-connect-selected":
            server = self.selected_server

            if server is not None:
                # Offloading for the vpn to establisg a connection
                self.run_worker(lambda: self.controller.connect_to(server), thread=True, exclusive=True)
            else:
                self.notify("Please select a server first!", severity="error")
        
    
