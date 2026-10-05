import logging
from argparse import Namespace
from dataclasses import asdict, dataclass, field
from pathlib import Path
from sys import exit

from rich.console import Console
from yaml import YAMLError, safe_dump, safe_load

from systembot.cli import parse_args

log = logging.getLogger(__name__)

DATAPATH = Path.home() / ".systembot"

console = Console()


@dataclass
class LLMClient:
    provider: str
    host: str
    model: str
    api_key: str = "ollama"
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
    args: Namespace = None

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

        if "client" in data:
            client_data = data["client"]
            self.client = LLMClient(
                provider=client_data["provider"],
                host=client_data["host"],
                model=client_data["model"],
                options=client_data["options"],
            )
            if "api_key" in client_data:
                self.client.api_key = client_data["api_key"]

        if "logging" in data:
            logging_data = data["logging"]
            self.logging = Logging(
                level=logging_data["level"], mode=logging_data["mode"]
            )

        if "max_turns" in data:
            self.max_turns = data["max_turns"]

        if "command_timeout" in data:
            self.command_timeout = data["command_timeout"]

        if "blacklist" in data:
            self.blacklist = data["blacklist"]

    def from_args(self, args: Namespace):
        self.args = args

        if not self.client:
            all_params = args.provider and args.url and args.model
            if args.provider == "openai-compat":
                all_params = all_params and args.api_key

            if not all_params:
                raise ConfigError(
                    "Need provider, url and model. Also need api_key if provider is 'openai-compat'"
                )
            self.client = LLMClient(
                host=args.url, model=args.model, provider=args.provider
            )
            if args.provider == "openai-compat":
                self.client.api_key = args.api_key
        else:
            if args.url:
                self.client.host = args.url
            if args.model:
                self.client.model = args.model
            if args.provider:
                self.client.provider = args.provider
            if args.api_key:
                self.client.api_key = args.api_key

    def dump_yaml(self, path: Path):
        to_dump = {
            "client": asdict(self.client),
            "blacklist": self.blacklist,
            "logging": asdict(self.logging),
            "max_turns": self.max_turns,
            "command_timeout": self.command_timeout,
        }
        try:
            with open(path, "w") as config_file:
                safe_dump(to_dump, config_file)
        except (YAMLError, OSError, PermissionError) as e:
            msg = f"Failed to create the config file: {path} because: {e}"
            log.error(msg)
            raise ConfigError(msg)


def bootstrap() -> Config:
    config_path = DATAPATH / "config.yaml"
    args = parse_args()

    config = Config()

    try:
        if not DATAPATH.exists():
            if args.provider is None or args.url is None or args.model is None:
                msg = (
                    "Initial run. No config file. Pass inference "
                    "provider with -p, host URL with -u and model name with"
                    " -m and api_key with -k with provider is 'openai-compat'"
                )
                console.print(msg, style="red")
                exit(1)
            config.from_args(args)
            DATAPATH.mkdir()
            config.dump_yaml(config_path)
        else:
            config.from_yaml(config_path)
            config.from_args(args)
    except ConfigError as e:
        console.print(e, style="red")
        exit(1)

    logging.basicConfig(
        filename=DATAPATH / "app.log",
        filemode=config.logging.mode,
        level=config.logging.level,
    )
    return config


settings = bootstrap()
