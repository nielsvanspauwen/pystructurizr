import importlib
import json
import sys

import click

from pystructurizr.dsl import Dumper


@click.command()
@click.option('--view', prompt='Your view file (e.g. example.componentview)',
              help='The view file to generate.')
@click.option(
    "--directives", help="Flag to add extra directives (i.e. !docs) or omit",
    is_flag=True, default=False)
def dump(view: str, directives: bool):
    try:
        initial_modules = set(sys.modules.keys())
        module = importlib.import_module(view)
        imported_modules = set(sys.modules.keys()) - initial_modules
        dumper = Dumper(with_directives=directives)
        code = module.workspace.dump(dumper=dumper)
        print(json.dumps({
            "code": code,
            "imported_modules": list(imported_modules)
        }))
    except ModuleNotFoundError:
        # pylint: disable=raise-missing-from
        raise click.BadParameter("Invalid view name. Make sure you don't include the .py file extension.")
    except AttributeError:
        # pylint: disable=raise-missing-from
        raise click.BadParameter("Non-compliant view file: make sure it exports the PyStructurizr workspace.")


@click.group()
def cli():
    pass


cli.add_command(dump)

if __name__ == '__main__':
    cli()
