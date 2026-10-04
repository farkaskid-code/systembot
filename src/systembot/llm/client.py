import logging
from abc import ABC
from collections.abc import Callable
from dataclasses import asdict, dataclass, field

import ollama

from systembot.config import settings

log = logging.getLogger(__name__)


@dataclass
class ToolCall:
    name: str
    args: dict = field(default_factory=dict)


@dataclass
class Message:
    role: str
    content: str = ""
    tool_name: str = None
    toolcalls: list[ToolCall] = field(default_factory=list)


@dataclass
class History:
    messages: list[Message] = field(default_factory=list)

    def add(self, msg: Message):
        self.messages.append(asdict(msg))


@dataclass
class Client(ABC):
    def chat(self, history: History, tools: list[Callable]) -> Message: ...


class ClientError(RuntimeError):
    pass


@dataclass
class Ollama(Client):
    client: ollama.Client = None

    def chat(self, history: History, tools: list[Callable]) -> Message:
        if not self.client:
            self.client = ollama.Client(host=settings.client.host)

        try:
            response = self.client.chat(
                model=settings.client.model,
                options=settings.client.options,
                messages=history.messages,
                tools=tools,
            )
            toolcalls = []
            if response.message.tool_calls:
                toolcalls = [
                    ToolCall(
                        name=call["function"]["name"],
                        args=call["function"]["arguments"],
                    )
                    for call in response.message.tool_calls
                ]
            msg = Message(
                role="assistant",
                content=response.message.content,
                toolcalls=toolcalls,
            )
            history.add(msg)
            return msg
        except Exception as e:
            error = f"Failed to call model: {e}"
            log.error(error)
            raise ClientError(error)
