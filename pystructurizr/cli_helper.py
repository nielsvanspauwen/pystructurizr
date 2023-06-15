import click
import importlib
import subprocess
import sys
import aiofiles
import click
import httpx
import sys
import os


# This is useally run within the same process as cli.py
# But for the 'dev' command, we run it as a separate process, so it can be run
# repeatedly within the same dev session whenever the view changes.
def generate_diagram_code(view):
    try:
        module = importlib.import_module(view)
        code = module.workspace.dump()
        return code
    except ModuleNotFoundError:
        raise click.BadParameter("Invalid view name. Make sure you don't include the .py file extension.")
    except AttributeError:
        raise click.BadParameter("Non-compliant view file: make sure it exports the PyStructurizr workspace.")

def generate_diagram_code_in_child_process(view):
    def run_child_process():
        # Run a separate Python script as a child process
        output = subprocess.check_output([sys.executable, "-m", "pystructurizr.cli", "dump", "--view", view])
        return output.decode().strip()

    # Run the child process and capture its output
    child_output = run_child_process()
    return child_output


async def generate_svg(diagram_code, tmp_folder):
    url = f"https://kroki.io/structurizr/svg"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data=diagram_code)

    if resp.status_code != 200:
        print(resp)
        if resp.content:
            print(resp.content.decode())
        raise click.ClickException("Failed to create diagram")
    
    svg_file_path = f"{tmp_folder}/diagram.svg"
    async with aiofiles.open(svg_file_path, "w") as f:
        await f.write(resp.text)

    return svg_file_path


def ensure_tmp_folder_exists():
    tmp_folder = "/tmp/pystructurizr"
    os.makedirs(tmp_folder, exist_ok=True)
    return tmp_folder
