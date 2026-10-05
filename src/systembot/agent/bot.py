import platform
from dataclasses import dataclass, field
from logging import getLogger
from pathlib import Path

from rich.console import Console

from systembot.config import settings
from systembot.executor import execute_command
from systembot.llm.client import History, Message, Ollama, OpenAICompat
from systembot.llm.loop import ToolLoop

log = getLogger(__name__)
console = Console()


@dataclass
class Systembot:
    history: History = field(default_factory=History)

    def setup_prompt(self):
        path = Path(__file__).resolve().parent / "systembot_prompt.md"
        try:
            log.debug(f"Reading system_prompt from: {path}")
            prompt = path.read_text()
        except FileNotFoundError:
            msg = f"Failed to initialize the bot with system_prompt, check if {path} exists"
            log.error(msg)
            console.print(msg, style="red")

        self.history.add(Message(role="system", content=prompt))

    def platform_context(self):
        current_platform = platform.system()
        log.debug(f"Operating on: {current_platform}")
        context = f"You are on: {current_platform}, generate commands accordingly"
        self.history.add(Message(role="system", content=context))

    def ask(self, query: str) -> str:
        self.setup_prompt()
        self.platform_context()

        log.debug(f"User query: {query}")
        self.history.add(Message(role="user", content=query))

        client = (
            OpenAICompat() if settings.client.provider == "openai-compat" else Ollama()
        )

        loop = ToolLoop(client=client, tools=[execute_command], history=self.history)
        return loop.run()
