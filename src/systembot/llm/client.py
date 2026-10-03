import logging

from ollama import Client

from systembot.llm import LLMCient, LLMRequest, LLMResponse

log = logging.getLogger(__name__)


class Ollama(LLMCient):
    def __init__(self) -> None:
        super().__init__()

    def chat(self, request: LLMRequest) -> LLMResponse | None:
        client = Client(host=self.host)

        try:
            response = client.chat(
                model=request.model,
                messages=request.messages,
                tools=request.tools,
                options=request.options,
            )
            return LLMResponse(
                message={
                    "role": response.message.role,
                    "content": response.message.content,
                },
                tool_calls=response.message.tool_calls,
            )
        except Exception as e:
            log.error(f"Failed to call model because of: {e}")
            return
