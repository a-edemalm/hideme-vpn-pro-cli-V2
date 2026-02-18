class HideMeConfig:
    """
    Ren och enkel konfiguration. 
    Ingen Enum, ingen .value, ingen konvertering.
    """
    # Strängar - nås via HideMeConfig.PREFIX
    class SERVICE:
        PREFIX = "hide.me@"
    
    class URL:
        SERVERS = "https://api.hide.me/v1/network/free/en"
        IP_CHECK = "https://api.hide.me/ip"

    class IFACE:
        TUNNEL = "vpn"
        IS_STATE_UP = ["up", "unknown"]
    
    # Integer - nås direkt som en int via HideMeConfig.RETRY_ATTEMPTS
    RE_ATTEMPTS = 3