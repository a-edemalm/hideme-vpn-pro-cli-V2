from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class ConnectionInfo:
    """
    """
    IP: str
    CITY: str
    COUNTRY: str
    COUNTRY_CODE: str
    IS_PROTECTED: bool
    LATITUDE: float
    LONGITUDE: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConnectionInfo':
        """
        """
        return cls(
            IP=data.get("ip", "N/A"),
            CITY=data.get("cityName", "N/A"),
            COUNTRY=data.get("countryName", "N/A"),
            COUNTRY_CODE=data.get("countryCode", "N/A"),
            IS_PROTECTED=data.get("isConnected", False), 
            LATITUDE=float(data.get("lat", 0.0)),
            LONGITUDE=float(data.get("lon", 0.0))
        )