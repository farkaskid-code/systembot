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

    config = get_config()
    log_level = (
        config.get("logging").get("level", "INFO") if "logging" in config else "INFO"
    )

    logging.basicConfig(
        filename=Path(data_path / "app.log"), filemode="w", level=log_level
    )

    bashbot = Bashbot(config=config)
    response = bashbot.run(sys.argv[1])
    console.print(Rule())
    console.print("[SYSTEMBOT]: ", style="bold green")
    console.print(Markdown(response))
