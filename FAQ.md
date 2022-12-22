
# Frequently Asked Questions
- [Does Textual support images?](#does-textual-support-images)
- [How do I center a widget in a screen?](#how-do-i-center-a-widget-in-a-screen)
- [How do I pass arguments to an app?](#how-do-i-pass-arguments-to-an-app)

<a name="does-textual-support-images"></a>
## Does Textual support images?

Textual doesn't have built in support for images yet, but it is on the [Roadmap](https://textual.textualize.io/roadmap/).

See also the [rich-pixels](https://github.com/darrenburns/rich-pixels) project for a Rich renderable for images that works with Textual.

<a name="how-do-i-center-a-widget-in-a-screen"></a>
## How do I center a widget in a screen?

To center a widget within a container use
[`align`](https://textual.textualize.io/styles/align/). But remember that
`align` works on the *children* of a container, it isn't something you use
on the child you want centered.

For example, here's an app that shows a `Button` in the middle of a
`Screen`:

```python
from textual.app import App, ComposeResult
from textual.widgets import Button

class ButtonApp(App):

    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Button("PUSH ME!")

if __name__ == "__main__":
    ButtonApp().run()
```

<a name="how-do-i-pass-arguments-to-an-app"></a>
## How do I pass arguments to an app?

When creating your `App` class, override `__init__` as you would when
inheriting normally. For example:

```python
from textual.app import App, ComposeResult
from textual.widgets import Static

class Greetings(App[None]):

    def __init__(self, greeting: str="Hello", to_greet: str="World") -> None:
        self.greeting = greeting
        self.to_greet = to_greet
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(f"{self.greeting}, {self.to_greet}")
```

Then the app can be run, passing in various arguments; for example:

```python
# Running with default arguments.
Greetings().run()

# Running with a keyword arguyment.
Greetings(to_greet="davep").run()

# Running with both positional arguments.
Greetings("Well hello", "there").run()
```

<hr>

Generated by [FAQtory](https://github.com/willmcgugan/faqtory)