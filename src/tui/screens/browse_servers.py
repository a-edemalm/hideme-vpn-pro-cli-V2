from typing import cast
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, OptionList, Label, Button
from tui.widgets.nordic_logo import NordicLogo
from tui.constants import ElementID
from tui.controllers.server_controller import ServerController
from tui.widgets.ServerList import ServerList
from tui.interfaces import AppInterface
from models.server import Server
from utils.logger import Logger


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
            # Sidebar
            with Container(id=ElementID.CNR_SIDEBAR.id):
                # Logo
                yield NordicLogo()
                # Sub-title
                yield Label(ElementID.LBL_LIST_TITLE.title, 
                            id=ElementID.LBL_LIST_TITLE.id
                            )
                # Server List
                yield ServerList(id=ElementID.LIST_SERVER.id)

            # Main panel
            with Container(id=ElementID.CNR_MAIN.id): 
                # Sub-title
                yield Label(ElementID.LBL_SERVER_DETAILS.title,
                            id=ElementID.LBL_SERVER_DETAILS.id 
                            )
                # Server details
                yield Label(ElementID.LBL_DETAILS_MSG.title, 
                            id=ElementID.LBL_DETAILS_MSG.id
                            )
                # Menu frame
                with Container(classes=ElementID.CNR_MENU_CARD.clazz):
                    # Actions
                    yield Button(ElementID.BTN_CONNECT.title, 
                                 id=ElementID.BTN_CONNECT.id, 
                                 classes=ElementID.BTN_CONNECT.clazz
                                 )
                    yield Button(ElementID.BTN_FAV_ADD.title,
                                 id=ElementID.BTN_FAV_ADD.id)
                    yield Button(ElementID.BTN_RETURN.title, 
                                 id=ElementID.BTN_RETURN.id
                                 )
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
        self.details_label = self.query_one(f"#{ElementID.LBL_DETAILS_MSG.id}", Label)
        self.server_list = self.query_one(f"#{ElementID.LIST_SERVER.id}", ServerList)

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
            f"Location:  {self.selected_server.CITY}, {self.selected_server.COUNTRY_CODE}\n"
            f"Continent: {self.selected_server.CONTINENT}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Button interaction logic and routing.

        :param self: Instance reference
        :param event: Button click event data
        """
        btn_id = event.button.id # Clicked button event-id

        # Route actions
        match btn_id:
            case ElementID.BTN_RETURN.id: # back to main-screen
                self.app.pop_screen() 
            case ElementID.BTN_CONNECT.id: # VPN CONNECT
                server = self.selected_server

                if server is not None:
                    # Offloading for the vpn to establisg a connection
                    self.run_worker(lambda: self.controller.connect_to(server), thread=True, exclusive=True)
                else:
                    self.notify("Please select a server first!", severity="error")
            case _:
                Logger.error("Unknown button pressed.")
    
