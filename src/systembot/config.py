import logging
import sys
from argparse import Namespace
from pathlib import Path

from yaml import YAMLError, safe_dump, safe_load

log = logging.getLogger(__name__)

PATH = Path.home() / ".systembot" / "config.yaml"


def get_config() -> dict:
    try:
        with open(PATH, "r") as config_file:
            log.info(f"Reading the configuration from: {PATH}")
            config = safe_load(config_file)

        if "model" not in config:
            log.error(f"No model configuration found in {PATH}")
            sys.exit(1)

        return config
    except FileNotFoundError:
        log.debug(f"Config file not found at: {PATH}")

    log.error("No config file found")
    sys.exit(1)


def create_basic_config(args: Namespace):
    if args.url is None or args.model is None:
        print(
            "Initial run. No config file. Pass Ollama host URL with -u and model name with -m"
        )
        sys.exit(1)

    config = {
        "model": {"host": args.url, "name": args.model},
        "logging": {"level": "INFO", "mode": "w"},
    }

    try:
        with open(PATH, "w") as config_file:
            safe_dump(config, config_file)
    except (YAMLError, OSError, PermissionError) as e:
        log.error(f"Failed to create the config file: {PATH} because: {e}")
        sys.exit(1)

    log.info(f"Created a basic config file: {PATH}")
    return config
