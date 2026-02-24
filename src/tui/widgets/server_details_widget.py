from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Static

from core.dtos import Server


class ServerDetailsWidget(Widget):
    selected_server: reactive[Server | None] = reactive(None)

    def compose(self) -> ComposeResult:
        yield Label(" SERVER DETAILS ", id="details-header")
        yield Static("Select a server to see details.", id="details-body")

    def on_mount(self) -> None:
        self._body = self.query_one("#details-body", Static)

        if self.selected_server:
            self._update_ui(self.selected_server)

    def watch_selected_server(self, server: Server | None) -> None:
        if self.is_mounted:
            self._update_ui(server)

    def _update_ui(self, server: Server | None) -> None:
        if server:
            self._body.update(
                f"[b]NAME:[/b] {server.COUNTRY}\n"
                f"[b]LOCATION:[/b] {server.CITY}, {server.COUNTRY_CODE}\n"
                f"[b]CONTINENT:[/b] {server.CONTINENT}"
            )
        else:
            self._body.update("Select a server to see details.")

    def reset_details(self):
        self.selected_server = None
        self._update_ui(None)

    DEFAULT_CSS = """
    $bg-dark: #2E3440;       /* nord0 */
    $bg-card: #3B4252;       /* nord1 */
    $bg-select: #434C5E;     /* nord2 */
    $text-main: #ECEFF4;     /* nord6 */
    $text-dim: #4C566A;      /* nord3 */

    $accent: #88C0D0;        /* nord8 (Cyan) */
    $success: #A3BE8C;       /* nord14 (Green) */
    $warning: #EBCB8B;       /* nord13 (Yellow) */
    $error: #BF616A;         /* nord11 (Red) */

    ServerDetailsWidget {
        background: $bg-card;
        padding: 1 3; /* HEIGHT SIDES */
        height: 8;
        width: 50;
        margin: 1 0;
        layout: vertical
    }
    #details-header {
        color: $accent;
        text-style: bold;
        margin-bottom: 1;
        width: 100%;
        border-bottom: solid $accent;
        text-align: center;
    }
    #details-body {
        color: $text-main;
        height: auto;
    }
    """
