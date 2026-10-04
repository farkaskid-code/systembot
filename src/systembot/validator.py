import logging

from systembot.config import settings

log = logging.getLogger(__name__)


def validate_command(command: str) -> list[str]:
    commands = command.strip().split("&&")
    log.debug("Validating commands against blacklist")

    blacklist = settings.blacklist
    if len(blacklist) == 0:
        log.warning("No commands are blacklisted, consider adding some")
        blacklist = ["rm", "shutdown", "reboot", "dd", "mkfs"]

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
