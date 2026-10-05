import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from rich.console import Console

from systembot.config import settings
from systembot.llm.client import Client, ClientError, History, Message

log = logging.getLogger(__name__)
console = Console()


@dataclass
class ToolLoop:
    client: Client
    tools: list[Callable[[Any], str]]
    history: History

    def run(self) -> str:
        log.info(f"Running tool loop with {settings.max_turns} maximum turns")
        tool_map = {tool.__name__: tool for tool in self.tools}

        for turn in range(1, settings.max_turns + 1):
            try:
                msg = self.client.chat(self.history, self.tools)
            except ClientError as e:
                log.info(f"Turn {turn}: {e}")
                console.print(e, style="red")
                return f"{e}"

            if len(msg.toolcalls) == 0:
                log.info(f"Turn {turn}: No toolcalls, existing loop")
                return msg.content

            for call in msg.toolcalls:
                tool = tool_map.get(call.name, None)
                if tool:
                    log.info(
                        f"Turn {turn}: Calling tool {tool.__name__} with args {call.args}"
                    )
                    self.history.add(
                        Message(
                            role="tool", tool_name=call.name, content=tool(**call.args)
                        )
                    )
                else:
                    log.info(f"Turn {turn}: No tools found for call {call.name}")

        return "Maximum turns execeeded"
