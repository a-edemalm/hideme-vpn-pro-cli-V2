from rich.table import Table
from textual import on
from textual.widgets import OptionList
from textual.message import Message
from src.models.server import Server

class ServerList(OptionList):
    """
    Custom OptionList that maps Server objects to UI rows.
    Featuering DEFAULT CSS.
    """

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

    ServerList,
    ServerList:focus {
        background: $bg-dark;
        height: 1fr;
        scrollbar-gutter: stable;
        border: none;
    }

    ServerList .option-list--option {
        padding: 0 1; 
        background: $bg-dark;
        color: $text-main;
        border: none;
    }

    ServerList .option-list--option-hover {
        padding: 0 1;
        background: $bg-select;
        color: $accent;
        border: none;
    }

    ServerList > .option-list--option-highlighted,
    ServerList:focus > .option-list--option-highlighted,
    ServerList > .option-list--option-selected {
        padding: 0 1;
        background: $accent;
        color: $bg-dark;
        text-style: bold;
        border: none;
    }
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the server list component.

        :param self: Instance reference
        :param args: Positional arguments for OptionaList
        :param kwargs: Keyword arguments for OptionalList
        """
        super().__init__(*args, **kwargs)
        self.servers: list[Server] = []

    def _build_row(self, server: Server) -> Table:
        """
        Formats a server object into, rich table row.

        :param self: Instance reference
        :param server: The server to format
        
        """
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(server.DISPLAY_NAME, f" - {server.COUNTRY_CODE}")
        return grid
    
    def populate(self, servers: list[Server]) -> None:
        """
        Clears the list and fills it with new server data.

        :param self: Instance reference
        :param servers: Collection of server objects
        """
        self.servers = servers
        with self.app.batch_update():
            self.clear_options()
            self.add_options([self._build_row(s) for s in servers])

    @on(OptionList.OptionSelected)
    def server_selected(self, event: OptionList.OptionSelected) -> None:
        """
        Enter/Click event and broadcasts the selected server.

        :param self: Instance reference
        :param event: The selection event from Textual
        """
        event.stop()
        if self.servers:
            server = self.servers[event.option_index]
            self.post_message(self.ServerSelected(server))

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

