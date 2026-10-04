import logging
import platform

from ollama import Client
from rich.console import Console

from systembot.config import Config

from .executor import execute, execute_command

log = logging.getLogger(__name__)
console = Console()


class Bashbot:
    prompt = f"""
        - You are a system bot who will interact with the system using the CLI.
        - You will have access to a tool for executing a command which you can call multiple times.
        - When you need to gather information or perform a task, you will execute appropriate commands.
        - When the user requests a query, you will execute the needed commands and then respond in brief and to the point messages.
        - You are working on: {platform.system()}, generate commands accordingly.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self.tools = [execute_command]

    def run(self, query: str) -> str:
        log.info(
            f"Using model: {self.config.client.model} served from: {self.config.client.host}"
        )
        client = Client(host=self.config.client.host)
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": query},
        ]

        for turn in range(self.config.max_turns):
            with console.status("[green]Thinking...") as status:
                try:
                    response = client.chat(
                        model=self.config.client.model,
                        messages=messages,
                        tools=self.tools,
                        options=self.config.client.options,
                    )
                    status.update("Done")
                    log.debug(
                        f"Response from model (turn {turn + 1}): {response.message}"
                    )
                    messages.append(
                        {
                            "role": "assistant",
                            "content": response.message.content,
                            "tool_calls": response.message.tool_calls,
                        }
                    )
                except Exception as e:
                    log.error(f"Failed to call model because of: {e}")
                    continue

            if not response.message.tool_calls:
                log.info("No tool calls required, returning model response.")
                return response.message.content

            for call in response.message.tool_calls:
                if call["function"]["name"] == execute_command.__name__:
                    log.info(
                        f"Calling tool: {execute_command.__name__} with args: {call['function']['arguments']}"
                    )
                    console.print("Running: ", end="", style="yellow")
                    command = call["function"]["arguments"]["cmd"]
                    console.print(command)
                    result = execute(config=self.config, cmd=command)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": call["function"]["name"],
                            "content": result,
                        }
                    )
                else:
                    log.warning(f"Tool not found: {call['function']['name']}")
                    return f"Tool not found: {call['function']['name']}"

        log.error(f"Failed to call the model after {self.config.max_turns} tries")
        return f"Failed to call the model after {self.config.max_turns} tries"
