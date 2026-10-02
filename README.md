# systembot

## Overview
`systembot` is a CLI tool that acts as a bridge between natural language instructions and shell execution, using a local LLM for command generation and analysis. It ensures safe execution of commands by validating them against a configurable blacklist.

## Prerequisites
- Ollama server running with the desired model.
- Python 3.x installed.
- [UV](https://docs.astral.sh/uv/getting-started/installation/) package manager installed.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install the tool using UV:
   ```bash
   cd <repository-directory>
   uv tool install .
   ```

## Getting Started
You need a Ollama server and a tool calling model for this to work, it's required. Once setup, just run,
```bash
systembot -u http://{ollama-server-host}:11434 -m {model-name} "hello"
```

to do a test run. This will create a basic config file at `~/.systembot/config.yaml`.
Once the configuration file is there, you don't need to pass the `-u` and `-m` flags.
Simply go,
```bash
sysetmbot "what's my IP?"
```

## Configuration Reference
Configuration file is at `~/.systembot/config.yaml` with the following content:
```yaml
model: # Required: it needs an Ollama server to work
  host: http://{ollama-server-host}:11434
  name: qwen3:14b # A model that supports tool calling
  num_ctx: 16384 # Optional

blacklist: # Optional but recommended for safety guardrails
  - rm
  - shutdown
  - reboot
  - dd
  - mkfs

logging: # Optional
  level: INFO # Options are: [NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL], increasing order of severity. Defaults INFO
  mode: w # Options are: [w, a], meaning write, append. Defaults to w.

max_turns: 8 # Optional. Max turn allowed for the agent loop
command_timeout: 10 # Optional. Timeout in seconds for shell command execution
```

## Usage
Run the tool with a natural language prompt:
```bash
systembot "natural language prompt"
```

## Example
### Basic use case:
General queries about the system, basic tasks.

<img width="1260" height="547" alt="Screenshot From 2026-10-02 18-58-21" src="https://github.com/user-attachments/assets/df3a2fbc-653a-4f16-93b4-72d19a30e737" />

### Advanced use case:
You can create instruction / task files for specific workflows and ask `systembot` to execute that workflow.

<img width="1458" height="1032" alt="Screenshot From 2026-10-02 19-07-43" src="https://github.com/user-attachments/assets/5cae99b4-ab4f-435c-8b44-149a6ae4b06e" />

## Notes
- Platform agnostic, will work on Linux, Windows and Mac OS.
- Commands are validated before execution to prevent blacklisted commands from running.
- The tool logs executed commands and results for auditing purposes at `~/.systembot/app.log`
