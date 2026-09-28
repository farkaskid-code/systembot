import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_commands(config: dict, generated_commands: list[str]) -> list[str]:
    logger.debug("Validating commands against blacklist")

    if "blacklist" not in config:
        logger.error("Faulty config file")

    blacklist = config.get("blacklist", [])

    valid_commands = []
    for command in generated_commands:
        parts = command.split()
        if not parts:
            continue

        cmd = parts[0]
        if cmd in blacklist:
            logger.error(f"Command '{cmd}' is blacklisted and will be skipped.")
            continue

        valid_commands.append(command)

    logger.debug(f"Validated commands: {valid_commands}")
    return valid_commands
