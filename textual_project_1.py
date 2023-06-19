from textual.app import App, ComposeResult
from textual.widgets import Label, Button, Header


class QuestionApp(App[str]):
    
    TITLE = "625 Words to learn!"
    SUB_TITLE = "The first words to learn in any language!"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("GERO ZAYAS", id="question") 
        yield Button("Yes", id="1", variant="primary")
        yield Button("Yes", id="2", variant="primary")
        yield Button("Yes", id="3", variant="primary")
        yield Button("No", id="4", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)

if __name__ == "__main__":
    app = QuestionApp()
    reply = app.run()
    print(reply)


