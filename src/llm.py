import logging
from json import JSONDecodeError, loads
from os import getenv

from ollama import Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, model_name: str) -> None:
        self.model = model_name
        self.client = Client(host=getenv("OLLAMA_API_BASE"))

    def get_commands(self, user_prompt: str):
        # Placeholder for sending user_prompt to the LLM and receiving generated_commands

        system_prompt = "You are a command generator. Generate a list of shell commands based on the user's input. Respond as a JSON array with each command as a string element"
        logger.debug(f"Sending prompt to LLM: {user_prompt}")
        response = self.client.generate(
            model=self.model, prompt=user_prompt, system=system_prompt
        )
        logger.debug(f"LLM response: {response.response}")

        if response.response.startswith("```"):
            response_json = "\n".join(response.response.splitlines()[1:-1])
        else:
            response_json = response.response

        try:
            generated_commands = loads(response_json)
            logger.debug(f"Parsed commands: {generated_commands}")
            if isinstance(generated_commands, list):
                return generated_commands
            else:
                raise TypeError("LLM response is not a list")
        except JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError("Failed to parse LLM response as JSON") from e
        except TypeError as e:
            logger.error(f"Invalid response from LLM: {e}")
            raise ValueError(f"Invalid response from LLM: {e}")

    def get_analysis(self, command_outputs):
        # Placeholder for sending command_outputs back to the LLM and receiving analysis
        analysis = "The commands were executed successfully."
        return analysis
