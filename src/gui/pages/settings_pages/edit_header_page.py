# -*- coding: utf-8 -*-
__author__ = "Francesco"
__version__ = "0101 2022/03/16"

from customtkinter import *

from .edit_header_pages import header_editor
from ....gui import main_page_enum
from ....lib import project_lib

CONFIG_FILE = "config.json"


class EditHeadersPage(CTkFrame):
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

        self.title = CTkLabel(master=self,
                              text="Modifica intestazioni",
                              text_font=("Roboto Medium", 20))  # font name and size in px
        self.title.grid(row=0, column=1, pady=20)

        headers = project_lib.header_avable()

        self.open_editor_dix = {}
        buttons = []

        i = 0
        for header in headers:
            i += 1
            var = CTkButton(
                master=self,
                text=f"Modifica {header.split('.')[0]}",
                fg_color=("gray65", "gray25"),
                command=lambda bound_header=header: self.open_header_editor(bound_header))

            var.grid(row=i, column=1,
                     padx=20)
            self.open_editor_dix[header] = False
            buttons.append(var)

        back_button = CTkButton(
            master=self,
            text=f"Indietro",
            fg_color=("gray65", "gray25"),
            command=lambda: self.app.chose_frame(main_page_enum.MainPageEnum.SETTINGS))

        back_button.grid(row=7, column=0, columnspan=3,
                         padx=20, pady=20, sticky="es")

    def open_header_editor(self, header):
        self.app.change_right_frame(
            header_editor.HeaderEditor(self.app, self.app, header))
