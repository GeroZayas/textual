from textual.app import App, ComposeResult
from textual.widgets import Label, Button

class HelloApp(App):
    def compose(self) -> ComposeResult:
        name = 'Gero' 
        yield(Label(name))

if __name__ == "__main__":
    app = HelloApp()
    app.run()