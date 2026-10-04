import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.rule import Rule

from systembot.cli import parse_args

from .agent import Bashbot
from .config import Config

log = logging.getLogger(__name__)
console = Console()

DATAPATH = Path(Path.home() / ".systembot")


def main():
    config_path = DATAPATH / "config.yaml"
    logfile_path = DATAPATH / "app.log"
    args = parse_args()

    config = Config()

    if not DATAPATH.exists():
        if args.url is None or args.model is None:
            print(
                "Initial run. No config file. Pass Ollama host URL with -u and model name with -m"
            )
            sys.exit(1)
        config.from_args(args)
        DATAPATH.mkdir()
        config.dump_yaml(config_path)
    else:
        config.from_yaml(config_path)
        config.from_args(args)

    logging.basicConfig(
        filename=logfile_path, filemode=config.logging.mode, level=config.logging.level
    )

    bashbot = Bashbot(config=config)
    response = bashbot.run(args.query)
    console.print(Rule())
    console.print("[SYSTEMBOT]: ", style="bold green")
    console.print(Markdown(response))
