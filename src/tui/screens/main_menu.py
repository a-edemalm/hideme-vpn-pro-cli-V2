from typing import cast
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Label
from textual.containers import Container, Horizontal
from tui.widgets.nordic_logo import NordicLogo
from tui.controllers.main_controller import MainController
from tui.interfaces import AppInterface
from tui.constants import ElementID, ScreenID
from utils.logger import Logger

class MainMenu(Screen):
    """
    Primary navigation dashboard, main menu for the application.
    """
    
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
            # Main panel
            with Container(id=ElementID.CNR_MAIN.id):
                # Menu frame
                with Container(classes=ElementID.CNR_MENU_CARD.clazz):
                    # Actions
                    yield Button(ElementID.BTN_Q_CONNECT.title, 
                                 id=ElementID.BTN_Q_CONNECT.id, 
                                 classes=ElementID.BTN_Q_CONNECT.clazz
                                 )
                    yield Button(ElementID.BTN_BROWSE_SERVER.title, 
                                 id=ElementID.BTN_BROWSE_SERVER.id
                                 )
                    yield Button(ElementID.BTN_FAV_SERVER.title,
                                 id=ElementID.BTN_FAV_SERVER.id
                                 )
                    yield Button(ElementID.BTN_DISCONNECT.title,
                                 id=ElementID.BTN_DISCONNECT.id,
                                 classes=ElementID.BTN_DISCONNECT.clazz
                                 )
                    yield Button(ElementID.BTN_EXIT.title, 
                                 id=ElementID.BTN_EXIT.id,
                                 classes=ElementID.BTN_EXIT.clazz)

            yield Footer()

    def on_mount(self) -> None:
        """
        Initializes the screen controller on mount.

        :param self: Instance reference
        """
        app_ref = cast(AppInterface, self.app) # Type-cast, to access shared services
        self.controller = MainController(app_ref)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Button interaction logic and routing.

        :param self: Instance reference
        :param event: Button click event data
        """
        btn_id = event.button.id # clicked button event-id

        # Route actions
        match btn_id:
            case ElementID.BTN_EXIT.id: # back to main-screen
                self.app.exit() 
            case ElementID.BTN_BROWSE_SERVER.id: # Server-screen
                self.app.push_screen(ScreenID.BROWSE_SERVERS.id)
            case ElementID.BTN_Q_CONNECT.id: # VPN CONNECT
                self.notify("Connecting...", severity="information")
            case ElementID.BTN_DISCONNECT.id: # VPN DISCONNECT
                # Offloading for the vpn to disconnect
                self.run_worker(lambda: self.controller.disconnect(), thread=True, exclusive=True)
            case _:
                Logger.error("Unknown button pressed.")