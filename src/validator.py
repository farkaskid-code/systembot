import logging

import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigError(RuntimeError):
    pass


def load_config() -> dict:
    try:
        with open("config.yaml", "r") as config_file:
            logger.debug(f"Reading the configuration from: {config_file.name}")
            config = yaml.safe_load(config_file)
        return config
    except FileNotFoundError as e:
        logger.error(f"Config file not found: {e}")
        raise ConfigError(f"Config file not found: {e}")


def validate_commands(generated_commands: list[str]) -> list[str]:
    logger.debug("Validating commands against blacklist")
    config = load_config()

    if "blacklist" not in config:
        logger.error("Faulty config file")
        raise ConfigError("Faulty config file")

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
