import time
from typing import Any, Dict

from core.dtos import FavoriteDto, IpCheckDto, RecentConnectionDto, Server, ServerDto


def _validate_id(id_val: Any) -> int:
    """Shared helper for ID validation"""
    if not isinstance(id_val, int):
        raise ValueError(f"Invalid ID: {id_val}")
    return id_val


# DICT(DICTOINARY)
# DTO(DATA TRANSFER OBJECT)

# --- RAW DICT TO DTOs---


def dict_to_server_dto(data: Dict[str, Any]) -> ServerDto:
    valid_id = _validate_id(data.get("id"))
    geo = data.get("geo", {})

    return ServerDto(
        ID=valid_id,
        HOSTNAME=data.get("hostname", "N/A"),
        FLAG=data.get("flag", "N/A"),
        COUNTRY=data.get("displayName", "N/A"),
        COUNTRY_CODE=geo.get("countryCode", "N/A"),
        CITY=geo.get("cityName", "N/A"),
        CONTINENT=geo.get("continent", "N/A"),
        LAT=geo.get("lat", 0.0),
        LON=geo.get("lon", 0.0),
    )


def dict_to_ip_check(data: Dict[str, Any]) -> IpCheckDto:
    """ """
    return IpCheckDto(
        IP=data.get("ip", "N/A"),
        CITY=data.get("cityName", "N/A"),
        COUNTRY=data.get("countryName", "N/A"),
        COUNTRY_CODE=data.get("countryCode", "N/A"),
        IS_PROTECTED=data.get("isConnected", False),
        LATITUDE=float(data.get("lat", 0.0)),
        LONGITUDE=float(data.get("lon", 0.0)),
    )


def dict_to_favorite_dto(data: Dict[str, Any]) -> FavoriteDto:
    valid_id = _validate_id(data.get("id"))
    geo = data.get("geo", {})

    return FavoriteDto(
        ID=valid_id,
        HOSTNAME=str(data.get("hostname", "N/A")),
        CITY=str(geo.get("city", "N/A")),
        COUNTRY=str(geo.get("country", "N/A")),
        IS_FAVORITE=bool(data.get("isFavorite", True)),
    )


def dict_to_recent_connnection(data: Dict[str, Any]) -> RecentConnectionDto:
    valid_id = _validate_id(data.get("id"))

    return RecentConnectionDto(
        ID=valid_id,
        HOSTNAME=data.get("hostname", "N/A"),
        TIMESTAMP=data.get("timestamp", "N/A"),
    )


# --- DTOs TO RAW DICT ---


def favorite_dto_to_dict(dto: FavoriteDto) -> Dict[str, Any]:
    return {
        "id": dto.ID,
        "hostname": dto.HOSTNAME,
        "geo": {"city": dto.CITY, "country": dto.COUNTRY},
        "isFavorite": dto.IS_FAVORITE,
    }


def recent_connection_to_dict(dto: RecentConnectionDto) -> Dict[str, Any]:
    return {"id": dto.ID, "hostname": dto.HOSTNAME, "timestamp": dto.TIMESTAMP}


# -- CROSS-MODEL CONVERSIONS ---


def server_dto_to_server(dto: ServerDto) -> Server:
    return Server(
        ID=dto.ID,
        HOSTNAME=dto.HOSTNAME,
        FLAG=dto.FLAG,
        CITY=dto.CITY,
        COUNTRY=dto.COUNTRY,
        COUNTRY_CODE=dto.COUNTRY_CODE,
        CONTINENT=dto.CONTINENT,
    )


def server_to_server_dto(server: Server) -> ServerDto:
    """Maps from UI server, back to DTO for backend-service"""
    return ServerDto(
        ID=server.ID,
        HOSTNAME=server.HOSTNAME,
        FLAG=server.FLAG,
        CITY=server.CITY,
        COUNTRY_CODE=server.COUNTRY_CODE,
        COUNTRY=server.COUNTRY,
        CONTINENT=server.CONTINENT,
        LAT=0.0,
        LON=0.0,
    )


def server_to_favorite_dto(server: Server) -> FavoriteDto:
    return FavoriteDto(
        ID=server.ID,
        HOSTNAME=server.HOSTNAME,
        CITY=server.CITY,
        COUNTRY=server.COUNTRY,
        IS_FAVORITE=server.IS_FAVORITE,
    )


def server_to_recent_dto(server: Server) -> RecentConnectionDto:
    """Maps a live Server model to a RecentConnection record."""
    return RecentConnectionDto(
        ID=server.ID,
        HOSTNAME=server.HOSTNAME,
        # Using a timestamp so the UI can show 'Connected 2 mins ago'
        TIMESTAMP=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
