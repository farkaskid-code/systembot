import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.rule import Rule

from .agent import Bashbot
from .config import get_config

log = logging.getLogger(__name__)
console = Console()


def main():
    data_path = Path(Path.home() / ".systembot")

    if not data_path.exists():
        data_path.mkdir()

    logging.basicConfig(
        filename=Path(data_path / "app.log"), filemode="w", level=logging.INFO
    )

    bashbot = Bashbot(config=get_config())
    response = bashbot.run(sys.argv[1])
    console.print(Rule())
    console.print("[SYSTEMBOT]: ", style="bold green")
    console.print(Markdown(response))
