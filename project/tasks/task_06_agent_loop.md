# Task: Implement Agent Loop with Tool Calls

## Goal
Implement an `Agent` class that encapsulates an agent loop using tool calls to execute shell commands one by one. This class will replace the `LLMClient` and will handle communication with the LLM using the Ollama Python SDK. The `Agent` class will take tool functions as arguments during initialization.

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

## High Level Approach
1. **Create the `agent.py` file**.
2. **Define the `Agent` class**:
   - Initialize the class with the required attributes.
   - Implement the `run` method to handle the agent loop.
5. **Testing**:
   - Write unit tests for the `Agent` class to ensure it behaves as expected.
   - Update existing tests to accommodate the new architecture.

## Interfaces
- **Agent Class**:
  - `__init__(self, agent_name: str, model_name: str, system_prompt: str, tool_functions: dict, max_turns: int = 5)`
  - `run(self, user_prompt: str) -> str`

## Notes
- Ensure that the agent loop handles errors gracefully and logs any issues.
- Consider adding a mechanism to handle large command outputs by truncating them to a reasonable size.

## TODOs for Later
- Implement additional features such as logging to a file or integrating with a web interface.
- Address command execution in later tasks.
