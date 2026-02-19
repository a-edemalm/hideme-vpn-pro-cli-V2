from enum import Enum

class ElementID(Enum):
    """
    Registry of all fixed UI element IDs.
    """
# UI-BUTTON
    #VPN STATUS
    BTN_Q_CONNECT=("btn-q-connect", "Quick Connect", "btn-connect")
    BTN_CONNECT=("btn-connect-selected", "Connect", "btn-connect")
    BTN_DISCONNECT=("btn-disconnect", "Disconnect", "btn-disconnect")
    #VPN SERVER
    BTN_BROWSE_SERVER=("btn-browse", "Browse Servers")
    BTN_FAV_SERVER=("btn-fav", "Favorites")
    BTN_FAV_ADD=("btn-fav-selected", "Add to Favorite")
    #APPLICATION
    BTN_EXIT=("btn-exit", "Exit", "btn-exit")
    BTN_RETURN=("btn-return", "Back to Menu")
# UI-OTHER
    #CONTAINER
    CNR_SIDEBAR=("sidebar")
    CNR_MAIN=("main-panel")
    CNR_MENU_CARD=("","","menu-card")
    #LABEL
    LBL_LIST_TITLE=("list-title", "SERVERS")
    LBL_SERVER_DETAILS=("details-title", "SERVER DETAILS")
    LBL_DETAILS_MSG=("details-msg", "Select a server to see details.")
    #OTHERS
    LIST_SERVER=("server-list")

    def __init__(self, element_id: str, title: str = "", clazz: str = "") -> None:
        """
        Unpacks the tuple of into accessible properties.
        """
        self.id = element_id
        self.title = title
        self.clazz = clazz

class ScreenID(Enum):
    """
    Registry of all screens
    """
    MAIN="main"
    BROWSE_SERVERS="browse_servers"

    def __init__(self, screen_id: str) -> None:
        """
        Unpacks the tuple of into accessible properties.
        """
        self.id = screen_id
