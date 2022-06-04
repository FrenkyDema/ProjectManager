from pathlib import Path
import sys, types


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

def print_import(str):
    print(str)
    for name, val in list(globals().items()):
        if isinstance(val, types.ModuleType):
            name = val.__name__
            print("Main -", val.__name__)

import_parents(1)


from .lib import project_lib

from .gui.pages import main_page
from .gui.pages import new_project_page
from .gui.pages import settings_page
from .gui.pages import settings_page_enum
from .gui.pages.settings_pages import edit_header_page

from .gui import main_application
from .gui import main_page_enum



if __name__ == "__main__":

    project_lib.default_project_settings_values()

    app = main_application.App()    
    app.start()