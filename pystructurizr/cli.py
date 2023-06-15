import click
import asyncio
import os
import shutil
import subprocess
from .cli_helper import generate_diagram_code, generate_diagram_code_in_child_process, generate_svg, ensure_tmp_folder_exists
from .cli_watcher import observe_modules
from .cloudstorage import create_cloud_storage, CloudStorage



@click.command()
@click.option('--view', prompt='Your view file (e.g. example.componentview)',
              help='The view file to generate.')
def dump(view):
    diagram_code = generate_diagram_code(view)
    click.echo(diagram_code)



@click.command()
@click.option('--view', prompt='Your view file (e.g. example.componentview)',
              help='The view file to develop.')
def dev(view):
    click.echo(f"Setting up live preview of view {view}...")
    # Prep the /tmp/pystructurizr folder
    tmp_folder = ensure_tmp_folder_exists()
    current_script_path = os.path.abspath(__file__)
    index_html = os.path.join(os.path.dirname(current_script_path), 'index.html')
    shutil.copy(index_html, f"{tmp_folder}/index.html")

    async def async_behavior():
        print("Generating diagram...")
        diagram_code = generate_diagram_code_in_child_process(view)
        await generate_svg(diagram_code, tmp_folder)

    async def observe_loop():
        await async_behavior()
        click.echo("Launching webserver...")
        subprocess.Popen(f"httpwatcher --root {tmp_folder} --watch {tmp_folder}", shell=True)
        await observe_modules(['example.users', 'example.chatsystem', 'example.containerview', 'example.workspace', 'example', 'pystructurizr.dsl'], async_behavior)

    asyncio.run(observe_loop())



@click.command()
@click.option('--view', prompt='Your view file (e.g. example.componentview)',
              help='The view file to generate and upload to cloud storage.')
@click.option('--gcs-credentials', prompt='Path to json file containing Google Cloud Storage credentials', type=click.Path(exists=True),
              help='Path to the credentials.json file for Google Cloud Storage.')
@click.option('--bucket-name', prompt='Name of the bucket on Google Cloud Storage',
              help='The name of the bucket to use on Google Cloud Storage.')
@click.option('--object-name', prompt='Name of the object on Google Cloud Storage',
              help='The name of the object to use on Google Cloud Storage.')
def build(view, gcs_credentials, bucket_name, object_name):
    async def async_behavior():
        # Generate diagram
        diagram_code = generate_diagram_code(view)
        tmp_folder = ensure_tmp_folder_exists()

        # Generate SVG
        svg_file_path = await generate_svg(diagram_code, tmp_folder)

        # Upload it to the requested cloud storage provider
        cloud_storage = create_cloud_storage(CloudStorage.Provider.GCS, gcs_credentials)
        svg_file_url = cloud_storage.upload_file(svg_file_path, bucket_name, object_name)
        print(svg_file_url)
    
    asyncio.run(async_behavior())



@click.group()
def cli():
    pass

cli.add_command(dump)
cli.add_command(dev)
cli.add_command(build)

if __name__ == '__main__':
    cli()
