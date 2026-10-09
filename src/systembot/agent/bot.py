import platform
from dataclasses import dataclass, field
from logging import getLogger
from pathlib import Path

from rich.console import Console

from systembot.bootstrap import runtime
from systembot.executor import execute_command
from systembot.llm.client import Message
from systembot.llm.context import Context, Interaction
from systembot.llm.loop import ToolLoop

log = getLogger(__name__)
console = Console()


def setup_prompt() -> Message:
    path = Path(__file__).resolve().parent / "systembot_prompt.md"
    try:
        log.debug(f"Reading system_prompt from: {path}")
        prompt = path.read_text()
        current_platform = platform.system()
        log.info(f"Operating on: {current_platform}")
        prompt = (
            f"{prompt}\n\nYou are on: {current_platform}, generate commands accordingly"
        )
        return Message(role="system", content=prompt)
    except FileNotFoundError:
        msg = f"Failed to initialize the bot with system_prompt, check if {path} exists"
        log.error(msg)
        console.print(msg, style="red")


@dataclass
class Systembot:
    context: Context = field(
        default_factory=lambda: Context(cap=int(runtime.ctx_size * 0.9))
    )

    def ask(self, query: str) -> str:
        system_prompt_msg = setup_prompt()

        log.info(f"User query: {query}")
        query_msg = Message(role="user", content=query)

        self.context.add(Interaction(model_msg=system_prompt_msg, reply_msg=query_msg))

        log.debug(f"Using client for: {runtime.config.client.provider}")

        loop = ToolLoop(
            client=runtime.client, tools=[execute_command], context=self.context
        )
        result = loop.run()
        log.debug(f"History: {self.context.history}")
        return result
