from typing import cast
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Label
from textual.containers import Container, Horizontal
from src.tui.widgets.nordic_logo import NordicLogo
from tui.controllers.main_controller import MainController
from tui.interfaces import AppInterface

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
            
            with Container(id="sidebar"): # Sidebar
                # Logo
                yield NordicLogo()

            with Container(id="main-panel"): # Main panel
                # Menu frame
                with Container(classes="menu-card"):
                    # Actions
                    yield Button("Quick Connect", id="btn-q-connect", classes="btn-connect")
                    yield Button("Browse Servers", id="btn-browse")
                    yield Button("Favorites", id="btn-fav")
                    yield Button("Disconnect", id="btn-disconnect", classes="btn-disconnect")
                    yield Button("Exit", id="btn-exit", classes="btn-exit")

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

        if btn_id == "btn-exit": # Route actions
            self.app.exit()

        elif btn_id == "btn-browse":
            self.app.push_screen("browse")

        elif btn_id =="btn-q-connect":
            self.notify("Connecting...", severity="information")
        
        elif btn_id == "btn-disconnect":
            # Offloading for the vpn to disconnect
            self.run_worker(lambda: self.controller.disconnect(), thread=True, exclusive=True)
        