from typing import cast

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Mount, ScreenResume, ScreenSuspend
from textual.screen import Screen
from textual.widgets import Button, Footer, Header

from tui.controllers.main_controller import MainController
from tui.interfaces import AppInterface
from tui.widgets.ip_check import IpCheckWidget
from tui.widgets.nordic_logo import NordicLogo


class MainMenu(Screen):
    """
    Primary navigation dashboard, main menu for the application.
    """

    app_ref: AppInterface

    # --- LAYOUT ---

    def compose(self) -> ComposeResult:
        """
        Defines the visual layout

        :param self: Instance reference
        """
        yield Header(show_clock=False)

        with Horizontal():
            # Sidebar
            with Container(id="sidebar"):
                # Logo
                yield NordicLogo()
                # Ip check
                yield IpCheckWidget()

            # Main panel
            with Container(id="main-panel"):
                # Menu frame
                with Container(classes="menu-card"):
                    # Actions
                    yield Button(
                        "Quick Connect", id="btn-q-connect", classes="btn-connect"
                    )
                    yield Button("Browse Servers", id="btn-browse")
                    yield Button("Favorites", id="btn-favorites")
                    yield Button(
                        "Disconnect", id="btn-disconnect", classes="btn-disconnect"
                    )
                    yield Button("Exit", id="btn-exit")

            yield Footer()

    # --- SCREEN STATES ---

    @on(Mount)
    async def handle_mount(self) -> None:
        """Initializes screen and controller"""
        self.app_ref = cast(AppInterface, self.app)
        self.controller = MainController(self.app_ref)

        # Cache freq. accessed widgets
        self.app_ref.ip_check = self.query_one(IpCheckWidget)

    @on(ScreenResume)
    def handle_resume(self) -> None:
        """Refresh data on resume"""
        # Accessed widgets
        self.app_ref.ip_check.visible = True

    @on(ScreenSuspend)
    def handle_suspend(self) -> None:
        """Clean screen state on leave"""
        # Accessed widgets
        self.app_ref.ip_check.reset_details()

    # --- UI INTERACTION --

    # --- on BUTTON Press ---

    @on(Button.Pressed, "#btn-q-connect")
    def handle_quick_connect(self) -> None:
        """Handle qucik connection button"""
        self._run_quick_connect()

    @on(Button.Pressed, "#btn-disconnect")
    def handle_disconnect(self) -> None:
        """Handle disconnection button"""
        self._run_disconnect()

    # --- NAVIGATION ---

    @on(Button.Pressed, "#btn-browse")
    def handle_browse(self) -> None:
        """Handle navigation to the screen browse all servers."""
        self.app.push_screen("browse_servers")

    @on(Button.Pressed, "#btn-favorites")
    def handle_favorites(self) -> None:
        """Handle navigation to the screen favorites browser."""
        self.app.push_screen("browse_servers_fav")

    @on(Button.Pressed, "#btn-exit")
    def handle_exit(self) -> None:
        """Terminates the application."""
        self.app.exit()

    # --- BACKGROUND TASKS ---

    @work(exclusive=True)
    async def _run_quick_connect(self) -> None:
        """Execute quick connection, most recent server"""
        if await self.controller.connect_quick():
            self.notify("VPN Connected", title="Quick Connect")
            self.app_ref.trigger_ip_refresh()
        else:
            self.notify("No recent server found", severity="warning")

    @work(exclusive=True)
    async def _run_disconnect(self) -> None:
        """Execute disconnection"""
        if await self.controller.disconnect():
            self.notify("VPN Disconnected")
            self.app_ref.trigger_ip_refresh()
