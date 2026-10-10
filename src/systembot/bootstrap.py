import logging
from argparse import Namespace
from dataclasses import dataclass, field
from sys import exit

import ollama
from openai import OpenAI
from rich.console import Console

from systembot.cli import parse_args
from systembot.config import DATAPATH, Config, LLMClient, read_config
from systembot.llm.client import Client, Ollama, OpenAICompat

console = Console()


@dataclass
class Runtime:
    config: Config = field(default_factory=lambda: read_config())
    args: Namespace = field(default_factory=lambda: parse_args())

    @property
    def client(self) -> Client:
        provider = (
            self.args.provider if self.args.provider else self.config.client.provider
        )
        host = self.args.base_url if self.args.base_url else self.config.client.base_url
        model = self.args.model if self.args.model else self.config.client.model
        if provider == "ollama":
            options = self.config.client.options
            return Ollama(client=ollama.Client(host=host), model=model, options=options)

        key = self.args.api_key if self.args.api_key else self.config.client.api_key

        return OpenAICompat(client=OpenAI(base_url=host, api_key=key), model=model)

    @property
    def query(self) -> str:
        return self.args.query

    @property
    def ctx_size(self) -> int:
        return self.config.client.options.get("num_ctx", 0)


def bootstrap() -> Runtime:
    runtime = Runtime()

    client_from_config = runtime.config.client
    client_from_args = LLMClient()
    client_from_args.from_args(runtime.args)

    # case: no config, no args
    if not client_from_config.valid() and not client_from_args.valid():
        msg = (
            "Initial run. No config file. Pass inference "
            "provider with -p, host URL with -u and model name with"
            " -m and api_key with -k if provider is 'openai-compat'"
        )
        console.print(msg, style="red")
        exit(1)

    # case: no config, args
    if not client_from_config.valid() and client_from_args.valid():
        runtime.config.client = client_from_args
        DATAPATH.mkdir()
        runtime.config.dump_yaml(DATAPATH / "config.yaml")

    logging.basicConfig(
        filename=DATAPATH / "app.log",
        filemode=runtime.config.logging.mode,
        level=runtime.config.logging.level,
    )
    return runtime


runtime = bootstrap()
