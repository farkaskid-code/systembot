def validate_commands(generated_commands):
    allowed_commands = {"find", "ls", "mkdir", "mv", "rm"}
    valid_commands = [cmd for cmd in generated_commands if any(cmd.startswith(allowed) for allowed in allowed_commands)]
    return valid_commands
