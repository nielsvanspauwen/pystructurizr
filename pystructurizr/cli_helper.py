import click
import importlib
import subprocess
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
