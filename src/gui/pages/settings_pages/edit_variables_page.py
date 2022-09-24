# -*- coding: utf-8 -*-
__author__ = "Francesco"
__version__ = "0101 2022/03/16"

from customtkinter import *

from ....gui import main_page_enum
from ....lib import project_lib
from ....lib.project_lib import PROJECT_SETTINGS_FILE

CONFIG_FILE = "config.json"


def change_variable(variable: str, entry_text: StringVar):
    project_lib.update_key_json(
        PROJECT_SETTINGS_FILE, variable, entry_text.get())


class EditVariablePage(CTkFrame):
    def __init__(self, master, app):
        self.app = app
        super().__init__(master)

        # configure grid layout (3x7)
        for i in range(5):
            self.rowconfigure(i, weight=1)
        self.rowconfigure(7, weight=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.title = CTkLabel(master=self,
                              text="Modifica variabili",
                              text_font=("Roboto Medium", 20))  # font name and size in px
        self.title.grid(row=0, column=2, pady=20)

        self.folder_prefix_label = CTkLabel(master=self,
                                            text="Prefisso cartella:",
                                            text_font=("Roboto Medium", 10))  # font name and size in px
        self.folder_prefix_label.grid(row=1, column=0, columnspan=1, padx=10, pady=20, sticky="e")

        self.entry_text = StringVar()
        self.folder_prefix_entry = self.init_custom_entry()
        self.folder_prefix_entry.grid(row=1, column=2, columnspan=3, padx=20, pady=20)
        self.add_entry_text_trace()

        back_button = CTkButton(
            master=self,
            text=f"Fatto",
            fg_color=("gray65", "gray25"),
            command=lambda: self.app.chose_frame(main_page_enum.MainPageEnum.SETTINGS))

        back_button.grid(row=7, column=1, columnspan=2,
                         padx=20, pady=20, sticky="s")

        self.set_default_values()

    def set_default_values(self):

        title: str = project_lib.get_key_value_json(PROJECT_SETTINGS_FILE, "folder_prefix")
        if title != "":
            self.folder_prefix_entry.insert(0, title)
        else:
            self.entry_text = StringVar()
            self.folder_prefix_entry = self.init_custom_entry()
            self.folder_prefix_entry.grid(row=1, column=2, columnspan=3, padx=20, pady=20)
            self.add_entry_text_trace()

    def init_custom_entry(self):
        return CTkEntry(
            master=self,
            width=500,
            height=45,
            placeholder_text="Prefisso cartella",
            textvariable=self.entry_text
        )

    def add_entry_text_trace(self):
        self.entry_text.trace("w", lambda name, index, mode, var=self.entry_text: change_variable("folder_prefix", var))
