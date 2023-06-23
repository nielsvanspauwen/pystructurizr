import importlib
import json
import sys

import click


@click.command()
@click.option('--view', prompt='Your view file (e.g. example.componentview)',
              help='The view file to generate.')
def dump(view: str):
    try:
        initial_modules = set(sys.modules.keys())
        module = importlib.import_module(view)
        imported_modules = set(sys.modules.keys()) - initial_modules
        code = module.workspace.dump()
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
