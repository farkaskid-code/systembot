# Bot
# data - LLMCient, messages, responseHandler

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class LLMRequest:
    model: str
    messages: list[dict]
    tools: list[Callable]
    options: dict


@dataclass
class LLMResponse:
    message: dict
    tool_calls: list[dict]


@dataclass
class LLMCient(ABC):
    url: str

    @abstractmethod
    def chat(self, request: LLMRequest) -> LLMResponse | None: ...


@dataclass
class ChatLoop:
    model: str
    options: dict
    client: LLMCient
    messages: list[dict]
    tools: list[Callable]
    handler: Callable[[LLMResponse], dict | None]

    def run(self):
        while True:
            response = self.client.chat(
                LLMRequest(
                    model=self.model,
                    messages=self.messages,
                    tools=self.tools,
                    options=self.options,
                )
            )
            message = self.handler(response)
            if message:
                self.messages.append(message)
            else:
                break
