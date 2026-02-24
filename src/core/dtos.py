from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

# --- DATACLASS FROZEN DTOs

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    """
    Encapsulates the outcome of an operation, carrying state,
    message, and optional payloads.
    """

    is_success: bool
    msg: str
    data: Optional[T] = None

    @classmethod
    def ok(cls, msg: str = "", data: Optional[T] = None) -> "Result[T]":
        """Constructs a successful result, for end-user"""
        return cls(is_success=True, msg=msg, data=data)

    @classmethod
    def fail(cls, msg: str = "") -> "Result[T]":
        """Constructs a failed result, for end-user"""
        return cls(is_success=False, msg=msg)


@dataclass(frozen=True)
class ServerDto:
    ID: int
    HOSTNAME: str
    FLAG: str

    # Geo-data (Plockas från geo-objektet)
    CITY: str
    COUNTRY_CODE: str
    COUNTRY: str
    CONTINENT: str
    LAT: float
    LON: float

    @property
    def service_name(self) -> str:
        """Helper method for systemd-name-flag"""
        return self.FLAG


@dataclass(frozen=True)
class IpCheckDto:
    """ """

    IP: str
    CITY: str
    COUNTRY: str
    COUNTRY_CODE: str
    IS_PROTECTED: bool
    LATITUDE: float
    LONGITUDE: float


@dataclass(frozen=True)
class FavoriteDto:
    ID: int
    HOSTNAME: str
    CITY: str
    COUNTRY: str
    IS_FAVORITE: bool


@dataclass(frozen=True)
class RecentConnectionDto:
    ID: int
    HOSTNAME: str
    TIMESTAMP: str


@dataclass(frozen=True)
class NetworkDto:
    @dataclass(frozen=True)
    class _API_URLS:
        SERVERS = "https://api.hide.me/v1/network/free/en"
        IP_CHECK = "https://api.hide.me/ip"

    API_URLS: _API_URLS = field(default_factory=_API_URLS)
    SYSTEMD_TARGET: str = "hide.me@"


# --- DATACLASS DTOs


@dataclass
class Server:
    ID: int
    HOSTNAME: str
    FLAG: str
    # GEO
    CITY: str
    COUNTRY: str
    COUNTRY_CODE: str
    CONTINENT: str

    # FAVORITE.json
    IS_FAVORITE: bool = False
