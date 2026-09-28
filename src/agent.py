import logging
from collections.abc import Callable
from os import getenv

from ollama import Client

from executor import CmdResult, execute_command
from validator import validate_command

log = logging.getLogger(__name__)


class ConfigError(RuntimeError):
    pass


class Bashbot:
    model: str
    prompt: str
    tools: list[Callable]
    max_turns: int = 10

    def __init__(self, config: dict) -> None:
        self.prompt = (
            "You are a system bot who will interact with the system using the terminal."
            "When you need information to gather information or perform as task, you will be appropriate executing shell commands"
            "You will have access to a tool for executing a shell command"
            "When user requests a query, you will respond in brief and to the point messages."
        )

        self.model = config.get("model", {}).get("name")
        self.num_ctx = config.get("model", {}).get("num_ctx", 4096)
        self.tools = [execute_command]
        self.max_turns = config.get("max_turns", 10)

        if not self.model:
            raise ConfigError("Model information mising")

        self.config = config

    def run(self, query: str) -> str:
        client = Client(host=getenv("OLLAMA_API_BASE"))
        tool_from_name = {tool.__name__: tool for tool in self.tools}
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": query},
        ]

        for _ in range(self.max_turns):
            response = client.chat(
                model=self.model,
                messages=messages,
                tools=self.tools,
                options={"num_ctx": self.num_ctx},
            )
            log.debug(f"Response: {response.message}")
            messages.append(response.message)

            if not response.message.tool_calls:
                return response.message.content

            for call in response.message.tool_calls:
                tool = tool_from_name.get(call.function.name)

                if tool:
                    invalid_commands = validate_command(
                        config=self.config,
                        command=call.function.arguments.get("cmd", ""),
                    )
                    if len(invalid_commands) == 0:
                        log.info(
                            f"Calling tool: {tool.__name__} with args: {call.function.arguments}"
                        )
                        print(
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
                                "content": f"Following commands are blacklisted: {invalid_commands}",
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
