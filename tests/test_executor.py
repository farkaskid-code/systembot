import subprocess
import unittest
from subprocess import CalledProcessError, TimeoutExpired
from unittest.mock import patch

from src.executor import CmdResult, execute_commands


class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.config = {"timeout": 10}

    @patch("subprocess.run")
    def test_single_valid_command(self, mock_run):
        # Mock the subprocess.run to return a successful command result
        mock_run.return_value = subprocess.CompletedProcess(
            args=["echo", "hello"], returncode=0, stdout="hello\n", stderr=""
        )
        # Execute the single valid command
        result = execute_commands(self.config, ["echo hello"])
        # Define the expected CmdResult object
        expected = [
            CmdResult(command="echo hello", return_code=0, stdout="hello\n", stderr="")
        ]
        # Assert that the result matches the expected output
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_multiple_valid_commands(self, mock_run):
        # Mock the subprocess.run to return multiple successful command results
        mock_run.side_effect = [
            subprocess.CompletedProcess(
                args=["echo", "hello"], returncode=0, stdout="hello\n", stderr=""
            ),
            subprocess.CompletedProcess(
                args=["echo", "world"], returncode=0, stdout="world\n", stderr=""
            ),
        ]
        # Execute the multiple valid commands
        result = execute_commands(self.config, ["echo hello", "echo world"])
        # Define the expected CmdResult objects
        expected = [
            CmdResult(command="echo hello", return_code=0, stdout="hello\n", stderr=""),
            CmdResult(command="echo world", return_code=0, stdout="world\n", stderr=""),
        ]
        # Assert that the result matches the expected output
        self.assertEqual(result, expected)

    def test_empty_command_list(self):
        # Execute an empty command list
        result = execute_commands(self.config, [])
        # Define the expected empty list
        expected = []
        # Assert that the result matches the expected output
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_single_command_fails(self, mock_run):
        # Mock the subprocess.run to return a failed command result
        mock_run.return_value = subprocess.CompletedProcess(
            args=["invalid_command"],
            returncode=1,
            stdout="",
            stderr="command not found\n",
        )
        # Execute the single failing command
        result = execute_commands(self.config, ["invalid_command"])
        # Define the expected CmdResult object
        expected = [
            CmdResult(
                command="invalid_command",
                return_code=1,
                stdout="",
                stderr="command not found\n",
            )
        ]
        # Assert that the result matches the expected output
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_multiple_commands_some_fail(self, mock_run):
        # Mock the subprocess.run to return multiple command results, some successful, some failed
        mock_run.side_effect = [
            subprocess.CompletedProcess(
                args=["echo", "hello"], returncode=0, stdout="hello\n", stderr=""
            ),
            subprocess.CompletedProcess(
                args=["invalid_command"],
                returncode=1,
                stdout="",
                stderr="command not found\n",
            ),
        ]
        # Execute the multiple commands
        result = execute_commands(self.config, ["echo hello", "invalid_command"])
        # Define the expected CmdResult objects
        expected = [
            CmdResult(command="echo hello", return_code=0, stdout="hello\n", stderr=""),
            CmdResult(
                command="invalid_command",
                return_code=1,
                stdout="",
                stderr="command not found\n",
            ),
        ]
        # Assert that the result matches the expected output
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_command_times_out(self, mock_run):
        # Mock the subprocess.run to raise a TimeoutExpired exception
        mock_run.side_effect = TimeoutExpired(cmd=["sleep", "10"], timeout=10)
        # Execute the command that times out
        result = execute_commands(self.config, ["sleep 10"])
        # Define the expected CmdResult object
        expected = [
            CmdResult(
                command="sleep 10",
                return_code=1,
                stdout="",
                stderr="Command timed out\n",
            )
        ]
        # Assert that the result matches the expected output
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_command_generates_exception(self, mock_run):
        # Mock the subprocess.run to raise a CalledProcessError exception
        mock_run.side_effect = CalledProcessError(
            returncode=1,
            cmd=["invalid_command"],
            output="",
            stderr="command not found\n",
        )
        # Execute the command that generates an exception
        result = execute_commands(self.config, ["invalid_command"])
        # Define the expected CmdResult object
        expected = [
            CmdResult(
                command="invalid_command",
                return_code=1,
                stdout="",
                stderr="command not found\n",
            )
        ]
        # Assert that the result matches the expected output
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_command_no_output(self, mock_run):
        # Mock the subprocess.run to return a command result with no output
        mock_run.return_value = subprocess.CompletedProcess(
            args=["true"], returncode=0, stdout="", stderr=""
        )
        # Execute the command with no output
        result = execute_commands(self.config, ["true"])
        # Define the expected CmdResult object
        expected = [CmdResult(command="true", return_code=0, stdout="", stderr="")]
        # Assert that the result matches the expected output
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_command_only_stderr_output(self, mock_run):
        # Mock the subprocess.run to return a command result with only stderr output
        mock_run.return_value = subprocess.CompletedProcess(
            args=["echo", "error"], returncode=1, stdout="", stderr="error\n"
        )
        # Execute the command with only stderr output
        result = execute_commands(self.config, ["echo error"])
        # Define the expected CmdResult object
        expected = [
            CmdResult(command="echo error", return_code=1, stdout="", stderr="error\n")
        ]
        # Assert that the result matches the expected output
        self.assertEqual(result, expected)

    @patch("subprocess.run")
    def test_command_both_stdout_and_stderr_output(self, mock_run):
        # Mock the subprocess.run to return a command result with both stdout and stderr output
        mock_run.return_value = subprocess.CompletedProcess(
            args=["echo", "hello"], returncode=0, stdout="hello\n", stderr="info\n"
        )
        # Execute the command with both stdout and stderr output
        result = execute_commands(self.config, ["echo hello"])
        # Define the expected CmdResult object
        expected = [
            CmdResult(
                command="echo hello", return_code=0, stdout="hello\n", stderr="info\n"
            )
        ]
        # Assert that the result matches the expected output
        self.assertEqual(result, expected)
