# Task: Implement Agent Loop with Tool Calls

## Goal
Implement an `Agent` class that encapsulates an agent loop using tool calls to execute shell commands one by one. This class will replace the `LLMClient` and will handle communication with the LLM using the Ollama Python SDK. The `Agent` class will take tool functions as arguments during initialization. Additionally, update the `execute_commands` function to handle a single command and create a higher-order function `executor` that returns a tool call function.

## Functionalities
1. **Initialization**:
   - Initialize the agent with an agent name, model name, system prompt, tool functions, and an optional maximum number of turns.
2. **Agent Loop**:
   - Implement a method to run the agent loop, which will:
     - Send the user prompt to the LLM.
     - Handle tool calls to execute shell commands.
     - Send the command outputs back to the LLM for analysis.
     - Continue the loop until the LLM stops requesting tools or reaches the maximum number of turns.
3. **Logging and Debugging**:
   - Add logging to track the flow of the agent loop and any errors that occur.
4. **Command Execution**:
   - Update the `execute_commands` function to handle a single command and rename it to `execute_command`.
   - Create a higher-order function `executor` that returns a tool call function.
   - The tool call function will take a command as a string argument and return a JSON-serialized `CmdResult` object.

## High Level Approach
1. **Create the `agent.py` file**.
2. **Define the `Agent` class**:
   - Initialize the class with the required attributes.
   - Implement the `run` method to handle the agent loop.
3. **Update `executor.py`**:
   - Rename `execute_commands` to `execute_command`.
   - Create the `executor` function that returns a tool call function.
4. **Update `main.py`**:
   - Replace the `LLMClient` with the `Agent` class.
   - Use the `executor` function to create a tool call function and pass it to the `Agent` instance.
5. **Testing**:
   - Write unit tests for the `Agent` class to ensure it behaves as expected.
   - Update existing tests to accommodate the new architecture.
   - Write unit tests for the `executor` function and the tool call function.

## Interfaces
- **Agent Class**:
  - `__init__(self, agent_name: str, model_name: str, system_prompt: str, tool_functions: dict, max_turns: int = 5)`
  - `run(self, user_prompt: str) -> str`

- **executor.py**:
  - `execute_command(config: dict, command: str) -> CmdResult`
  - `executor(config: dict) -> Callable[[str], str]`

## Notes
- Ensure that the agent loop handles errors gracefully and logs any issues.
- Consider adding a mechanism to handle large command outputs by truncating them to a reasonable size.

## TODOs for Later
- Implement additional features such as logging to a file or integrating with a web interface.
- Address command execution in later tasks.
