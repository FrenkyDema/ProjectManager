from pathlib import Path
import sys
from customtkinter import *
from tkinter import StringVar, messagebox, scrolledtext

from enum import Enum

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


import_parents(2)

from .main_page_enum import MainPageEnum
from .pages.settings_page_enum import SettingsPageEnum

from .pages.main_page import MainPage
from .pages.settings_page import SettingsPage
from .pages.new_project_page import NewProjectPage

from .main_application import App

from .pages.settings_pages.edit_header_page import EditHeadersPage

from ..lib import project_lib


import types
for name, val in list(globals().items()):
    if isinstance(val, types.ModuleType):
        name = val.__name__
        if not name.startswith("customtkinter") and not name.startswith("tkinter"):
            print(val.__name__)