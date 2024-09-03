# In a non-interactive, non-testing mode, route input from stdin to the output.
# When testing, read from the object provided (probably a StreamIO)

from pathlib import Path
import sys

from wizlib.handler import Handler
from wizlib.parser import WizParser
import wizlib.io


class StreamHandler(Handler):
    """Handle non-interactive input, such as via a pipe in a shell. Only runs
    when not in a tty."""

    name = 'stream'
    text: str = ''

    def __init__(self, file=None, stdin=True):
        if file:
            self.text = Path(file).read_text()
        elif not wizlib.io.isatty():
            self.text = wizlib.io.stream()

    def __str__(self):
        return self.text

    @classmethod
    def fake(cls, value):
        """Return a fake StreamHandler with forced values, for testing"""
        handler = cls(stdin=False)
        handler.text = value
        return handler
