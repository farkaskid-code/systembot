import logging
from collections.abc import Callable

from ollama import Client
from rich.console import Console

from .executor import execute, execute_command

log = logging.getLogger(__name__)
console = Console()


class Bashbot:
    model: str
    prompt: str
    tools: list[Callable]
    max_turns: int = 10

    def __init__(self, config: dict) -> None:
        self.prompt = (
            "You are a system bot who will interact with the system using the terminal."
            "When you need information to gather information or perform a task, you will appropriately execute shell commands."
            "You will have access to a tool for executing a shell command."
            "When the user requests a query, you will respond in brief and to the point messages."
        )

        self.host = config.get("model", {}).get("host")
        self.model = config.get("model", {}).get("name")
        self.num_ctx = config.get("model", {}).get("num_ctx", 4096)
        self.tools = [execute_command]
        self.max_turns = config.get("max_turns", 10)
        self.config = config

    def run(self, query: str) -> str:
        client = Client(host=self.host)
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": query},
        ]

        for turn in range(self.max_turns):
            with console.status("[bold green]Thinking...") as status:
                try:
                    response = client.chat(
                        model=self.model,
                        messages=messages,
                        tools=self.tools,
                        options={"num_ctx": self.num_ctx},
                    )
                    status.update("Done")
                    log.debug(
                        f"Response from model (turn {turn + 1}): {response.message}"
                    )
                    messages.append(response.message)
                except Exception as e:
                    log.error(f"Failed to call model because of: {e}")
                    continue

            if not response.message.tool_calls:
                log.info("No tool calls required, returning model response.")
                return response.message.content

            for call in response.message.tool_calls:
                if call.function.name == execute_command.__name__:
                    log.info(
                        f"Calling tool: {execute_command.__name__} with args: {call.function.arguments}"
                    )
                    console.print(
                        f"Calling tool: {execute_command.__name__} with args: {call.function.arguments}",
                        style="bold yellow",
                    )
                    result = execute(
                        config=self.config, cmd=call.function.arguments.get("cmd", "")
                    )
                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": call.function.name,
                            "content": result,
                        }
                    )
                else:
                    log.warning(f"Tool not found: {call.function.name}")
                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": call.function.name,
                            "content": "Tool not found",
                        }
                    )

        log.error(f"Failed to call the model after {self.max_turns} tries")
        return "Failed to call the model after {self.max_turns} tries"
