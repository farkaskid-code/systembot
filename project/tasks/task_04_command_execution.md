# Command Execution

## Goal
Implement the `execute_commands` function in `src/executor.py` to return a list of `CmdResult` objects.

## Functionalities
- Define the `CmdResult` class as a `NamedTuple` with the following fields:
  - `command`: The command that was executed.
  - `return_code`: The return code of the command execution.
  - `stdout`: The standard output of the command.
  - `stderr`: The standard error of the command.
- Update the `execute_commands` function to return a list of `CmdResult` objects instead of tuples.
- Handle exceptions such as `TimeoutExpired` and `CalledProcessError` and include appropriate error messages in the `stderr` field.

## High Level Approach
1. Define the `CmdResult` class in a new file `src/types.py` or within `src/executor.py`.
2. Update the `execute_commands` function to use the `CmdResult` class.
3. Ensure that the function handles exceptions and returns appropriate `CmdResult` objects.

## Interfaces
- **Class:**
  - `CmdResult(command: str, return_code: int, stdout: str, stderr: str)`
    - **Parameters:**
      - `command`: The command that was executed.
      - `return_code`: The return code of the command execution.
      - `stdout`: The standard output of the command.
      - `stderr`: The standard error of the command.
- **Function:**
  - `execute_commands(valid_commands: list[str]) -> list[CmdResult]`
    - **Parameters:**
      - `valid_commands`: A list of validated shell commands to be executed.
    - **Returns:**
      - A list of `CmdResult` objects, where each object contains the command and its corresponding execution results.

## Notes
- Ensure that the function is robust and handles various edge cases, such as empty command lists or commands that produce large outputs.
- Consider adding a configuration option to set the timeout value dynamically.
