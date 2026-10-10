import logging
from dataclasses import dataclass, field

from systembot.llm.client import Message

log = logging.getLogger(__name__)


@dataclass
class Interaction:
    model_msg: Message
    reply_msg: Message
    ctx_size: int = -1


@dataclass
class Context:
    cap: int = 0
    size: int = 0
    dropped: int = 0
    history: list[Interaction] = field(default_factory=list)

    def add(self, interaction: Interaction):
        self.history.append(interaction)

    def get_messages(self) -> list[dict]:
        if self.cap != 0:
            while self.size > self.cap:
                self.size -= self.history[self.dropped + 1].ctx_size
                self.dropped += 1
                log.debug(f"Dropped turn: {self.dropped} from the context history")

        messages = []
        for interaction in [self.history[0], *self.history[self.dropped + 1 :]]:
            messages.append(interaction.model_msg.asdict())
            messages.append(interaction.reply_msg.asdict())

        return messages
