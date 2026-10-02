# CLI Parser Implementation

## Goal
Implement a CLI parser using the `argparse` package to handle command-line arguments for the system bot.

## Functionalities
1. Parse the `-u` or `--url` flag to accept a string representing the Ollama host URL.
2. Parse the `-m` or `--model` flag to accept a string representing the model name.
3. Parse the `-h` or `--help` flag to display help information.
4. Parse an unflagged CLI string argument representing the query.

## High Level Approach
1. Import the `argparse` module.
2. Create an `ArgumentParser` object.
3. Add the `-u` or `--url` flag with a type of `str`.
4. Add the `-m` or `--model` flag with a type of `str`.
5. Add the `-h` or `--help` flag to display help information.
6. Add an unflagged CLI string argument for the query.
7. Parse the command-line arguments.
8. Return the parsed arguments.

## Interfaces
- `parse_args() -> argparse.Namespace`: A function that parses the command-line arguments and returns them.

## Notes
- Ensure that the help information for the `-u` and `-m` flags is clear and descriptive.

## TODOs for later
- Add error handling for invalid input values.
