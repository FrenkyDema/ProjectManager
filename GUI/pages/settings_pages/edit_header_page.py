# -*- coding: utf-8 -*-
__autor__ = "Francesco"
__version__ = "0101 2022/03/16"

from pathlib import Path
from tkinter import messagebox, scrolledtext

from customtkinter import *

CONFIG_FILE = "config.json"


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


import_parents(4)
from ....bin import project_lib
from ...main_application import App
from ...main_page_enum import MainPageEnum


class EditHeadersPage(CTkFrame):
    def __init__(self, master, app: App):
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
                fg_color=("gray75", "gray30"),
                command=lambda bound_header=header: open_header_editor(bound_header))

            var.grid(row=i, column=1,
                     padx=20)
            self.open_editor_dix[header] = False
            buttons.append(var)

        back_button = CTkButton(
            master=self,
            text=f"Indietro",
            fg_color=("gray75", "gray30"),
            command=lambda: self.app.chose_frame(MainPageEnum.SETTINGS))

        back_button.grid(row=7, column=0, columnspan=3,
                         padx=20, pady=20, sticky="es")

        def open_header_editor(header):

            def clear_text():
                text_editor.delete("1.0", "end")

            def save_request(window):
                on_closing(window, messagebox.askyesno("Save", "Salvare modifiche?"))

            def on_closing(window, saving):
                if saving:
                    text = text_editor.get("1.0", tkinter.END).rstrip("\n")
                    project_lib.save_header(header, text)

                self.open_editor_dix[header] = False
                window.destroy()

            if not self.open_editor_dix[header]:
                self.open_editor_dix[header] = True
                window = CTkToplevel(self)
                window.geometry("900x530")

                window.protocol("WM_DELETE_WINDOW", lambda: save_request(window))

                # configure grid layout (1x2)
                window.columnconfigure(0, weight=1)
                window.columnconfigure(1, weight=10)
                window.rowconfigure(0, weight=1)
                window.rowconfigure(1, weight=10)

                # ========= config frame left =========

                label_left = CTkLabel(
                    window, text=f"Tags", text_font=("Roboto Medium", 10))
                label_left.grid(row=0, column=0, pady=10, sticky="we")

                frame_left = CTkFrame(master=window,
                                      corner_radius=0)
                frame_left.grid(row=1, rowspan=2, column=0, sticky="nswe")

                frame_left.rowconfigure(0, weight=1)
                frame_left.columnconfigure(0, weight=1)

                tags_area = tkinter.Text(frame_left,
                                         width=20,
                                         font=("Roboto Medium", 10))
                tkinter.Scrollbar(tags_area, orient="vertical")
                tags_area.insert(tkinter.INSERT, project_lib.get_tags(
                    CONFIG_FILE).rstrip("\n"))
                tags_area.configure(state='disabled')

                tags_area.grid(column=0, row=0, pady=10,
                               padx=10, sticky="nsew")

                # ========= config frame right =========

                label_right = CTkLabel(
                    window, text=f"Modifica {header}", text_font=("Roboto Medium", 17))
                label_right.grid(row=0, column=1, pady=10)

                frame_right = CTkFrame(master=window,
                                       corner_radius=10)
                frame_right.grid(row=1, column=1, padx=20,
                                 pady=20, sticky="nswe")

                # configure grid layout (3x2)
                frame_right.rowconfigure(1, weight=10)
                frame_right.columnconfigure(0, weight=1)
                frame_right.columnconfigure(1, weight=1)
                frame_right.columnconfigure(2, weight=1)

                text_editor = scrolledtext.ScrolledText(frame_right, wrap=tkinter.WORD,
                                                        font=("Roboto Medium", 10))
                text_editor.insert(
                    tkinter.INSERT, project_lib.get_header_text(header).rstrip("\n"))

                text_editor.grid(column=0, row=0, columnspan=3, pady=10,
                                 padx=10, sticky="nsew")

                # placing cursor in text area
                text_editor.focus()

                submit_button = CTkButton(master=frame_right,
                                          text="Fatto",
                                          fg_color=("gray75", "gray30"),
                                          command=lambda: on_closing(window, True))
                submit_button.grid(row=1, column=2, pady=10,
                                   padx=10, sticky="se")

                cancel_button = CTkButton(master=frame_right,
                                          text="Annulla",
                                          fg_color=("gray75", "gray30"),
                                          command=lambda: on_closing(window, False))
                cancel_button.grid(row=1, column=1, pady=10,
                                   padx=10, sticky="s")

                clear_button = CTkButton(master=frame_right,
                                         text="Cancella",
                                         fg_color=("gray75", "gray30"),
                                         command=clear_text)
                clear_button.grid(row=1, column=0, pady=10,
                                  padx=10, sticky="sw")
