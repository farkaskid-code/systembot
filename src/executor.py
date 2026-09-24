import subprocess

def execute_commands(valid_commands):
    command_outputs = []
    for cmd in valid_commands:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        command_outputs.append(result.stdout)
    return command_outputs
