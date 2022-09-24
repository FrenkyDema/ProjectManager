# -*- coding: utf-8 -*-
__author__ = "Francesco"
__version__ = "0101 2022/03/19"

import tkinter
from genericpath import isdir
from tkinter import filedialog, messagebox

from PIL import Image
from PIL.ImageTk import PhotoImage
from customtkinter import *

from ..pages import new_project_enum
from ...lib import project_lib
from ...lib.project_lib import PROJECT_SETTINGS_FILE


def option_menu_callback(choice):
    project_lib.update_key_json(
        PROJECT_SETTINGS_FILE, "selected_language", choice)


def change_project_title(entry_text: StringVar):
    project_lib.update_key_json(
        PROJECT_SETTINGS_FILE, "project_name", entry_text.get())


def project_title_check(project_title):
    if project_title == "" or len(project_title) < 3:
        messagebox.showerror(
            "Invalid Input", "Inserire un titolo valido o\ncaratteri minimi 3")
        return True
    if any((c in "/\\:,.") for c in project_title):
        messagebox.showerror(
            "Invalid Input", "Inserire un titolo valido \ncaratteri /\\:,. non consentiti")
        return True
    return False


def project_directory_check():
    if not isdir(project_lib.get_key_value_json(PROJECT_SETTINGS_FILE, "path")):
        messagebox.showerror(
            "Error", "Selezionare un percorso valido")
        return True
    return False


class NewProjectPage(CTkFrame):
    def __init__(self, master, app):
        self.app = app
        super().__init__(master)

        # configure grid layout (3x7)
        for i in range(7):
            self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.title = CTkLabel(
            master=self,
            text="Nuovo progetto",
            text_font=("Roboto Medium", 20))  # font name and size in px
        self.title.grid(row=0, column=1, pady=20)

        self.recent_button = CTkButton(
            self,
            text="",
            width=50,
            height=50,
            corner_radius=10,
            image=PhotoImage(Image.open(project_lib.get_image_path("recent_icon.png")).resize((30, 30))),
            fg_color=("gray65", "gray25"),  # <- custom tuple-color
            command=lambda: self.app.chose_frame(new_project_enum.NewProjectPageEnum.RECENT))
        self.recent_button.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="en")

        self.entry_text = StringVar()
        self.project_name_entry = self.init_custom_entry()
        self.project_name_entry.grid(row=1, column=0, columnspan=3, padx=20, pady=15)
        self.add_entry_text_trace()

        self.directory_frame = CTkFrame(master=self)
        self.directory_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=15)

        self.directory_frame.columnconfigure(0, weight=1)
        self.directory_frame.columnconfigure(1, weight=1)
        self.directory_frame.columnconfigure(2, weight=1)

        self.root_display = CTkLabel(
            self.directory_frame,
            width=400,
            height=45)
        self.root_display.grid(row=0, column=0, columnspan=2, padx=10, sticky="e")

        self.chose_directory_button = CTkButton(
            self.directory_frame,
            height=45,
            width=45,
            image=PhotoImage(Image.open(project_lib.get_image_path("add-folder_ico.png")).resize((30, 30))),
            text="",
            fg_color=("gray65", "gray25"),  # <- custom tuple-color
            command=self.chose_directory)
        self.chose_directory_button.grid(row=0, column=2, sticky="w")

        self.description_button = CTkButton(
            self,
            text="Descrizione",
            compound="right",
            image=PhotoImage(Image.open(project_lib.get_image_path("description_icon.png")).resize((30, 30))),
            fg_color=("gray65", "gray25"),  # <- custom tuple-color
            command=lambda: self.app.chose_frame(new_project_enum.NewProjectPageEnum.DESCRIPTION))
        self.description_button.grid(row=3, column=1, padx=40, pady=15)

        supported_language = project_lib.get_key_value_json("config.json", "supported_languages").keys()
        self.language_option_menu_var = StringVar(value="Scegli linguaggio")
        self.language_combobox = CTkOptionMenu(
            master=self,
            values=list(supported_language),
            fg_color=("gray65", "gray25"),
            command=option_menu_callback,
            variable=self.language_option_menu_var
        )
        self.language_combobox.grid(row=4, column=1, padx=30, pady=15)

        self.auto_readme = False
        self.auto_readme_switch = CTkSwitch(
            master=self,
            text="Auto Readme",
            command=self.change_auto_readme
        )
        self.auto_readme_switch.grid(row=5, column=1, padx=40, pady=15)
        self.auto_readme_switch.configure(state=tkinter.DISABLED)

        self.submit_button = CTkButton(
            self,
            height=40,
            text="Crea Progetto",
            compound="right",
            image=PhotoImage(Image.open(project_lib.get_image_path("submit_icon.png")).resize((30, 30))),
            fg_color=("gray65", "gray25"),  # <- custom tuple-color
            command=self.submit_all)
        self.submit_button.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="se")

        self.set_default_values()

    def set_default_values(self):

        title: str = project_lib.get_key_value_json(PROJECT_SETTINGS_FILE, "project_name")
        if title != "":
            self.project_name_entry.insert(0, title)
        else:
            self.entry_text = StringVar()
            self.project_name_entry = self.init_custom_entry()
            self.project_name_entry.grid(row=1, column=0, columnspan=3, padx=20, pady=20)
            self.add_entry_text_trace()

        directory = project_lib.get_key_value_json(
            PROJECT_SETTINGS_FILE, "path")
        self.root_display.set_text(directory)

    def init_custom_entry(self):
        return CTkEntry(
            master=self,
            width=500,
            height=45,
            placeholder_text="Titolo progetto",
            textvariable=self.entry_text
        )

    def add_entry_text_trace(self):
        self.entry_text.trace("w", lambda name, index, mode, var=self.entry_text: change_project_title(var))

    def change_auto_readme(self):
        self.auto_readme = not self.auto_readme
        project_lib.update_key_json(
            PROJECT_SETTINGS_FILE, "auto_readme", self.auto_readme)

    def chose_directory(self):
        directory = filedialog.askdirectory()
        self.root_display.set_text(directory.replace("\\", "/"))
        project_lib.update_key_json(
            PROJECT_SETTINGS_FILE, "path", directory)

    def language_selected_check(self):
        if project_lib.get_key_value_json(PROJECT_SETTINGS_FILE, "selected_language") == "":
            messagebox.showerror(
                "Error", "Devi selezionare minimo 1 linguaggio")
            self.language_combobox.open_dropdown_menu()
            return True
        return False

    def submit_all(self):
        project_title = self.project_name_entry.get()
        if project_title_check(project_title) or self.language_selected_check() or project_directory_check():
            return
        project_lib.update_key_json(PROJECT_SETTINGS_FILE, "project_name", project_title)

        if project_lib.get_key_value_json(PROJECT_SETTINGS_FILE, "description") == "":
            empty_description = messagebox.askquestion(
                "Empty description",
                'La descrizione é vuota, vuoi aggiungerne una?',
                icon='warning'
            )
            if empty_description == "yes":
                self.app.change_page(new_project_enum.NewProjectPageEnum.DESCRIPTION)
                return

        exist, per_bin, per_doc = project_lib.make_project_dir()

        if not exist:
            try:
                project_lib.create_project_file(per_bin, per_doc)
            except Exception as e:
                messagebox.showerror("Error", f"Errore, riprova.\nError-code: '{e}'")
                return

        else:
            messagebox.showerror("Error", "Progetto giá esistente")
            return

        project_lib.default_project_settings_values()
        self.set_default_values()

        messagebox.showinfo("Confirm", "Progetto creato con successo")
