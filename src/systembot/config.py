from argparse import Namespace
from dataclasses import asdict, dataclass, field
from pathlib import Path

from rich.console import Console
from yaml import YAMLError, safe_dump, safe_load

DATAPATH = Path.home() / ".systembot"

console = Console()


@dataclass
class LLMClient:
    provider: str = None
    base_url: str = None
    model: str = None
    api_key: str = None
    options: dict = field(default_factory=dict)

    def valid(self) -> bool:
        if not self.provider:
            return False

        provider = self.provider

        if provider == "openai-compat" and not self.api_key:
            return False

        if not self.base_url:
            return False

        return self.model is not None

    def from_args(self, args: Namespace):
        self.provider = args.provider
        self.base_url = args.base_url
        self.model = args.model
        self.api_key = args.api_key


@dataclass
class Logging:
    level: str = "INFO"
    mode: str = "w"


class ConfigError(RuntimeError):
    pass


@dataclass
class Config:
    client: LLMClient = field(default_factory=LLMClient)
    blacklist: list = field(default_factory=list)
    logging: Logging = field(default_factory=Logging)
    max_turns: int = 6
    command_timeout: int = 10

    def dump_yaml(self, path: Path):
        console.print(f"Creating config file at: {path}", style="blue")
        try:
            with open(path, "w") as config_file:
                safe_dump(asdict(self), config_file)
        except (YAMLError, OSError, PermissionError) as e:
            msg = f"Failed to create the config file: {path} because: {e}"
            console.print(msg, style="red")


def read_config() -> Config:
    path = DATAPATH / "config.yaml"
    config = Config()
    data = {}

    try:
        with open(path, "r") as config_file:
            data = safe_load(config_file)
    except FileNotFoundError:
        msg = f"Config file not found at: {path}"
        console.print(msg, style="yellow")
        return config

    if "client" in data:
        client_data = data["client"]
        config.client = LLMClient(
            provider=client_data["provider"],
            base_url=client_data["base_url"],
            model=client_data["model"],
            options=client_data["options"],
        )
        if "api_key" in client_data:
            config.client.api_key = client_data["api_key"]

    if "logging" in data:
        logging_data = data["logging"]
        config.logging = Logging(level=logging_data["level"], mode=logging_data["mode"])

    if "max_turns" in data:
        config.max_turns = data["max_turns"]

    if "command_timeout" in data:
        config.command_timeout = data["command_timeout"]

    if "blacklist" in data:
        config.blacklist = data["blacklist"]

    return config
