import subprocess
import sys
import threading
from typing import Dict, Optional


def run_command(command: str, env: Optional[Dict[str, str]] = None) -> None:
    """
    Executes the given command in a subprocess and prints its stdout and stderr in real-time.

    Args:
    - command (str): The command to be executed.
    - env (Optional[Dict[str, str]]): A dictionary of environment variables to use for the subprocess.

    Raises:
    - subprocess.CalledProcessError: If the subprocess returns a non-zero exit code.
    """

    def reader_thread(pipe, callback):
        for line in iter(pipe.readline, ""):
            callback(line)
        pipe.close()

    # Function to print stdout
    def print_stdout(line: str) -> None:
        print(line, end="")

    # Function to print stderr
    def print_stderr(line: str) -> None:
        print(line, end="", file=sys.stderr)

    # Start the subprocess
    process = subprocess.Popen(
        command,
        shell=True,
        executable="/bin/bash",
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Start threads to read and display stdout and stderr in real-time
    t1 = threading.Thread(target=reader_thread, args=(process.stdout, print_stdout))
    t2 = threading.Thread(target=reader_thread, args=(process.stderr, print_stderr))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    # Wait for the process to complete and get the return code
    return_code = process.wait()

    # Check the return code
    if return_code:
        raise subprocess.CalledProcessError(return_code, command)
