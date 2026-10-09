import logging
from abc import ABC
from collections.abc import Callable
from dataclasses import asdict, dataclass, field

import ollama
from function_schema import get_function_schema
from openai import OpenAI
from rich.console import Console

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
    ctx_size: int = -1

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
class Client(ABC):
    def chat(self, messages: list[dict], tools: list[Callable]) -> Message: ...


class ClientError(RuntimeError):
    pass


@dataclass
class Ollama(Client):
    client: ollama.Client
    model: str
    options: dict = field(default_factory=dict)

    def chat(self, messages: list[dict], tools: list[Callable]) -> Message:
        try:
            with console.status("[green]Thinking..."):
                response = self.client.chat(
                    model=self.model,
                    options=self.options,
                    messages=messages,
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
        msg.ctx_size = response.prompt_eval_count

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
        return msg


@dataclass
class OpenAICompat(Client):
    client: OpenAI
    model: str

    def chat(self, messages: list[dict], tools: list[Callable]) -> Message:
        try:
            with console.status("[green]Thinking..."):
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
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
        msg.ctx_size = response.usage.prompt_tokens

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
        return msg
