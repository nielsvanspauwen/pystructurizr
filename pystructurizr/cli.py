import aiofiles
import click
import httpx
import sys
import asyncio
import os
import shutil
from .cli_helper import generate_diagram_code, generate_diagram_code_in_child_process
from .cli_watcher import observe_modules



@click.command()
@click.option('--view', prompt='Your view file (e.g. example.componentview)',
              help='The view file to generate.')
def dump(view):
    initial_modules = set(sys.modules.keys())
    diagram_code = generate_diagram_code(view)
    current_modules = set(sys.modules.keys())
    # print("Imported modules:")
    # print(current_modules - initial_modules)
    click.echo(diagram_code)
    

@click.command()
@click.option('--view', prompt='Your view file (e.g. example.componentview)',
              help='The view file to develop.')
def dev(view):
    click.echo(f"Setting up live preview of view {view}...")
    # Prep the /tmp/pystructurizr folder
    tmp_folder = "/tmp/pystructurizr"
    os.makedirs(tmp_folder, exist_ok=True)
    current_script_path = os.path.abspath(__file__)
    index_html = os.path.join(os.path.dirname(current_script_path), 'index.html')
    print(index_html)
    shutil.copy(index_html, f"{tmp_folder}/index.html")

    async def async_behavior():
        print("Generating diagram...")
        diagram_code = generate_diagram_code_in_child_process(view)
        # print(diagram_code)
        url = f"https://kroki.io/structurizr/svg"

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=diagram_code)
        if resp.status_code != 200:
            print(resp)
            if resp.content:
                print(resp.content.decode())
            raise click.ClickException("Failed to create diagram")
        async with aiofiles.open(f"{tmp_folder}/diagram.svg", "w") as f:
            await f.write(resp.text)
            print(f"Updated SVG in {tmp_folder}")

    async def observe_loop():
        await async_behavior()
        await observe_modules(['example.users', 'example.chatsystem', 'example.containerview', 'example.workspace', 'example', 'pystructurizr.dsl'], async_behavior)

    asyncio.run(observe_loop())


@click.command()
@click.option('--view', prompt='Your view file (e.g. example.componentview)',
              help='The view file to generate and upload to S3.')
def build(view):
    click.echo(f"Generating view {view} and uploading to S3...")
    diagram_code = generate_diagram_code(view)
    
    async def async_behavior():
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=diagram_code)
        if resp.status_code != 200:
            print(resp)
            raise click.ClickException("Failed to create diagram")
        
        # TODO: take resp.text and upload it to an AVG file in an S3 bucket
        
    asyncio.run(async_behavior())


@click.group()
def cli():
    pass

cli.add_command(dump)
cli.add_command(dev)
cli.add_command(build)

if __name__ == '__main__':
    cli()
