from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import Button, Input, Label, Static


class EditableText(Static):
    """Custom widget to show (editable) static text."""

    DEFAULT_CSS = """..."""  # Default CSS should go here...

    _confirm_button: Button
    """The button to confirm changes to the text."""
    _edit_button: Button
    """The button to start editing the text."""
    _input: Input
    """The field that allows editing text."""
    _label: Label
    """The label that displays the text."""

    class Edit(Message):
        """The user switched to edit mode."""

    class Display(Message):
        """The user switched to display mode."""

    def compose(self) -> ComposeResult:
        self._input = Input(
            placeholder="Type something...", classes="editabletext--input ethidden"
        )
        self._label = Label("", classes="editabletext--label")
        self._edit_button = Button("📝", classes="editabletext--edit")
        self._confirm_button = Button(
            "✅", classes="editabletext--confirm ethidden", disabled=True
        )

        yield self._input
        yield self._label
        yield self._edit_button
        yield self._confirm_button

    @property
    def is_editing(self) -> bool:
        """Is the text being edited?"""
        return not self._input.has_class("ethidden")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if self.is_editing:
            self.switch_to_display_mode()
        else:
            self.switch_to_editing_mode()

        event.stop()

    def switch_to_editing_mode(self) -> None:
        if self.is_editing:
            return

        self._input.value = str(self._label.renderable)

        self._label.add_class("ethidden")
        self._input.remove_class("ethidden")

        self._edit_button.disabled = True
        self._edit_button.add_class("ethidden")
        self._confirm_button.disabled = False
        self._confirm_button.remove_class("ethidden")

        self.post_message_no_wait(self.Edit(self))

    def switch_to_display_mode(self) -> None:
        if not self.is_editing:
            return

        self._label.renderable = self._input.value

        self._input.add_class("ethidden")
        self._label.remove_class("ethidden")

        self._confirm_button.disabled = True
        self._confirm_button.add_class("ethidden")
        self._edit_button.disabled = False
        self._edit_button.remove_class("ethidden")

        self.post_message_no_wait(self.Display(self))