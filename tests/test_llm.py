import unittest
from unittest.mock import patch

from src.llm import LLMClient


class TestLLM(unittest.TestCase):
    def setUp(self):
        self.llm_client = LLMClient(model_name="qwen2.5-coder:14b")

    def test_get_commands_single_command(self):
        # Example user prompt
        user_prompt = "List all files in the current directory"

        # Expected generated commands
        expected_commands = ["ls"]

        # Get commands from the LLM client
        generated_commands = self.llm_client.get_commands(user_prompt)

        # Assert that the generated commands match the expected commands
        self.assertEqual(generated_commands, expected_commands)

    def test_get_commands_multiple_commands(self):
        # Example user prompt
        user_prompt = "Create a new directory named 'test_dir' and list its contents"

        # Expected generated commands
        expected_commands = ["mkdir test_dir", "ls test_dir"]

        # Get commands from the LLM client
        generated_commands = self.llm_client.get_commands(user_prompt)

        # Assert that the generated commands match the expected commands
        self.assertEqual(generated_commands, expected_commands)

    def test_get_commands_empty_response(self):
        # Example user prompt that should return an empty list of commands
        user_prompt = "This is a test prompt that should return no commands"

        # Expected generated commands
        expected_commands = []

        # Get commands from the LLM client
        generated_commands = self.llm_client.get_commands(user_prompt)

        # Assert that the generated commands match the expected commands
        self.assertEqual(generated_commands, expected_commands)

    @patch("src.llm.Client.generate")
    def test_get_commands_invalid_json(self, mock_generate):
        # Mock the response to return an invalid JSON string
        mock_response = mock_generate.return_value
        mock_response.response = "Invalid JSON response"

        # Example user prompt that should return an invalid JSON response
        user_prompt = "This is a test prompt that should return invalid JSON"

        # Assert that a ValueError is raised with the expected message
        with self.assertRaisesRegex(ValueError, "Failed to parse LLM response as JSON"):
            self.llm_client.get_commands(user_prompt)


if __name__ == "__main__":
    unittest.main()
