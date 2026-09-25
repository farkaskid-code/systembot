import unittest
from unittest.mock import mock_open, patch

from src.validator import ConfigError, validate_commands


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.blacklist = ["rm", "shutdown", "reboot", "dd", "mkfs"]

    @patch("src.validator.load_config")
    def test_validate_commands_no_commands(self, mock_load_config):
        mock_load_config.return_value = {"blacklist": self.blacklist}
        generated_commands = []
        valid_commands = validate_commands(generated_commands)
        self.assertEqual(valid_commands, [])

    @patch("src.validator.load_config")
    def test_validate_commands_all_valid(self, mock_load_config):
        mock_load_config.return_value = {"blacklist": self.blacklist}
        generated_commands = ["ls -l", "echo Hello", "cat file.txt"]
        valid_commands = validate_commands(generated_commands)
        self.assertEqual(valid_commands, generated_commands)

    @patch("src.validator.load_config")
    def test_validate_commands_all_blacklisted(self, mock_load_config):
        mock_load_config.return_value = {"blacklist": self.blacklist}
        generated_commands = [
            "rm file.txt",
            "shutdown now",
            "reboot",
            "dd if=/dev/zero of=/dev/null",
            "mkfs /dev/sda",
        ]
        valid_commands = validate_commands(generated_commands)
        self.assertEqual(valid_commands, [])

    @patch("src.validator.load_config")
    def test_validate_commands_mixed_valid_and_blacklisted(self, mock_load_config):
        mock_load_config.return_value = {"blacklist": self.blacklist}
        generated_commands = ["ls -l", "rm file.txt", "echo Hello", "shutdown now"]
        valid_commands = validate_commands(generated_commands)
        self.assertEqual(valid_commands, ["ls -l", "echo Hello"])

    @patch("src.validator.load_config")
    def test_validate_commands_empty_command(self, mock_load_config):
        mock_load_config.return_value = {"blacklist": self.blacklist}
        generated_commands = ["", "ls -l", "rm file.txt"]
        valid_commands = validate_commands(generated_commands)
        self.assertEqual(valid_commands, ["ls -l"])

    @patch("src.validator.load_config")
    def test_validate_commands_whitespace_command(self, mock_load_config):
        mock_load_config.return_value = {"blacklist": self.blacklist}
        generated_commands = ["   ", "ls -l", "rm file.txt"]
        valid_commands = validate_commands(generated_commands)
        self.assertEqual(valid_commands, ["ls -l"])

    @patch(
        "builtins.open",
        new_callable=mock_open,
    )
    def test_validate_commands_config_not_found(self, mock_open):
        mock_open.side_effect = FileNotFoundError("Config file not found")
        with self.assertRaises(ConfigError) as context:
            validate_commands([])
        self.assertEqual(
            str(context.exception), "Config file not found: Config file not found"
        )

    @patch("src.validator.load_config", return_value={})
    def test_validate_commands_faulty_config(self, mock_load_config):
        with self.assertRaises(ConfigError) as context:
            validate_commands([])
        self.assertEqual(str(context.exception), "Faulty config file")


if __name__ == "__main__":
    unittest.main()
