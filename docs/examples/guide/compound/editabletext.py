from typing import Any

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Button, Input, Label, Static, TextLog


class _EditableTextButtonContainer(Horizontal):
    pass


class EditableText(Static):
    DEFAULT_CSS = """
    EditableText {
        layout: horizontal;
        width: 1fr;
        height: 3;
    }

    .editabletext--input {
        width: 1fr;
        height: 3;
    }

    .editabletext--label {
        width: 1fr;
        height: 3;
        border: round $primary;
    }

    _EditableTextButtonContainer {
        padding-left: 1;
        padding-right: 1;
        width: auto;
    }

    .editabletext--edit {
        min-width: 0;
        width: 4;
    }

    .editabletext--confirm {
        min-width: 0;
        width: 4;
    }

    EditableText .ethidden {
        display: none;
    }
    """

    _confirm_button: Button
    """The button to confirm changes to the text."""
    _edit_button: Button
    """The button to start editing the text."""
    _input: Input
    """The field that allows editing text."""
    _label: Label
    """The label that displays the text."""

    class Edit(Message):
        """Sent when the user starts editing text."""

    class Display(Message):
        """Sent when the user starts displaying text."""

    def compose(self) -> ComposeResult:
        self._input = Input(
            placeholder="Type something...", classes="editabletext--input ethidden"
        )
        self._label = Label("", classes="editabletext--label")
        self._edit_button = Button(
            "📝",
            classes="editabletext--edit etbutton",
        )
        self._confirm_button = Button(
            "✅",
            classes="editabletext--confirm etbutton",
            disabled=True,
        )

        yield self._input
        yield self._label
        yield _EditableTextButtonContainer(
            self._edit_button,
            self._confirm_button,
        )

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
        self._confirm_button.disabled = False

        self.emit_no_wait(self.Edit(self))

    def switch_to_display_mode(self) -> None:
        if not self.is_editing:
            return

        self._label.renderable = self._input.value

        self._input.add_class("ethidden")
        self._label.remove_class("ethidden")

        self._confirm_button.disabled = True
        self._edit_button.disabled = False

        self.emit_no_wait(self.Display(self))


class EditableTextApp(App[None]):

    text_log: TextLog

    def compose(self) -> ComposeResult:
        self.text_log = TextLog()

        yield Label("Hey, there!")
        yield EditableText()
        yield EditableText()
        yield Label("Bye")
        yield EditableText()
        yield Button()
        yield self.text_log

    def on_editable_text_edit(self, event: EditableText.Edit) -> None:
        self.text_log.write(f"Editing {id(event.sender)}.")

    def on_editable_text_display(self, event: EditableText.Display) -> None:
        self.text_log.write(f"Displaying {id(event.sender)}.")

    def on_button_pressed(self) -> None:
        for editabletext in self.query(EditableText):
            editabletext.switch_to_editing_mode()


app = EditableTextApp()


if __name__ == "__main__":
    app.run()
