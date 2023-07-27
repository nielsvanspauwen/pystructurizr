# PyStructurizr
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
[![PyPI version](https://badge.fury.io/py/pystructurizr.svg)](https://badge.fury.io/py/pystructurizr)
[![Pylint](https://github.com/nielsvanspauwen/pystructurizr/actions/workflows/pylint.yml/badge.svg?branch=master)](https://github.com/nielsvanspauwen/pystructurizr/actions/workflows/pylint.yml)

PyStructurizr provides a Python DSL inspired by [Structurizr](https://structurizr.com/), and is intended for generating C4 diagrams.

## Overview
[Structurizr](https://structurizr.com/) builds upon "diagrams as code", allowing you to create multiple software architecture diagrams from a single model. A popular way of creating Structurizr workspaces is the Structurizr DSL.

However, Structurizr DSL has some downsides:

1. It's a custom language, with its own syntax rules and limitations
2. It has rather primitive support for splitting your diagram code over multiple files, with only `#include`-like support rather than proper imports. That makes it really hard to maintain C4 models with a team.

PyStructurizr solves that. It implements the same concepts as Structurizr DSL, but now in plain Python. That means you can use the full power and flexibility of Python to define your diagrams!

### Example
Consider the following example (as shown on Structurizr's homepage), in Structurizr DSL:
```
workspace {
    model {
        user = person "User"
        softwareSystem = softwareSystem "Software System" {
            webapp = container "Web Application" {
                user -> this "Uses"
            }
            container "Database" {
                webapp -> this "Reads from and writes to"
            }
        }
    }
    views {
        container softwareSystem {
            include *
            autolayout lr
        }
    }
}
```

In PyStructurizr, this becomes:
```python
from pystructurizr.dsl import Workspace

# Create the model(s)
with Workspace() as workspace:
    with workspace.Model(name="model") as model:
        user = model.Person("User")
        with model.SoftwareSystem("Software System") as software_system:
            webapp = software_system.Container("Web Application")
            db = software_system.Container("Database")

    # Define the relationships
    user.uses(webapp, "Uses")
    webapp.uses(db, "Reads from and writes to")

# Create a view onto the model
workspace.ContainerView(
    software_system, 
    "My Container View",
    "The container view of our simply software system."
)
```

For such a simple example, the benefits are not super obvious, but look at the example in this repo for something more realistic.

### CLI
PyStructurizr comes with a DSL that allows to convert your Python code to Structurizr DSL, or to immediately generate SVG versions of the diagrams. You can even upload directly to your favorite cloud storage provider: this is ideal if you want to include diagrams on blogs, wiki's, etc.

Finally, there's a development mode so you can get live preview of the diagram you're working on in your webbrowser.

## Installation

```pip install pystructurizr```

## Usage

### Convert to Structurizr DSL
```pystructurizr dump --view <path_to_view_file>```

### Live preview 
```pystructurizr dev --view <path_to_view_file>```

### Convert to SVG and upload to cloud storage
```pystructurizr build --view <path_to_view_file> --gcs-credentials <path_to_credentials_json_file> --bucket-name <string> --object-name <string>```

Note that this command uses kroki.io under the hood to generate your SVG file. The benefit is that you don't need to install any tools that understand Structurizr DSL on your machine. The downside is that your diagram code is sent to an online service.

## License

MIT License

## Acknowledgements

- [Structurizr](https://structurizr.com/) 
- [Kroki](https://kroki.io/)
