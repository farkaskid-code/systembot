import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from systembot.config import settings
from systembot.llm.client import Client, History, Message

log = logging.getLogger(__name__)


@dataclass
class ToolLoop:
    prompt: str
    client: Client
    tools: list[Callable[[Any], str]]
    history: History = field(default_factory=History)

    def run(self, query: str) -> str:
        tool_map = {tool.__name__: tool for tool in self.tools}

        self.history.add(Message(role="system", content=self.prompt))
        self.history.add(Message(role="user", content=query))

        for turn in range(settings.max_turns):
            msg = self.client.chat(self.history, self.tools)
            print(msg)
            if len(msg.toolcalls) == 0:
                return msg.content

            for call in msg.toolcalls:
                tool = tool_map.get(call.name, None)
                if tool:
                    self.history.add(
                        Message(
                            role="tool", tool_name=call.name, content=tool(**call.args)
                        )
                    )
