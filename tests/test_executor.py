import unittest
from unittest.mock import patch, mock_open
from src.executor import execute_commands, CmdResult
from subprocess import TimeoutExpired, CalledProcessError

class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.config = {"timeout": 10}

    @patch("subprocess.run")
    def test_single_valid_command(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["echo", "hello"], returncode=0, stdout="hello\n", stderr="")
        result = execute_commands(self.config, ["echo hello"])
        expected = [CmdResult(command="echo hello", return_code=0, stdout="hello\n", stderr="")]
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_multiple_valid_commands(self, mock_run):
        mock_run.side_effect = [
            subprocess.CompletedProcess(args=["echo", "hello"], returncode=0, stdout="hello\n", stderr=""),
            subprocess.CompletedProcess(args=["echo", "world"], returncode=0, stdout="world\n", stderr="")
        ]
        result = execute_commands(self.config, ["echo hello", "echo world"])
        expected = [
            CmdResult(command="echo hello", return_code=0, stdout="hello\n", stderr=""),
            CmdResult(command="echo world", return_code=0, stdout="world\n", stderr="")
        ]
        self.assertEqual(result, expected)

    def test_empty_command_list(self):
        result = execute_commands(self.config, [])
        expected = []
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_single_command_fails(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["invalid_command"], returncode=1, stdout="", stderr="command not found\n")
        result = execute_commands(self.config, ["invalid_command"])
        expected = [CmdResult(command="invalid_command", return_code=1, stdout="", stderr="command not found\n")]
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_multiple_commands_some_fail(self, mock_run):
        mock_run.side_effect = [
            subprocess.CompletedProcess(args=["echo", "hello"], returncode=0, stdout="hello\n", stderr=""),
            subprocess.CompletedProcess(args=["invalid_command"], returncode=1, stdout="", stderr="command not found\n")
        ]
        result = execute_commands(self.config, ["echo hello", "invalid_command"])
        expected = [
            CmdResult(command="echo hello", return_code=0, stdout="hello\n", stderr=""),
            CmdResult(command="invalid_command", return_code=1, stdout="", stderr="command not found\n")
        ]
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_command_times_out(self, mock_run):
        mock_run.side_effect = TimeoutExpired(cmd=["sleep", "10"], timeout=10)
        result = execute_commands(self.config, ["sleep 10"])
        expected = [CmdResult(command="sleep 10", return_code=1, stdout="", stderr="Command timed out\n")]
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_command_generates_exception(self, mock_run):
        mock_run.side_effect = CalledProcessError(returncode=1, cmd=["invalid_command"], output="", stderr="command not found\n")
        result = execute_commands(self.config, ["invalid_command"])
        expected = [CmdResult(command="invalid_command", return_code=1, stdout="", stderr="command not found\n")]
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_command_no_output(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["true"], returncode=0, stdout="", stderr="")
        result = execute_commands(self.config, ["true"])
        expected = [CmdResult(command="true", return_code=0, stdout="", stderr="")]
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_command_only_stderr_output(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["echo", "error"], returncode=1, stdout="", stderr="error\n")
        result = execute_commands(self.config, ["echo error"])
        expected = [CmdResult(command="echo error", return_code=1, stdout="", stderr="error\n")]
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_command_both_stdout_and_stderr_output(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["echo", "hello"], returncode=0, stdout="hello\n", stderr="info\n")
        result = execute_commands(self.config, ["echo hello"])
        expected = [CmdResult(command="echo hello", return_code=0, stdout="hello\n", stderr="info\n")]
        self.assertEqual(result, expected)
