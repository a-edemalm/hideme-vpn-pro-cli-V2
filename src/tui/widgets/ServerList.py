from rich.table import Table
from textual import on
from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, OptionList

from core.dtos import Server


class ServerListWidget(Widget):
    """
    Custom OptionList that maps Server objects to UI rows.
    Featuering DEFAULT CSS.
    """

    servers: reactive[list[Server]] = reactive(list, always_update=True)

    class ServerSelected(Message):
        """
        POST message emitted when a server is picked from the list.
        """

        def __init__(self, server: Server) -> None:
            """
            Initialize the selection message.

            :param self: Instance reference
            :param server: The server object being passed
            """
            self.server = server
            super().__init__()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._list_view: OptionList | None = None

    def compose(self) -> ComposeResult:
        yield Label(" Server List ", id="list-header")
        yield OptionList(id="server-list")

    def on_mount(self) -> None:
        self._op_list = self.query_one("#server-list", OptionList)

        if self.servers:
            self._update_ui(self.servers)

    def watch_servers(self, new_servers: list[Server]) -> None:
        """
        Clears the list and fills it with new server data.

        :param self: Instance reference
        :param servers: Collection of server objects
        """
        if self.is_mounted:
            self._update_ui(new_servers)

    def _update_ui(self, new_servers: list[Server]) -> None:

        if not self._op_list:
            return

        with self.app.batch_update():
            # clear op_list
            self._op_list.clear_options()
            # add servers
            self._op_list.add_options([self._build_row(s) for s in new_servers])

    def _build_row(self, server: Server) -> Table:
        """
        Formats a server object into, rich table row.

        :param self: Instance reference
        :param server: The server to format

        """
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(server.COUNTRY, f" - {server.COUNTRY_CODE}")
        return grid

    @on(OptionList.OptionSelected, "#server-list")
    def _on_selection(self, event: OptionList.OptionSelected) -> None:
        """
        Enter/Click event and broadcasts the selected server.

        :param self: Instance reference
        :param event: The selection event from Textual
        """
        event.stop()
        try:
            selected_server = self.servers[event.option_index]
            self.post_message(self.ServerSelected(selected_server))
        except IndexError:
            pass

    def reset_list(self) -> None:
        self.servers = []

        if hasattr(self, "_op_list") and self._op_list:
            self._op_list.highlighted = None
            self._op_list.clear_options()
            self._op_list

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

    ServerListWidget {
        layout: vertical;
        background: $bg-dark;
    }

    #list-header {
        color: $accent;
        text-style: bold;
        margin: 1 0;
        width: 100%;
        border-bottom: solid $accent;
        text-align: center;
    }
    
    #server-list {
        background: $bg-dark;
        height: 1fr;
        scrollbar-gutter: stable;
        border: none;
    }

    #server-list:focus {
        background: $bg-dark;
        height: 1fr;
        scrollbar-gutter: stable;
        border: none;
    }

    #server-list .option-list--option {
        padding: 0 1; 
        background: $bg-dark;
        color: $text-main;
        border: none;
    }

    #server-list .option-list--option-hover {
        padding: 0 1;
        background: $bg-select;
        color: $accent;
        border: none;
    }

    #server-list > .option-list--option-highlighted,
    #server-list:focus > .option-list--option-highlighted,
    #server-list > .option-list--option-selected {
        padding: 0 1;
        background: $accent;
        color: $bg-dark;
        text-style: bold;
        border: none;
    }
    """
