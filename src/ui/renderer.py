import os
from src.ui.style import Style

class MenuRenderer: 

    def __init__(self):
        self.WIDTH = 42
        self.BORDER = f"{Style.BOLD}{'=' * self.WIDTH}{Style.ENDC}"

    def clear (self):
        os.system('clear')

    def draw_header(self, title:str):
        print(f"\n{self.BORDER}")
        print(f" {title.center(self.WIDTH)}")
        print(f"{self.BORDER}\n")

    def draw_option(self, index: int, label: str):
        print(f" [{index}] {label}")

    def draw_footer(self):
        print(f"\n{self.BORDER}")

# Initiate once, directly
renderer = MenuRenderer()