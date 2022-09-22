import sys
import types
from pathlib import Path


def import_parents(level):
    global __package__
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]

    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError:  # giá rimosso
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])


def print_import(string):
    print(string)
    for name, val in list(globals().items()):
        if isinstance(val, types.ModuleType):
            name = val.__name__
            print("Main -", name)


import_parents(1)

from .lib import project_lib

from .gui import main_application

if __name__ == "__main__":
    project_lib.default_project_settings_values()

    app = main_application.App()
    app.start()
