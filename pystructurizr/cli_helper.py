from typing import List, Dict, Tuple
import json
import os
import subprocess
import sys

import aiofiles
import click
import httpx

import google.auth.transport.requests
import google.auth

from .config import URL


def _get_token():
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    request = google.auth.transport.requests.Request()
    creds, _ = google.auth.default(scopes=scopes)
    creds.refresh(request)
    return creds.id_token


def generate_diagram_code_in_child_process(view: str) -> Tuple[Dict, List[str]]:
    def run_child_process():
        # Run a separate Python script as a child process
        output = subprocess.check_output(
            [sys.executable, "-m", "pystructurizr.generator", "dump", "--view", view])
        return output.decode().strip()

    # Run the child process and capture its output
    child_output = run_child_process()
    result = json.loads(child_output)
    return result['code'], result['imported_modules']


async def generate_svg(diagram_code: Dict, tmp_folder: str) -> str:

    async with httpx.AsyncClient() as client:
        if "run.app" in URL:
            # Use Google Cloud Run's authentication mechanism
            headers = {"Authorization": f"Bearer {_get_token()}"}
        else:
            headers = {}
        resp = await client.post(URL, data=diagram_code, headers=headers)

    if resp.status_code != 200:
        print(resp)
        if resp.content:
            print(resp.content.decode())
        raise click.ClickException("Failed to create diagram")

    svg_file_path = f"{tmp_folder}/diagram.svg"
    async with aiofiles.open(svg_file_path, "w") as svg_file:
        await svg_file.write(resp.text)

    return svg_file_path


def ensure_tmp_folder_exists() -> str:
    tmp_folder = "/tmp/pystructurizr"
    os.makedirs(tmp_folder, exist_ok=True)
    return tmp_folder
