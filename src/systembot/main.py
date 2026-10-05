from rich.console import Console
from rich.markdown import Markdown
from rich.rule import Rule

from systembot.agent.bot import Systembot
from systembot.config import settings

console = Console()


def main():
    answer = Systembot().ask(settings.args.query)
    console.print(Rule())
    console.print("[SYSTEMBOT]:", style="bold green")
    console.print(Markdown(answer))
