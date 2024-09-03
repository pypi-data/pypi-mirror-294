import asyncio
import os
import shutil

COMMAND_TIMEOUT = 30
TIMEOUT_MESSAGE = f"Command timed out after {COMMAND_TIMEOUT} seconds"


async def execute_shell(code: str, working_directory: str) -> str:
    shell_path = (
        os.environ.get("SHELL")
        or shutil.which("bash")
        or shutil.which("sh")
        or "/bin/sh"
    )

    process = await asyncio.create_subprocess_exec(
        shell_path,
        "-l",
        "-c",
        code,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=working_directory,
    )

    exit_code = None
    stdout: list[str] = []
    stderr: list[str] = []
    assert process.stdout
    assert process.stderr
    stdout_capture_task = asyncio.create_task(capture(process.stdout, stdout))
    stderr_capture_task = asyncio.create_task(capture(process.stderr, stderr))

    async def capture_until_exit() -> int:
        await asyncio.wait({stdout_capture_task, stderr_capture_task})
        return await process.wait()

    try:
        exit_code = await asyncio.wait_for(capture_until_exit(), COMMAND_TIMEOUT)
    except (TimeoutError, asyncio.TimeoutError):  # noqa: UP041
        process.kill()

    output = []

    if stdout:
        output.append("STDOUT:\n\n" + "".join(stdout).strip() + "\n\n")

    if stderr:
        output.append("STDERR:\n\n" + "".join(stderr).strip() + "\n\n")

    if exit_code is None:
        output.append(f"EXIT CODE: {TIMEOUT_MESSAGE}")
    else:
        output.append(f"EXIT CODE: {exit_code}")

    return "".join(output)


async def capture(stream: asyncio.StreamReader, output: list[str]) -> None:
    while True:
        data = await stream.read(4096)

        if not data:
            break

        output.append(data.decode())
