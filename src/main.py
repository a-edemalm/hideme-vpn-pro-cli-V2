#!/usr/bin/env python3
import sys
from src.utils.logger import Logger

try:
    from tui.app_shell import AppShell
except ImportError as e:
    Logger.error(f"Failed to import the application {e}" \
                  "\nMake sure you are running this from root folder:" \
                  "\npython3 main.py")
    sys.exit(1)

def main():
    """
    Creates an instance of app and runs programms
    """
    try:
        app = AppShell()
        app.run()
        
    except KeyboardInterrupt:
        sys.exit(0)

    except Exception as e:
        Logger.error(f"Application crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()