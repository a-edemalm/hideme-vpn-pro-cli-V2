from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Button

from core.dtos import Server


class FavoriteButton(Button):
    is_favorite: reactive[bool] = reactive(False)
    server: reactive[Server | None] = reactive(None)

    class ToggleRequest(Message):
        """ """

        def __init__(self, server: Server) -> None:
            self.server = server
            super().__init__()

    def watch_is_favorite(self, new_val: bool) -> None:

        if new_val:
            self.label = "Remove from Favorites"
            self.add_class("is-favorite")
        else:
            self.label = "Add to Favorites"
            self.remove_class("is-favorite")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()

        if self.server:
            self.post_message(self.ToggleRequest(self.server))
