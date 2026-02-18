import datetime
from typing import NamedTuple
from src.ui.style import Style

class LogStyle(NamedTuple):
    label: str
    color: str

    def __str__(self):
        """Override, ToString"""
        return f"{self.color}[{self.label}]{Style.ENDC}"

class Logger:

    class _STYLES:
        """Internal storage, single truth of styles"""
        INFO    = LogStyle("INFO",    Style.BLUE)
        SUCCESS = LogStyle("SUCCESS", Style.GREEN)
        WARNING = LogStyle("WARNING", Style.YELLOW)
        ERROR   = LogStyle("ERROR",   Style.RED)

    @staticmethod
    def _is_show_date(is_date: bool) -> str:
        """Internal helper, builds timestamp"""

        if not is_date: return ""
        
        return f"[{datetime.datetime.now().strftime("%H:%M:%S")}]"
    
    @staticmethod
    def _log(header: LogStyle, body: str, is_date: bool):
        """Internal helper, assembles print message"""

        str_date = Logger._is_show_date(is_date)

        print(f"{str_date}{header} {body}")
    
    @staticmethod
    def info(msg: str, d: bool = True): Logger._log(Logger._STYLES.INFO, msg, d)
        
    @staticmethod
    def success(msg: str, d: bool = True): Logger._log(Logger._STYLES.SUCCESS, msg, d)

    @staticmethod
    def warning(msg: str, d: bool = True): Logger._log(Logger._STYLES.WARNING, msg, d)

    @staticmethod
    def error(msg: str, d: bool = True): Logger._log(Logger._STYLES.ERROR, msg, d)
