import unittest
from unittest.mock import patch, Mock
from src.systembot.agent import Bashbot
from src.systembot.config import get_config

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.config = get_config()
        self.agent = Bashbot(config=self.config)

    @patch("ollama.Client.chat")
    def test_run_no_tool_calls(self, mock_chat):
        mock_response = Mock()
        mock_response.message.content = "No tool calls required"
        mock_response.message.tool_calls = []
        mock_chat.return_value = mock_response

        result = self.agent.run("What is the weather?")

        self.assertEqual(result, "No tool calls required")
        mock_chat.assert_called_once()

    @patch("ollama.Client.chat")
    @patch("src.systembot.executor.execute")
    def test_run_with_tool_calls(self, mock_execute, mock_chat):
        mock_response = Mock()
        mock_response.message.content = "Executing command"
        mock_response.message.tool_calls = [
            {
                "function": {
                    "name": "execute_command",
                    "arguments": {"cmd": "echo Hello"}
                }
            }
        ]
        mock_chat.return_value = mock_response
        mock_execute.return_value = "Hello"

        result = self.agent.run("What is the weather?")

        self.assertEqual(result, "Hello")
        mock_chat.assert_called_once()
        mock_execute.assert_called_once_with(config=self.config, cmd="echo Hello")

    @patch("ollama.Client.chat")
    def test_run_max_turns_exceeded(self, mock_chat):
        mock_response = Mock()
        mock_response.message.content = "Executing command"
        mock_response.message.tool_calls = [
            {
                "function": {
                    "name": "execute_command",
                    "arguments": {"cmd": "echo Hello"}
                }
            }
        ]
        mock_chat.return_value = mock_response

        with patch.object(self.agent, 'max_turns', new=1):
            result = self.agent.run("What is the weather?")

        self.assertEqual(result, "Failed to call the model after 1 tries")
        mock_chat.assert_called_once()

    @patch("ollama.Client.chat")
    def test_run_tool_not_found(self, mock_chat):
        mock_response = Mock()
        mock_response.message.content = "Executing command"
        mock_response.message.tool_calls = [
            {
                "function": {
                    "name": "non_existent_tool",
                    "arguments": {"cmd": "echo Hello"}
                }
            }
        ]
        mock_chat.return_value = mock_response

        result = self.agent.run("What is the weather?")

        self.assertEqual(result, "Tool not found")
        mock_chat.assert_called_once()

if __name__ == '__main__':
    unittest.main()
