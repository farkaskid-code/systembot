import subprocess
import unittest
from unittest.mock import patch

from src.systembot.executor import CmdResult, execute


class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.config = {"command_timeout": 10, "blacklisted_commands": ["rm", "mv"]}

    @patch("subprocess.run")
    def test_execute_valid_command(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["echo", "hello"], returncode=0, stdout="hello\n", stderr=""
        )
        result = execute(self.config, "echo hello")
        expected_result = CmdResult(
            command="echo hello", return_code=0, stdout="hello\n", stderr=""
        ).json()
        self.assertEqual(result, expected_result)
        mock_run.assert_called_once_with(
            "echo hello",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

    @patch("subprocess.run")
    def test_execute_command_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="sleep 11", timeout=10)
        result = execute(self.config, "sleep 11")
        expected_result = CmdResult(
            command="sleep 11", return_code=1, stdout="", stderr="Command timed out\n"
        ).json()
        self.assertEqual(result, expected_result)
        mock_run.assert_called_once_with(
            "sleep 11",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

    @patch("subprocess.run")
    def test_execute_command_failure(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["ls", "/nonexistent"],
            returncode=2,
            stdout="",
            stderr="ls: /nonexistent: No such file or directory\n",
        )
        result = execute(self.config, "ls /nonexistent")
        expected_result = CmdResult(
            command="ls /nonexistent",
            return_code=2,
            stdout="",
            stderr="ls: /nonexistent: No such file or directory\n",
        ).json()
        self.assertEqual(result, expected_result)
        mock_run.assert_called_once_with(
            "ls /nonexistent",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

    @patch("src.systembot.executor.validate_command")
    def test_execute_blacklisted_command(self, mock_validate):
        mock_validate.return_value = ["rm"]
        result = execute(self.config, "rm -rf /")
        expected_result = CmdResult(
            command="rm -rf /",
            return_code=130,
            stderr="Following commands are blacklisted: ['rm']",
            stdout="",
        ).json()
        self.assertEqual(result, expected_result)
        mock_validate.assert_called_once_with(config=self.config, command="rm -rf /")


if __name__ == "__main__":
    unittest.main()
