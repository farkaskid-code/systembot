import logging
import sys
from pathlib import Path

from yaml import safe_load

log = logging.getLogger(__name__)


def get_config() -> dict:
    paths = [Path.home() / ".systembot" / "config.yaml", Path("config.yaml")]

    for path in paths:
        try:
            with open(path, "r") as config_file:
                log.info(f"Reading the configuration from: {path}")
                config = safe_load(config_file)

            if "model" not in config:
                log.error(f"No model configuration found in {path}")
                sys.exit(1)

            return config
        except FileNotFoundError:
            log.debug(f"Config file not found at: {path}")

    log.error("No config file found")
    sys.exit(1)
