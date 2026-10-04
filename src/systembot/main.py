import logging
import platform

from rich.console import Console
from rich.markdown import Markdown
from rich.rule import Rule

from systembot.cli import parse_args
from systembot.executor import execute_command
from systembot.llm.client import Ollama
from systembot.llm.loop import ToolLoop

from .agent import Bashbot

log = logging.getLogger(__name__)
console = Console()


def main():
    # bashbot = Bashbot()
    # response = bashbot.run(parse_args().query)

    prompt = f"""
        - You are a system bot who will interact with the system using the CLI.
        - You will have access to a tool for executing a command which you can call multiple times.
        - When you need to gather information or perform a task, you will execute appropriate commands.
        - When the user requests a query, you will execute the needed commands and then respond in brief and to the point messages.
        - You are working on: {platform.system()}, generate commands accordingly.
    """

    tools = [execute_command]
    loop = ToolLoop(prompt=prompt, client=Ollama(), tools=tools)
    response = loop.run(parse_args().query)
    console.print(Rule())
    console.print("[SYSTEMBOT]: ", style="bold green")
    console.print(Markdown(response))
