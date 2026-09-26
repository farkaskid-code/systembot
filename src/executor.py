import logging
import subprocess
from typing import NamedTuple

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CmdResult(NamedTuple):
    command: str
    return_code: int
    stdout: str
    stderr: str


def execute_commands(config: dict, valid_commands: list[str]) -> list[CmdResult]:
    timeout = 10
    if "timeout" in config:
        timeout = config.get("timeout")
    else:
        logger.debug(f"timeout not configured, defaulting to {timeout}")

    command_outputs = []
    for cmd in valid_commands:
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
            command_outputs.append(
                CmdResult(
                    command=cmd,
                    return_code=result.returncode,
                    stdout=result.stdout,
                    stderr=result.stderr,
                )
            )
            logger.info(
                f"Command '{cmd}' successfully executed with return_code: {result.returncode}"
            )
        except subprocess.TimeoutExpired as e:
            logger.error(f"Command '{cmd}' timed out because: {e}")
            command_outputs.append(
                CmdResult(
                    command=cmd, return_code=1, stdout="", stderr="Command timed out\n"
                )
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Command '{cmd}' failed because: {e}")
            command_outputs.append(
                CmdResult(
                    command=cmd,
                    return_code=e.returncode,
                    stdout=e.stdout,
                    stderr=e.stderr,
                )
            )

    return command_outputs
