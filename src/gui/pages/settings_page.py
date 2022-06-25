# -*- coding: utf-8 -*-
__autor__ = "Francesco"
__version__ = "0101 2022/03/16"
import tkinter
from customtkinter import *

from ..pages import settings_page_enum
from .settings_pages import edit_header_page


class SettingsPage(CTkFrame):
    def __init__(self, master, app):
        self.app = app
        super().__init__(master)

        # configure grid layout (3x7)
        for i in range(5):
            self.rowconfigure(i, weight=1)
        self.rowconfigure(5, weight=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.title = CTkLabel(master=self,
                              text="Impostazioni",
                              text_font=("Roboto Medium", 20))  # font name and size in px
        self.title.grid(row=0, column=1, pady=20)

        button_1 = CTkButton(
            master=self,
            text="Modifica intestazioni",
            fg_color=("gray65", "gray25"),
            command=lambda: self.change_page(settings_page_enum.SettingsPageEnum.EDIT_HEADER))
        button_1.grid(row=1, column=1,
                      padx=20, sticky="we")

        edit_variable_button = CTkButton(
            master=self,
            text="Modifica variabili",
            fg_color=("gray65", "gray25"),
            command=lambda: self.change_page(settings_page_enum.SettingsPageEnum.EDIT_VARIABLE))
        edit_variable_button.grid(row=2, column=1,
                                  padx=20, sticky="we")
        edit_variable_button.config(state=tkinter.DISABLED)

        edit_flag_button = CTkButton(
            master=self, text="Modifica flags",
            fg_color=("gray65", "gray25"),
            command=lambda: self.change_page(settings_page_enum.SettingsPageEnum.EDIT_FLAG))
        edit_flag_button.grid(row=3, column=1,
                              padx=20, sticky="we")
        edit_flag_button.config(state=tkinter.DISABLED)

    def change_page(self, page_type):
        match page_type:
            case settings_page_enum.SettingsPageEnum.EDIT_HEADER:
                self.app.change_right_frame(
                    edit_header_page.EditHeadersPage(self.app, self.app))

            case settings_page_enum.SettingsPageEnum.EDIT_VARIABLE:
                pass

            case settings_page_enum.SettingsPageEnum.EDIT_FLAG:
                pass

            case _:
                pass
