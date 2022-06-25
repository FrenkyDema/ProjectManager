# -*- coding: utf-8 -*-
__autor__ = "Francesco"
__version__ = "0101 2022/06/05"
import tkinter
from tkinter.tix import AUTO
from customtkinter import *
from tkinter import messagebox, scrolledtext

from .....lib import project_lib
from ... import settings_page_enum


CONFIG_FILE = "config.json"
PROJECT_SETTINGS_FILE = "project_settings.json"


class HeaderEditor(CTkFrame):
    def __init__(self, master, app, bound_header):
        self.app = app
        super().__init__(master)

        self.header = bound_header

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.title = CTkLabel(master=self,
                              text=f"Modifica {self.header}",
                              text_font=("Roboto Medium", 17))
        self.title.grid(row=0, column=0, pady=10)

        frame = CTkFrame(master=self,
                         corner_radius=10)
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")

        # configure grid layout (1x2)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=10)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=10)

        # ========= config frame left =========

        frame_left = CTkFrame(master=frame,
                              corner_radius=0)
        frame_left.grid(row=0, rowspan=2, column=0, sticky="nswe")

        frame_left.rowconfigure(0, weight=1)
        frame_left.rowconfigure(1, weight=5)

        frame_left.columnconfigure(0, weight=1)

        label_left = CTkLabel(frame_left,
                              text=f"Tags",
                              text_font=("Roboto Medium", 10))
        label_left.grid(row=0, column=0, sticky="we")

        tags_area = tkinter.Text(frame_left,
                                 width=AUTO,
                                 font=("Roboto Medium", 10))
        tkinter.Scrollbar(tags_area, orient="vertical")
        tags_area.insert(tkinter.INSERT, project_lib.get_tags(
            CONFIG_FILE).rstrip("\n"))
        tags_area.configure(state='disabled')

        tags_area.grid(row=1, column=0, pady=10,
                       padx=10, sticky="nsew")

        # ========= config frame right =========

        self.frame_right = CTkFrame(master=frame,
                                    corner_radius=10)
        self.frame_right.grid(row=0, column=1, padx=20,
                              pady=20, rowspan=2, sticky="nswe")

        # configure grid layout (3x2)
        self.frame_right.rowconfigure(0, weight=20)
        self.frame_right.rowconfigure(1, weight=1)
        self.frame_right.columnconfigure(0, weight=1)
        self.frame_right.columnconfigure(1, weight=1)
        self.frame_right.columnconfigure(2, weight=1)

        self.text_editor = scrolledtext.ScrolledText(self.frame_right,
                                                     font=("Roboto Medium", 10))
        self.text_editor.insert(
            tkinter.INSERT, project_lib.get_header_text(self.header).rstrip("\n"))

        self.text_editor.grid(column=0, row=0, columnspan=3, pady=10,
                              padx=10, sticky="nsew")

        # placing cursor in text area
        self.text_editor.focus()

        self.clear_button = CTkButton(master=self.frame_right,
                                      text="Cancella",
                                      fg_color=("gray65", "gray25"),
                                      command=self.clear_text)
        self.clear_button.grid(row=1, column=0, pady=10,
                               padx=10, sticky="w")

        self.cancel_button = CTkButton(master=self.frame_right,
                                       text="Annulla",
                                       fg_color=("gray65", "gray25"),
                                       command=lambda: self.back(False))
        self.cancel_button.grid(row=1, column=1, pady=10,
                                padx=10)

        self.submit_button = CTkButton(master=self.frame_right,
                                       text="Fatto",
                                       fg_color=("gray65", "gray25"),
                                       command=lambda: self.back(True))
        self.submit_button.grid(row=1, column=2, pady=10,
                                padx=10, sticky="e")

    def clear_text(self):
        self.text_editor.delete("1.0", "end")

    def back(self, saving):
        if(saving):
            text = self.text_editor.get("1.0", tkinter.END).rstrip("\n")
            project_lib.save_header(self.header, text)

        self.app.chose_frame(settings_page_enum.SettingsPageEnum.EDIT_HEADER)
