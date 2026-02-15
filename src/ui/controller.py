from typing import List, Callable, NamedTuple
from src.utils.logger import Logger
from ui.style import Style
from src.ui.renderer import renderer

class Action(NamedTuple):
    """Data container for menu options."""
    label: str
    callback: Callable
    is_exit: bool = False

class ControllerMenu:

    def __init__(self, title: str):
        self.title = title  
        self.options: List[Action] = []
    
    def _render(self):
            renderer.clear()
            renderer.draw_header(self.title)

            for i, opt in enumerate(self.options, 1):
                renderer.draw_option(i, opt.label)

            renderer.draw_footer()

    def _input(self) -> bool:
        try: 
            user_input = input(f"\n {Style.BOLD}Select >>{Style.ENDC} ").strip()

            if not user_input.isdigit():
                Logger.error("please enter a number.", False)
                input(" Press Enter...")
                return False

            idx = int(user_input) - 1

            if not (0 <= idx < len(self.options)):
                Logger.warning("option out of range.", d=False)
                input(" Press Enter...")
                return False

            selected = self.options[idx]
            selected.callback()

            return selected.is_exit
            
        except KeyboardInterrupt:
                print("\n")
                Logger.info("exiting menu...", False)
                return True
    
    def add(self, label: str, func: Callable, is_exit: bool = False):
        self.options.append(Action(label, func, is_exit))
        return self

    def run(self):
        while True:
            self._render()

            is_exit = self._input()

            if is_exit: break