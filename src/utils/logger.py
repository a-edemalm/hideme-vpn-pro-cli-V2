import datetime
from typing import NamedTuple


class ANSI:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


class _LogStyle(NamedTuple):
    label: str
    color: str

    def __str__(self):
        """Override, ToString"""
        return f"{self.color}[{self.label}]{ANSI.ENDC}"


class Logger:
    class _STYLES:
        """Internal storage, single truth of styles"""

        INFO = _LogStyle("INFO", ANSI.BLUE)
        SUCCESS = _LogStyle("SUCCESS", ANSI.GREEN)
        WARNING = _LogStyle("WARNING", ANSI.YELLOW)
        ERROR = _LogStyle("ERROR", ANSI.RED)

    @staticmethod
    def _is_show_date(is_date: bool) -> str:
        """Internal helper, builds timestamp"""

        if not is_date:
            return ""

        return f"[{datetime.datetime.now().strftime('%H:%M:%S')}]"

    @staticmethod
    def _log(header: _LogStyle, body: str, is_date: bool):
        """Internal helper, assembles print message"""

        str_date = Logger._is_show_date(is_date)

        print(f"{str_date}{header} {body}")

    @staticmethod
    def info(msg: str, d: bool = True):
        Logger._log(Logger._STYLES.INFO, msg, d)

    @staticmethod
    def success(msg: str, d: bool = True):
        Logger._log(Logger._STYLES.SUCCESS, msg, d)

    @staticmethod
    def warning(msg: str, d: bool = True):
        Logger._log(Logger._STYLES.WARNING, msg, d)

    @staticmethod
    def error(msg: str, d: bool = True):
        Logger._log(Logger._STYLES.ERROR, msg, d)
