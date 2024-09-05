import os
from typing import Any, Dict, Optional, TypedDict

import click

try:
    from rich.console import Console
    from rich.pretty import pretty_repr
    from rich.rule import Rule
    from rich.theme import Theme

    USE_RICH = True

    console = Console(theme=Theme({"rule.line": "gold3"}))
except ImportError:
    USE_RICH = False


class VerboseItem(TypedDict):
    data: Any
    level: int


class VerboseInfo:
    data: Dict[str, VerboseItem]
    level: Optional[int]

    def __init__(self, raw_data: Dict[str, Any], raw_level: Optional[int]) -> None:
        self.data = {}
        self.level = raw_level
        for key, value in raw_data.items():
            self.data[key] = VerboseItem(data=value, level=1)

    def add(self, key: str, data: Any, level: int):
        self.data[key] = VerboseItem(data=data, level=level)

    def show(self):
        if self.level and self.level > 0:
            if USE_RICH:
                console.print(Rule(__package__, characters="="))

                for key, value in self.data.items():
                    if self.level >= value["level"]:
                        console.print(f"{key}: {pretty_repr(value['data'])}")

                console.print(Rule(characters="="))
            else:
                try:
                    width, _ = os.get_terminal_size()
                except OSError:
                    # Might get `Inappropriate ioctl for device` on GitHub Actions
                    width = 80

                width_with_title = (width - 2 - len(__package__)) // 2
                rule_line = "=" * width_with_title

                click.echo(f"{rule_line} {__package__} {rule_line}")
                for key, value in self.data.items():
                    if self.level >= value["level"]:
                        click.echo(f"{key}: {value['data']}")
                click.echo("=" * width)
