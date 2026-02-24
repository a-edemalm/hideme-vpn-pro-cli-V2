import asyncio
import json
import os
from enum import Enum
from typing import Any, Dict, List, Union

from utils.logger import Logger


class ConfigSection(str, Enum):
    """Sections in config.json"""

    FAVORITES = "favorites"
    RECENT_CONNECTION = "recent_connection"
    NETWORK = "network_settings"


class ConfigManager:
    _file_name = "config.json"

    def __init__(self):

        curr_dir = os.path.dirname(os.path.abspath(__file__))

        resource_dir = os.path.join(curr_dir, "..", "resources")

        self._file_path = os.path.join(resource_dir, self._file_name)

        os.makedirs(resource_dir, exist_ok=True)

    # --- ASYNC CALLS ---
    async def read(self, section: ConfigSection) -> Dict[str, Any]:
        return await asyncio.to_thread(self._prepare_read_sync, section)

    async def write(
        self, section: ConfigSection, data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> bool:
        return await asyncio.to_thread(self._prepare_write_sync, section, data)

    # --- SYNC"PREPARE" METHODS ---
    def _prepare_read_sync(self, section: ConfigSection) -> Dict[str, Any]:
        """Returns raw dict. The caller uses converters to get a DTO."""
        full_config = self._load_file_sync()
        return full_config.get(section.value, {})

    def _prepare_write_sync(
        self, section: ConfigSection, data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> bool:
        """Takes a RAW DICT (already converted) and saves it."""
        full_config = self._load_file_sync()
        full_config[section.value] = data
        return self._save_file_sync(full_config)

    # --- SYNC PRIVATE METHODS ---
    def _load_file_sync(self) -> Dict[str, Any]:
        if not os.path.exists(self._file_path):
            return {}

        try:
            with open(self._file_path, "r") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, ValueError):
            return {}

    def _save_file_sync(self, data: Dict[str, Any]) -> bool:
        try:
            with open(self._file_path, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except OSError as e:
            Logger.error(f"Failed to save to disk, could not save config: {e}")
            return False
