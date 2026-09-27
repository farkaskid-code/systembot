import logging
from collections.abc import Callable
from os import getenv
from typing import NamedTuple

from ollama import Client

log = logging.getLogger(__name__)


class Agent(NamedTuple):
    name: str
    model: str
    prompt: str
    tools: list[Callable]
    max_turns: int = 5

    def run(self, query: str) -> str:
        client = Client(host=getenv("OLLAMA_API_BASE"))
        tool_from_name = {tool.__name__: tool for tool in self.tools}
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": query},
        ]

        for _ in range(self.max_turns):
            response = client.chat(
                model=self.model, messages=messages, tools=self.tools
            )
            log.debug(f"Response: {response.message}")
            messages.append(response.message)

            if not response.message.tool_calls:
                return response.message.content

            for call in response.message.tool_calls:
                tool = tool_from_name.get(call.function.name)

                if tool:
                    log.info(
                        f"Calling tool: {tool.__name__} with args: {call.function.arguments}"
                    )
                    result = tool(**call.function.arguments)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": call.function.name,
                            "content": result,
                        }
                    )
                else:
                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": call.function.name,
                            "content": "Tool not found",
                        }
                    )
