# systembot

## Overview
`systembot` is a CLI tool that acts as a bridge between natural language instructions and shell execution, using a local LLM for command generation and analysis. It ensures safe execution of commands by validating them against a configurable blacklist.

## Prerequisites
- Ollama server running with the desired model.
- Python 3.x installed.
- UV package manager installed.

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

## Configuration
Create a configuration file at `~/.systembot/config.yaml` with the following content:
```yaml
blacklist: # Optional but recommended for safety guardrails
  - rm
  - shutdown
  - reboot
  - dd
  - mkfs

model: # Required: it needs an Ollama server to work
  host: http://{ollama-server-host}:11434
  name: qwen3:14b # A model that supports tool calling
  num_ctx: 16384 # Optional
```

## Usage
Run the tool with a natural language prompt:
```bash
systembot "natural language prompt"
```

## Example
```bash
$ systembot "why is the system feeling slow?"
[SYSTEM] Running: top -b -n 1
[SYSTEM] Running: iostat -d 1 2
[SYSTEM] Running: journalctl --since "24 hours ago"
[SYSTEM] Analysis:
- High CPU usage from process 'SomeResourceHog' (PID 1234) is likely causing the slowness
- Memory was low 24 hours ago, but disk I/O is normal
```

## Notes
- Commands are validated before execution to prevent blacklisted commands from running.
- The tool logs executed commands and results for auditing purposes at `~/.systembot/app.log`
