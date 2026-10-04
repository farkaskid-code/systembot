import logging
from argparse import Namespace
from dataclasses import asdict, dataclass, field
from pathlib import Path
from sys import exit

from yaml import YAMLError, safe_dump, safe_load

from systembot.cli import parse_args

log = logging.getLogger(__name__)

DATAPATH = Path.home() / ".systembot"


@dataclass
class LLMClient:
    host: str
    model: str
    options: dict = field(default_factory=dict)


@dataclass
class Logging:
    level: str = "INFO"
    mode: str = "w"


class ConfigError(RuntimeError):
    pass


@dataclass
class Config:
    client: LLMClient = None
    blacklist: list = field(default_factory=list)
    logging: Logging = field(default_factory=Logging)
    max_turns: int = 6
    command_timeout: int = 10

    def from_yaml(self, path: Path):
        data = {}
        try:
            with open(path, "r") as config_file:
                log.info(f"Reading the configuration from: {path}")
                data = safe_load(config_file)
        except FileNotFoundError:
            msg = f"Config file not found at: {path}"
            log.error(msg)
            raise ConfigError(msg)

        if "model" in data:
            model_data = data["model"]
            self.client = LLMClient(
                host=model_data["host"],
                model=model_data["name"],
                options=model_data["options"],
            )

        if "logging" in data:
            logging_data = data["logging"]
            self.logging = Logging(
                level=logging_data["level"], mode=logging_data["mode"]
            )

        if "max_turns" in data:
            self.max_turns = data["max_turns"]

        if "command_timeout" in data:
            self.command_timeout = data["command_timeout"]

    def from_args(self, args: Namespace):
        if args.url and args.model:
            if not self.client:
                self.client = LLMClient(host=args.url, model=args.model)
            else:
                self.client.host = args.url
                self.client.model = args.model

    def dump_yaml(self, path: Path):
        try:
            with open(path, "w") as config_file:
                safe_dump(asdict(self), config_file)
        except (YAMLError, OSError, PermissionError) as e:
            msg = f"Failed to create the config file: {path} because: {e}"
            log.error(msg)
            raise ConfigError(msg)


def bootstrap() -> Config:
    config_path = DATAPATH / "config.yaml"
    args = parse_args()

    config = Config()

    if not DATAPATH.exists():
        if args.url is None or args.model is None:
            print(
                "Initial run. No config file. Pass Ollama host URL with -u and model name with -m"
            )
            exit(1)
        config.from_args(args)
        DATAPATH.mkdir()
        config.dump_yaml(config_path)
    else:
        config.from_yaml(config_path)
        config.from_args(args)

    logging.basicConfig(
        filename=DATAPATH / "app.log",
        filemode=config.logging.mode,
        level=config.logging.level,
    )
    return config


settings = bootstrap()
