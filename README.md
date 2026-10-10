# systembot

## Overview
`systembot` is a CLI tool that acts as a bridges natural language instructions and shell execution, using a local Ollama server or any OpenAI compatible inference service for command generation and analysis. It ensures safe execution of commands by validating them against a configurable blacklist.

## Prerequisites
- An Ollama server running with the desired model for local use or an OpenAI compatible inference service account.
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
You need a tool calling model for this to work, it's required. Once setup, just run,
```bash
systembot -p {provider} -u {inference API url} -m {model-name} -k {api_key} "hello"
```

to do a test run. This will create a basic config file at `~/.systembot/config.yaml`.
Once the configuration file is there, you don't need to pass the, `-p`, `-u` and `-m` flags.
Simply go,
```bash
systembot "what's my IP?"
```

## CLI Reference
Following are the available flag,

- `-p` or `--provider`: Can either be `ollama` or `openai-compat`. `ollama` is for running with local inference setups with ollama and `openai-compat` is for running with inference API services that support the OpenAI format.
- `-u` or `--base_url`: Base url for the inference server.
- `-m` or `--model`: The name of the model to be used.
- `-k` or `--api_key`: API key when using `openai-compat` provider. This is not needed when `ollama` provider is used.

As mentioned above, you don't to pass any of these flags when the configuration file is present. If you pass flags and config file is present, then the flags with override the information from the config file. 

## Configuration Reference
Configuration file is at `~/.systembot/config.yaml` with the following content:
```yaml
client: # Required: it needs an Ollama server to work
  provider: ollama # can be 'ollama' or 'openai-compat' for public inference servers
  base_url: http://{ollama-server-host}:11434
  model: qwen3:14b # A model that supports tool calling
  options: {} # model params like num_ctx, temperature. Only effective when using 'ollama' provider
  api_key: <key> # API key required for using public inference servers
  

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

**Context Management:** When `num_ctx` option is provided in client options, it will be used as context token budget for the internal chat loop.

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
