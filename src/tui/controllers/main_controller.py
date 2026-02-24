from typing import List

from core import converters, enrichers
from core.dtos import Server
from tui.interfaces import AppInterface


class MainController:
    """
    Controller handling business logic for server retrieval and connection states.
    """

    def __init__(self, app: AppInterface):
        """
        Initialize the controller with application services.

        :param self: Instance reference
        :param app: Application interface for service access
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

    async def connect_quick(self) -> bool:

        recent_dto = await self.app.conf_ser.get_recent_connection()

        if recent_dto is None:
            self.app.notify("No recent connections found.")
            return False

        all_servers = await self.load_servers()

        target_server = next((s for s in all_servers if s.ID == recent_dto.ID), None)

        if target_server:
            return await self.connect_to(target_server)

        return False

    async def connect_to(self, server: Server) -> bool:
        """
        Initiates a connection to the specified server and notifies the UI.

        :param self: Instance reference
        :param server: Server object to connect to
        """
        recent_connection = converters.server_to_recent_dto(server)

        await self.app.conf_ser.save_recent_connecetion(recent_connection)

        return await self.app.vpn_service.connect(server)

    async def disconnect(self) -> bool:
        """
        Terminates active VPN session and notifies user.

        :param self: Instance reference
        """
        return await self.app.vpn_service.disconnect()
