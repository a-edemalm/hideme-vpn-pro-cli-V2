from typing import cast

from textual import work
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.timer import Timer
from textual.widget import Widget
from textual.widgets import Label, Static

from core.dtos import IpCheckDto
from tui.interfaces import AppInterface


class IpCheckWidget(Widget):
    data: reactive[IpCheckDto | None] = reactive(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._refresh_timer: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Label("CONNECTION STATUS", id="ip-header")
        yield Static("", id="ip-body")

    def on_mount(self) -> None:
        self._body = self.query_one("#ip-body", Static)

        self._refresh_timer = self.set_interval(60, self.update_ip_info, pause=True)

    def on_show(self) -> None:
        if self._refresh_timer:
            self._refresh_timer.resume()

        if self.data is None:
            self.update_ip_info()

    def on_hide(self) -> None:
        if self._refresh_timer:
            self._refresh_timer.pause()

    @work(exclusive=True)
    async def update_ip_info(self) -> None:
        if not self.display:
            return

        app = cast(AppInterface, self.app)
        self.data = await app.vpn_service.get_connectivity()

    def watch_data(self, data: IpCheckDto | None) -> None:
        if self.is_mounted:
            self._update_ui(data)

    def _update_ui(self, data: IpCheckDto | None) -> None:
        if data:
            status = "CONNECTED" if data.IS_PROTECTED else "DISCONNECTED"

            self._body.update(
                f"[b]IP-ADRESS:[/b] {data.IP}\n"
                f"[b]LOCATION:[/b] {data.CITY} {data.COUNTRY_CODE}\n"
                f"[b]STATUS:[/b] {status}"
            )
        else:
            self._body.update("Checking connection status...")

    def reset_details(self) -> None:
        if self._refresh_timer:
            self._refresh_timer.pause()
        self.data = None
        self._update_ui(None)

    def refresh_details(self) -> None:
        self.reset_details()

        self.set_timer(6, self._trigger_delayed_update)

    def _trigger_delayed_update(self) -> None:
        if self._refresh_timer:
            self._refresh_timer.resume()
            self._refresh_timer.reset()

        self.update_ip_info()

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

    IpCheckWidget {
        background: $bg-card;
        padding: 1 3; /* HEIGHT SIDES */
        height: 8;
        width: 100%;
        margin: 1 0;
        layout: vertical
    }
    #ip-header {
        color: $accent;
        text-style: bold;
        margin-bottom: 1;
        width: 100%;
        border-bottom: solid $accent;
        text-align: center;
    }
    #ip-body {
        color: $text-main;
        height: auto;
    }
    """
