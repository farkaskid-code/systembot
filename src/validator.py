import logging

log = logging.getLogger(__name__)


def validate_command(config: dict, command: str) -> list[str]:
    commands = command.strip().split("&&")
    log.debug("Validating commands against blacklist")

    if "blacklist" not in config:
        log.error("No commands are blacklisted, consider adding some")

    blacklist = config.get("blacklist", ["rm", "shutdown", "reboot", "dd", "mkfs"])

    invalid_commands = []
    for cmd in commands:
        parts = cmd.split()
        if not parts:
            continue

        cmd_bin = parts[0]
        if cmd_bin in blacklist:
            log.error(f"Command '{cmd_bin}' is blacklisted and will be skipped.")
            invalid_commands.append(cmd_bin)

    log.debug(f"Invalid commands: {invalid_commands}")
    return invalid_commands
