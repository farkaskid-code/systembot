# systembot CLI Tool Specification

## What & Why
- A one-shot CLI tool that acts as a bridge between natural language instructions and shell execution, using a local LLM for both command generation and analysis.
- For users who want to automate system tasks or analyze system states via natural language without writing shell scripts or understanding technical details.
- Designed to be **agent-agnostic** (no assumptions about intent) and **safe** (commands are validated before execution).

---

## Scope
**In**
- CLI interface that takes a single natural language prompt as input
- Command generation by a local LLM (e.g., Ollama)
- Safe execution of generated shell commands
- Output of command results to the LLM for analysis
- Natural language response from the LLM displayed to the user

**Out**
- Web interface (for now)
- Multi-user support
- Complex task orchestration (e.g., workflows, plugins)

**Maybe Later**
- Persistent memory across sessions
- Interactive mode with follow-up prompts
- Plugin system for extending command capabilities

---

## Core Features
**Must-have**
- CLI interface: `systembot "natural language prompt"`
- LLM integration for command generation and analysis
- Safe command execution with validation
- Output of execution results to the LLM for analysis
- Natural language response to the user

**Nice-to-have**
- Pretty terminal output (e.g., with `rich`)
- Logging of executed commands and results
- Configurable command whitelist/blacklist

---

## Architecture Snapshot
```
[User Prompt] --> [LLM (Ollama)] 
              --> [Generated Commands] 
              --> [Command Validator] 
              --> [Shell Executor] 
              --> [Command Output] 
              --> [LLM (Ollama)] 
              --> [Natural Language Analysis] 
              --> [User Terminal]
```

**Tech Stack:**
- **Python 3.11+** (for `subprocess`, `ollama`, and `argparse`)
- **Ollama** (for local LLM inference)
- **subprocess** (for shell command execution)
- **argparse** (for CLI argument parsing)
- **rich** (optional, for enhanced terminal output)

---

## Build vs Existing Tools
| Part               | Build or Use Existing? | Tool / Service     | Notes |
|---------------------|------------------------|--------------------|-------|
| LLM Inference       | Use Existing           | Ollama             | Local model serving (e.g., `llama3`) |
| Shell Execution     | Build                  | Python `subprocess`| Safe implementation required |
| CLI Parsing         | Build                  | Python `argparse`  | For single-argument input |
| Terminal Output     | Use Existing           | `rich`             | Optional, for better formatting |
| Command Validation  | Build                  | Custom logic       | Whitelist allowed commands |

---

## Data
- **Key Entities:**
  - `user_prompt`: Natural language input from the user
  - `generated_commands`: List of shell commands from the LLM
  - `command_outputs`: Results of executed commands
  - `analysis`: Natural language analysis from the LLM based on command outputs

- **Relationships:**
  - 1 `user_prompt` → 1+ `generated_commands`
  - 1+ `generated_commands` → 1+ `command_outputs`
  - 1+ `command_outputs` → 1 `analysis`

---

## Notes for Building
### **Implementation Order**
1. **CLI Parsing**: Use `argparse` to handle the single input argument.
2. **LLM Integration**: Use the Ollama Python client to send prompts and receive responses.
3. **Command Validation**: Implement a whitelist of allowed commands (e.g., `find`, `ls`, `mkdir`).
4. **Command Execution**: Use `subprocess.run()` with `capture_output=True` and `timeout`.
5. **Output Analysis**: Send command outputs back to the LLM for analysis.
6. **Final Output**: Display the LLM's analysis to the user in natural language.

### **Keep Simple**
- Start with a minimal command whitelist (e.g., `find`, `ls`, `mkdir`, `mv`, `rm`).
- Avoid complex logic in the agent (it should be a passive relay).
- Use `subprocess.run()` with `shell=False` to avoid shell injection risks.

### **Known Risks**
- **Model Hallucination**: The LLM may generate invalid or dangerous commands.
  - Mitigation: Use a strict command whitelist and validate all commands before execution.
- **Command Output Size**: Large outputs could cause memory issues or DoS.
  - Mitigation: Truncate outputs to a reasonable size (e.g., 10,000 characters).
- **User Misunderstanding**: The LLM may misinterpret the user's intent.
  - Mitigation: The agent does not interpret the user's intent — it only executes commands.

---

## Interaction Style
- **One-shot**: The user provides a single prompt, and the tool completes the task in one go.
- **No Chat State**: No memory of previous interactions or context.
- **Natural Language**: All input and output is in natural language (no shell syntax required).
- **Safe by Default**: The agent validates all commands before execution.

---

## Example Workflow
```bash
$ systembot "why is the system feeling slow?"
[SYSTEM] Running: top -b -n 1
[SYSTEM] Running: iostat -d 1 2
[SYSTEM] Running: journalctl --since "24 hours ago"
[SYSTEM] Analysis:
- High CPU usage from process 'SomeResourceHog' (PID 1234) is likely causing the slowness
- Memory was low 24 hours ago, but disk I/O is normal
