import base64
import logging
import subprocess
from typing import Callable, Optional


class ProcessError(Exception):
    """An error that occurred while running a process."""

    def __init__(self, result: Optional["ProcessResult"], message: str | None = None):
        super().__init__(message)
        self.result = result


class ProcessResult(subprocess.CompletedProcess[str]):
    """The result of a process execution."""
    
    def __init__(self, stdout: str = "", stderr: str = "", returncode: int = 0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

    @property
    def failed(self) -> bool:
        return self.returncode != 0

    @staticmethod
    def from_subprocess_result(
        data: subprocess.CompletedProcess[str]
    ) -> "ProcessResult":
        return ProcessResult(
            stdout=data.stdout or "",
            stderr=data.stderr or "",
            returncode=data.returncode,
        )


def _escape_command(command: str) -> str:
    return command.replace("\\", r"\\\\").replace("$", "\\$")


def _get_docker_pid(host: str) -> str:
    """Gets the container id from the container name or id."""
    
    docker_pid = run(f"docker ps -f name={host} -qa").stdout.strip()
    if not docker_pid:
        docker_pid = run(f"docker ps -f id={host} -qa").stdout.strip()
    if not docker_pid:
        logging.info(f"Preparing container {host}...")
        docker_pid = run(f"docker run --detach {host} sleep infinity").stdout.strip()
    return docker_pid


def prepare_host(host: str | None) -> str | None:
    """Prepares a host for running commands."""

    if host and host.startswith("docker://"):
        host = host[9:]
        docker_pid = _get_docker_pid(host)
        if not docker_pid:
            raise ValueError(f"Could not find container with name or id {host}")
        return f"docker://{docker_pid}"
    return host


def cleanup_host(host: str | None) -> None:
    """Stops and removes a container if it was started by the process module."""

    if not host:
        return

    if host.startswith("docker://"):
        host = host[9:]
        logging.info(f"Stopping and removing container {host}...")

        try:
            run(f"docker stop {host}")
        except Exception:
            pass
        try:
            run(f"docker rm {host}")
        except Exception:
            pass


def capture_subprocess_output(
    command: str,
    stdout_handler: Callable[[str], None] | None = None,
) -> subprocess.CompletedProcess[str]:
    # Got the poll() trick from https://gist.github.com/tonykwok/e341a1413520bbb7cdba216ea7255828
    # Thanks @tonykwok!

    # shell = True is required for passing a string command instead of a list
    # bufsize = 1 means output is line buffered
    # universal_newlines = True is required for line buffering
    process = subprocess.Popen(
        command,
        shell=True,
        bufsize=1,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        text=True,
    )

    assert process.stdout is not None
    assert process.stderr is not None

    stdout: str = ""
    stderr: str = ""

    while process.poll() is None:
        line = process.stdout.readline()
        stdout += line
        if stdout_handler:
            stdout_handler(line)

    return_code = process.wait()
    stdout = stdout.strip()
    stderr = process.stderr.read()

    return subprocess.CompletedProcess(command, return_code, stdout, stderr)


def run(
    command: str,
    host: str | None = None,
    stdout_handler: Callable[[str], None] | None = None,
    stderr_handler: Callable[[str], None] | None = None,
) -> ProcessResult:
    """Runs a command on a host and returns the result.

    - `host` can be `None` (or empty) for the local host, `ssh://[user@]<host>` for an SSH host
    or `docker://<container>` for a running Docker container.
    - `stdout_handler` and `stderr_handler` are optional functions that are called
    with the output of the command as it is produced.
    
    Returns a `ProcessResult` object with the output of the command.
    """

    command = _escape_command(command)

    if host and host.startswith("ssh://"):
        ssh_host = host[6:]
        command = f"ssh {ssh_host} -- '{command}'"
    elif host and host.startswith("docker://"):
        docker_pid = host[9:]
        command = f"docker exec -i {docker_pid} sh -c '{command}'"

    result = capture_subprocess_output(command, stdout_handler)

    if result.stderr and stderr_handler:
        stderr_handler(result.stderr)

    return ProcessResult.from_subprocess_result(result)


def read_file(host: str | None, file_path: str) -> bytes:
    """Reads a file from a host and returns its content as bytes."""

    b64 = run(f"cat {file_path} | base64", host).stdout.strip()
    return base64.b64decode(b64)


def write_file(host: str, file_path: str, content: bytes) -> ProcessResult:
    """Writes content to a file on a host."""

    b64 = base64.b64encode(content).decode()
    return run(f"echo {b64} | base64 -di - > {file_path}", host)
