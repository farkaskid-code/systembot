import logging
from ast import literal_eval
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from rich.console import Console

from systembot.bootstrap import runtime
from systembot.llm.client import Client, ClientError, History, Message

log = logging.getLogger(__name__)
console = Console()


@dataclass
class ToolLoop:
    client: Client
    tools: list[Callable[[Any], str]]
    history: History

    def run(self) -> str:
        max_turns = runtime.config.max_turns
        log.info(f"Running tool loop with {max_turns} maximum turns")
        tool_map = {tool.__name__: tool for tool in self.tools}

        for turn in range(1, max_turns + 1):
            try:
                msg = self.client.chat(self.history, self.tools)
            except ClientError as e:
                log.info(f"Turn {turn}: {e}")
                console.print(e, style="red")
                return f"{e}"

            if not msg.tool_calls:
                log.info(f"Turn {turn}: No Toolcalls, exiting loop")
                return msg.content

            for call in msg.tool_calls:
                function = call.function
                tool = tool_map.get(function.name, None)
                if tool:
                    log.info(
                        f"Turn {turn}: Calling tool {tool.__name__} with args {call.function.arguments}"
                    )
                    tool_args = function.arguments
                    if type(tool_args) == str:
                        tool_args = literal_eval(tool_args)
                    self.history.add(
                        Message(
                            role="tool",
                            tool_call_id=call.id,
                            content=tool(**tool_args),
                        )
                    )
                else:
                    log.info(f"Turn {turn}: No tools found for call {call.name}")

        return "Maximum turns execeeded"
