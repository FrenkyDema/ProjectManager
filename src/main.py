import os
import sys
import types
from pathlib import Path


path, tail = os.path.split(__file__)
os.chdir(path)


def import_parents(level):
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]

    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError:
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])


def print_import(string):
    print(string)
    for name, val in list(globals().items()):
        if isinstance(val, types.ModuleType):
            name = val.__name__
            print("Main -", name)


import_parents(1)

from src.gui import main_application
from src.lib import project_lib

if __name__ == "__main__":
    from genericpath import isdir

    if not isdir(project_lib.resource_path("")):
        print("not exist")
        project_lib.create_app_files()

    project_lib.default_project_settings_values()

    app = main_application.App()
    app.start()
