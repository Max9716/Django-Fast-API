import asyncio
import os

SCRIPTS_DIR = "/var/www/html"
SYSTEM_PYTHON = "/usr/bin/python3"

async def run_script(script_name: str):
    script_path = os.path.join(SCRIPTS_DIR, f"{script_name}.py")

    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script '{script_name}' not found")

    process = await asyncio.create_subprocess_exec(
        SYSTEM_PYTHON,
        script_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    stdout = stdout.decode()
    stderr = stderr.decode()

    debug_info = {
        "stdout": stdout,
        "stderr": stderr,
        "returncode": process.returncode,
        "script_path": script_path
    }

    if process.returncode != 0:
        raise Exception(f"Script failed:\n{stderr}\nDebug info: {debug_info}")

    if not stdout:
        return f"Script ran, but no output.\nDebug info: {debug_info}"

    return stdout
