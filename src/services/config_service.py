from typing import List, Optional

from core import converters
from core.dtos import FavoriteDto, RecentConnectionDto
from services.config_manager import ConfigManager, ConfigSection


class ConfigService:
    def __init__(self, manager: ConfigManager):
        self._manager = manager

    # --- FAVORITES ---
    async def get_favorites(self) -> List[FavoriteDto]:
        raw_list = await self._manager.read(ConfigSection.FAVORITES)
        if not isinstance(raw_list, list):
            return []

        return [
            converters.dict_to_favorite_dto(item)
            for item in raw_list
            if isinstance(item, dict)
        ]

    async def save_favorites(self, dto: List[FavoriteDto]):
        raw_data = [converters.favorite_dto_to_dict(fav) for fav in dto]
        await self._manager.write(ConfigSection.FAVORITES, raw_data)

    # --- RECENT CONNECTION ---
    async def get_recent_connection(self) -> Optional[RecentConnectionDto]:
        raw_data = await self._manager.read(ConfigSection.RECENT_CONNECTION)
        if not raw_data:
            return None
        return converters.dict_to_recent_connnection(raw_data)

    async def save_recent_connecetion(self, dto: RecentConnectionDto):
        raw_data = converters.recent_connection_to_dict(dto)
        await self._manager.write(ConfigSection.RECENT_CONNECTION, raw_data)
