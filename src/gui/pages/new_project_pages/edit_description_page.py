# -*- coding: utf-8 -*-
__autor__ = "Francesco"
__version__ = "0101 2022/06/05"
import tkinter
from customtkinter import *
from tkinter import messagebox, scrolledtext


from ....lib import project_lib
from ... import main_page_enum


CONFIG_FILE = "config.json"
PROJECT_SETTINGS_FILE = "project_settings.json"

class EditDescriptionPage(CTkFrame):
    def __init__(self, master, app):
        self.app = app
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.title = CTkLabel(master=self,
                              text="Recenti",
                              text_font=("Roboto Medium", 20))  # font name and size in px
        self.title.grid(row=0, column=0, pady=10)


        frame = CTkFrame(master=self,
                            corner_radius=10)
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")

        # configure grid layout (3x7)
        for i in range(3):
            frame.columnconfigure(i, weight=1)
        frame.rowconfigure(0, weight=50)
        frame.rowconfigure(1, weight=1)

        # create label on CTkToplevel self.description_window

        self.text_area = scrolledtext.ScrolledText(frame, wrap=tkinter.WORD,
                                                font=("Roboto Medium", 10))
        self.text_area.insert(tkinter.INSERT,
                            project_lib.get_key_value_JSON(PROJECT_SETTINGS_FILE, "descrizione").rstrip("\n"))

        self.text_area.grid(column=0, row=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        # placing cursor in text area
        self.text_area.focus()

        self.clear_button = CTkButton(master=frame,
                                    text="Cancella",
                                    fg_color=("gray75", "gray30"),
                                    command=self.clear_text)
        self.clear_button.grid(row=1, column=0, pady=5, padx=5, sticky="sw")

        self.submit_button = CTkButton(master=frame,
                                    text="Fatto",
                                    fg_color=("gray75", "gray30"),
                                    command=self.back)
        self.submit_button.grid(row=1, column=2, pady=5, padx=5, sticky="se")

    def clear_text(self):
        self.text_area.delete("1.0", "end")

    def back(self):
        description = self.text_area.get("1.0", tkinter.END).rstrip("\n")

        project_lib.update_key_JSON(
            PROJECT_SETTINGS_FILE, "descrizione", description)

        self.app.chose_frame(main_page_enum.MainPageEnum.NEW_PROJECT)