import logging
import sys

from yaml import safe_load

from agent import Bashbot

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger(__name__)


def load_config() -> dict:
    try:
        with open("config.yaml", "r") as config_file:
            log.debug(f"Reading the configuration from: {config_file.name}")
            config = safe_load(config_file)
        return config
    except FileNotFoundError as e:
        log.error(f"Config file not found: {e}")
        sys.exit(1)


def main():
    bashbot = Bashbot(config=load_config())
    response = bashbot.run(sys.argv[1])
    print("----\n")
    print(f"[SYSTEMBOT]: {response}")


if __name__ == "__main__":
    main()
