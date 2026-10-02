import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.rule import Rule

from systembot.cli import parse_args

from .agent import Bashbot
from .config import create_basic_config, get_config

log = logging.getLogger(__name__)
console = Console()

DATAPATH = Path(Path.home() / ".systembot")


def main():
    args = parse_args()
    config = {}

    if not DATAPATH.exists():
        DATAPATH.mkdir()
        config = create_basic_config(args)
    else:
        config = get_config()
        if args.url and args.model:
            config["model"] = {"host": args.url, "name": args.model}

    if "logging" in config:
        log_level = config.get("logging").get("level", "INFO")
        log_mode = config.get("logging").get("mode", "w")

    logging.basicConfig(
        filename=Path(DATAPATH / "app.log"), filemode=log_mode, level=log_level
    )

    bashbot = Bashbot(config=config)
    response = bashbot.run(args.query)
    console.print(Rule())
    console.print("[SYSTEMBOT]: ", style="bold green")
    console.print(Markdown(response))
