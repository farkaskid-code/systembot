import logging
import sys

from agent import Agent
from executor import execute_command

logging.basicConfig(level=logging.ERROR)


def main():
    cli_agent_system_prompt = (
        "You are a system bot who will interact with the system using the terminal."
        "When you need information to gather information or perform as task, you will be appropriate executing shell commands"
        "You will have access to a tool for executing a shell command"
        "When user requests a query, you will respond in brief and to the point messages."
    )

    cli_agent = Agent(
        name="systembot",
        model="qwen3:14b",
        prompt=cli_agent_system_prompt,
        tools=[execute_command],
    )
    print(cli_agent.run(sys.argv[1]))


if __name__ == "__main__":
    main()
