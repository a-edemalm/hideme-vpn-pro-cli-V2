from textual.app import RenderResult
from textual.widget import Widget

class NordicLogo(Widget):
    """
    The application logo, featuring DEFAULT CSS.
    """ 

    DEFAULT_CSS = """
    NordicLogo {
        width: 100%;
        height: 2;
        content-align: center middle;
        margin: 1 0 0 0; /* TOP RIGHT BOTTOM LEFT */
        text-style: bold;
    }
    """

    def render(self) -> RenderResult:
        """
        Renders the styled ANCII logo using rich markup

        :param self: Instance reference
        """
        return (
            "[bold #88C0D0]Ｈ Ｉ Ｄ Ｅ . Ｍ Ｅ[/]\n"
            "[#81A1C1]Ｖ Ｐ Ｎ   Ｐ Ｒ Ｏ   Ｃ Ｌ Ｉ[/]"
        )