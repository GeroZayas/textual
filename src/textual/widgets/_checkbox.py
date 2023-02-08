from __future__ import annotations

from typing import ClassVar

from rich.console import RenderableType

from ..binding import Binding, BindingType
from ..geometry import Size
from ..message import Message
from ..reactive import reactive
from ..widget import Widget
from ..scrollbar import ScrollBarRender


class Checkbox(Widget, can_focus=True):
    """A checkbox widget that represents a boolean value.

    Can be toggled by clicking on it or through its [bindings][textual.widgets.Checkbox.BINDINGS].

    The checkbox widget also contains [component classes][textual.widgets.Checkbox.COMPONENT_CLASSES]
    that enable more customization.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("enter,space", "toggle", "Toggle", show=False),
    ]
    """
    | Key(s) | Description |
    | :- | :- |
    | enter,space | Toggle the checkbox status. |
    """

    COMPONENT_CLASSES: ClassVar[set[str]] = {
        "checkbox--switch",
    }
    """
    | Class | Description |
    | :- | :- |
    | `checkbox--switch` | Targets the switch of the checkbox. |
    """

    DEFAULT_CSS = """
    Checkbox {
        border: tall transparent;
        background: $panel;
        height: auto;
        width: auto;
        padding: 0 2;
    }

    Checkbox > .checkbox--switch {
        background: $panel-darken-2;
        color: $panel-lighten-2;
    }

    Checkbox:hover {
        border: tall $background;
    }

    Checkbox:focus {
        border: tall $accent;
    }

    Checkbox.-on {

    }

    Checkbox.-on > .checkbox--switch {
        color: $success;
    }
    """

    value = reactive(False, init=False)
    """The value of the checkbox; `True` for on and `False` for off."""

    slider_pos = reactive(0.0)
    """The position of the slider."""

    class Changed(Message, bubble=True):
        """Posted when the status of the checkbox changes.

        Can be handled using `on_checkbox_changed` in a subclass of `Checkbox`
        or in a parent widget in the DOM.

        Attributes:
            value: The value that the checkbox was changed to.
            input: The `Checkbox` widget that was changed.
        """

        def __init__(self, sender: Checkbox, value: bool) -> None:
            super().__init__(sender)
            self.value: bool = value
            self.input: Checkbox = sender

    def __init__(
        self,
        value: bool = False,
        *,
        animate: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        """Initialise the checkbox.

        Args:
            value: The initial value of the checkbox. Defaults to False.
            animate: True if the checkbox should animate when toggled. Defaults to True.
            name: The name of the checkbox.
            id: The ID of the checkbox in the DOM.
            classes: The CSS classes of the checkbox.
        """
        super().__init__(name=name, id=id, classes=classes)
        if value:
            self.slider_pos = 1.0
            self._reactive_value = value
        self._should_animate = animate

    def watch_value(self, value: bool) -> None:
        target_slider_pos = 1.0 if value else 0.0
        if self._should_animate:
            self.animate("slider_pos", target_slider_pos, duration=0.3)
        else:
            self.slider_pos = target_slider_pos
        self.post_message_no_wait(self.Changed(self, self.value))

    def watch_slider_pos(self, slider_pos: float) -> None:
        self.set_class(slider_pos == 1, "-on")

    def render(self) -> RenderableType:
        style = self.get_component_rich_style("checkbox--switch")
        return ScrollBarRender(
            virtual_size=100,
            window_size=50,
            position=self.slider_pos * 50,
            style=style,
            vertical=False,
        )

    def get_content_width(self, container: Size, viewport: Size) -> int:
        return 4

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        return 1

    def on_click(self) -> None:
        self.toggle()

    def action_toggle(self) -> None:
        self.toggle()

    def toggle(self) -> None:
        """Toggle the checkbox value. As a result of the value changing,
        a Checkbox.Changed message will be posted."""
        self.value = not self.value
