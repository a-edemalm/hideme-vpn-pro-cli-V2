from typing import List, Set

from core.dtos import Server
from services.config_service import ConfigService


async def enrich_favorites(
    servers: List[Server], config_service: ConfigService
) -> None:
    "Cross-references the live server list with saved favorites"
    favorites = await config_service.get_favorites()
    favorites_ids: Set[int] = {f.ID for f in favorites}

    for server in servers:
        server.IS_FAVORITE = server.ID in favorites_ids


def enrich_latency(servers: List[Server]) -> None:
    pass
