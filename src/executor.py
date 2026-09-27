import logging
import subprocess
from json import dumps
from typing import NamedTuple

logger = logging.getLogger(__name__)


class CmdResult(NamedTuple):
    """
    Represents the result of a command execution.

    Attributes:
        command (str): The command that was executed.
        return_code (int): The return code of the command execution.
        stdout (str): The standard output of the command.
        stderr (str): The standard error of the command.
    """

    command: str
    return_code: int
    stdout: str
    stderr: str

    def json(self) -> str:
        return dumps(self)


def execute_command(cmd: str) -> str:
    """
    Executes a shell command and returns its result.

    Parameters:
        cmd (str): The shell command to be executed.

    Returns:
        str: A string representing JSON serialization of an object what will contain information about the command execution.
        Following will be the keys,
        "command" - The command that was executed.
        "return_code" - The return code of the command execution.
        "stdout" - The standard output of the command.
        "stderr" - The standard error of the command.
    """
    timeout = 10
    logger.debug(f"Timeout set to {timeout} seconds")
    logger.info(f"Executing command '{cmd}'")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return CmdResult(
            command=cmd,
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        ).json()
        logger.info(
            f"Command '{cmd}' successfully executed with return_code: {result.returncode}"
        )
    except subprocess.TimeoutExpired as e:
        logger.error(f"Command '{cmd}' timed out because: {e}")
        return CmdResult(
            command=cmd, return_code=1, stdout="", stderr="Command timed out\n"
        ).json()
    except subprocess.CalledProcessError as e:
        logger.error(f"Command '{cmd}' failed because: {e}")
        return CmdResult(
            command=cmd,
            return_code=e.returncode,
            stdout=e.stdout,
            stderr=e.stderr,
        ).json()
