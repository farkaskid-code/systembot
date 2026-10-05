import logging
from abc import ABC
from collections.abc import Callable
from dataclasses import asdict, dataclass, field

import ollama
from rich.console import Console

from systembot.config import settings

log = logging.getLogger(__name__)
console = Console()


@dataclass
class ToolCall:
    name: str
    args: dict = field(default_factory=dict)


@dataclass
class Message:
    role: str
    content: str = ""
    thinking: str = None
    tool_name: str = None
    toolcalls: list[ToolCall] = field(default_factory=list)


@dataclass
class History:
    messages: list[dict] = field(default_factory=list)

    def add(self, msg: Message):
        self.messages.append(asdict(msg))


@dataclass
class Client(ABC):
    def chat(self, history: History, tools: list[Callable]) -> Message: ...


class ClientError(RuntimeError):
    pass


@dataclass
class Ollama(Client):
    client: ollama.Client = field(
        default_factory=lambda: ollama.Client(host=settings.client.host)
    )

    def chat(self, history: History, tools: list[Callable]) -> Message:
        try:
            with console.status("[green]Thinking..."):
                response = self.client.chat(
                    model=settings.client.model,
                    options=settings.client.options,
                    messages=history.messages,
                    tools=tools,
                )
            log.debug(f"Model responded in: {response.total_duration / 10**9} seconds")
        except Exception as e:
            error = f"Failed to call model: {e}"
            log.error(error)
            raise ClientError(error)

        log.debug(f"Model responded with: {response.message}")
        msg = Message(
            role="assistant",
            content=response.message.content,
        )
        if response.message.thinking:
            msg.thinking = response.message.thinking
        if response.message.tool_calls:
            msg.toolcalls = [
                ToolCall(
                    name=call.function.name,
                    args=call.function.arguments,
                )
                for call in response.message.tool_calls
            ]
        history.add(msg)
        return msg
