from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass(frozen=True)
class Server:
    """
    DTO represents a VPN-server from API:data
    """
    ID: int
    HOSTNAME: str
    FLAG: str
    DISPLAY_NAME: str
    
    # Geo-data (Plockas från geo-objektet)
    COUNTRY_CODE: str
    CITY: str
    CONTINENT: str
    LAT: float
    LON: float
    
    # Metadata
    TAGS: List[str] = field(default_factory=list)

    @property
    def service_name(self) -> str:
        """
        Helper method, for systemd-name-flag
        """
        return self.COUNTRY_CODE.lower()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Server':
        """
        Maps the complete JSON structure to the Server dataclass.
        """
        geo = data.get("geo", {})

        return cls(
            ID=data.get("id", 0),
            HOSTNAME=data.get("hostname", "N/A"),
            FLAG=data.get("flag", "N/A"),
            DISPLAY_NAME=data.get("displayName", "N/A"),
            
            # Nested Geo Mapping
            COUNTRY_CODE=geo.get("countryCode", "N/A"),
            CITY=geo.get("cityName", "N/A"),
            CONTINENT=geo.get("continent", "N/A"),
            LAT=geo.get("lat", 0.0),
            LON=geo.get("lon", 0.0),
            
            # Tags list
            TAGS=data.get("tags", [])
        )