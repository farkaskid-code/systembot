import logging
from ast import literal_eval
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from rich.console import Console

from systembot.bootstrap import runtime
from systembot.llm.client import Client, ClientError, Message
from systembot.llm.context import Context, Interaction

log = logging.getLogger(__name__)
console = Console()


@dataclass
class ToolLoop:
    client: Client
    tools: list[Callable[[Any], str]]
    context: Context

    def run(self) -> str:
        max_turns = runtime.config.max_turns
        log.info(f"Running tool loop with {max_turns} maximum turns")
        tool_map = {tool.__name__: tool for tool in self.tools}

        for turn in range(1, max_turns + 1):
            interaction = self.context.history[-1]
            try:
                msg = self.client.chat(self.context.get_messages(), self.tools)
            except ClientError as e:
                log.info(f"Turn {turn}: {e}")
                console.print(e, style="red")
                return f"{e}"

            interaction.ctx_size = msg.ctx_size - self.context.size
            self.context.size = msg.ctx_size
            log.info(f"Turn {turn}: Context size - {self.context.size} tokens")

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

                    tool_msg = Message(
                        role="tool",
                        tool_call_id=call.id,
                        content=tool(**tool_args),
                    )
                    self.context.add(Interaction(model_msg=msg, reply_msg=tool_msg))
                else:
                    log.info(f"Turn {turn}: No tools found for call {call.name}")

        return "Maximum turns execeeded"
