import logging
from abc import ABC
from ast import arguments, literal_eval
from collections.abc import Callable
from dataclasses import asdict, dataclass, field

import ollama
from function_schema import get_function_schema
from openai import OpenAI
from rich.console import Console

from systembot.config import settings

log = logging.getLogger(__name__)
console = Console()


@dataclass
class Function:
    name: str
    arguments: dict


@dataclass
class ToolCall:
    function: Function
    id: str = None
    type: str = "function"


@dataclass
class Message:
    role: str
    content: str = None
    thinking: str = None
    tool_call_id: str = None
    tool_calls: list[ToolCall] = None

    def asdict(self) -> dict:
        data = {"role": self.role}

        if self.content:
            data["content"] = self.content

        if self.thinking:
            data["thinking"] = self.thinking

        if self.tool_call_id:
            data["tool_call_id"] = self.tool_call_id

        if self.tool_calls:
            data["tool_calls"] = [asdict(call) for call in self.tool_calls]

        return data


@dataclass
class History:
    messages: list[dict] = field(default_factory=list)

    def add(self, msg: Message):
        self.messages.append(msg.asdict())


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

        model_msg = response.message
        log.debug(f"Model responded with: {model_msg}")

        msg = Message(role="assistant")
        if model_msg.content:
            msg.content = model_msg.content

        if model_msg.thinking:
            msg.thinking = model_msg.thinking

        if model_msg.tool_calls:
            msg.tool_calls = [
                ToolCall(
                    function=Function(
                        name=call.function.name,
                        arguments=call.function.arguments,
                    ),
                )
                for call in model_msg.tool_calls
            ]
        history.add(msg)
        return msg


@dataclass
class OpenAICompat(Client):
    client: OpenAI = field(
        default_factory=lambda: OpenAI(
            base_url=settings.client.host, api_key=settings.client.api_key
        )
    )

    def chat(self, history: History, tools: list[Callable]) -> Message:
        log.debug(f"Messages: {history.messages}")
        try:
            with console.status("[green]Thinking..."):
                response = self.client.chat.completions.create(
                    model=settings.client.model,
                    messages=history.messages,
                    tools=[
                        {"type": "function", "function": get_function_schema(tool)}
                        for tool in tools
                    ],
                )
        except Exception as e:
            error = f"Failed to call model: {e}"
            log.error(error)
            raise ClientError(error)

        model_msg = response.choices[0].message
        log.debug(f"Model responded with: {model_msg}")
        msg = Message(role="assistant")

        if model_msg.content:
            msg.content = model_msg.content

        if model_msg.tool_calls:
            msg.tool_calls = [
                ToolCall(
                    id=call.id,
                    function=Function(
                        name=call.function.name,
                        arguments=call.function.arguments,
                    ),
                )
                for call in model_msg.tool_calls
            ]
        history.add(msg)
        return msg
