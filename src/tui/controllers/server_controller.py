from typing import List

from core import converters, enrichers
from core.dtos import Server
from src.tui.interfaces import AppInterface


class ServerController:
    """
    Controller handling business logic for server retrieval and connection states.
    """

    def __init__(self, app: AppInterface):
        """
        Initialize the controller with application services.

        :param self: Instance reference
        :param app: Main application interface for service access
        """
        self.app = app

    async def load_servers(self) -> List[Server]:
        """
        Fetches, sorts, and pushes data to the UI.

        :param self: Instance reference
        """

        raw_dto = await self.app.vpn_service.fetch_servers()

        live_servers = [converters.server_dto_to_server(dto) for dto in raw_dto]

        await enrichers.enrich_favorites(live_servers, self.app.conf_ser)

        return live_servers

    async def load_servers_favorite(self) -> List[Server]:

        all_servers = await self.load_servers()

        return [s for s in all_servers if s.IS_FAVORITE]

    async def connect_to(self, server: Server) -> bool:
        """
        Initiates a connection to the specified server and notifies the UI.

        :param self: Instance reference
        :param server: Server object to connect to
        """
        recent_connection = converters.server_to_recent_dto(server)

        await self.app.conf_ser.save_recent_connecetion(recent_connection)

        return await self.app.vpn_service.connect(server)

    async def toggle_favorite(self, server: Server) -> bool:
        """
        Toggles server, and returns status.
        """

        server.IS_FAVORITE = not server.IS_FAVORITE

        current_favs = await self.app.conf_ser.get_favorites()

        if server.IS_FAVORITE:
            current_favs.append(converters.server_to_favorite_dto(server))
        else:
            current_favs = [f for f in current_favs if f.ID != server.ID]

        await self.app.conf_ser.save_favorites(current_favs)

        return server.IS_FAVORITE
