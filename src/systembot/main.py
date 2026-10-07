from rich.console import Console
from rich.markdown import Markdown
from rich.rule import Rule

from systembot.agent.bot import Systembot
from systembot.bootstrap import runtime

console = Console()


def main():
    answer = Systembot().ask(runtime.query)
    console.print(Rule())
    console.print("[SYSTEMBOT]:", style="bold green")
    console.print(Markdown(answer))
