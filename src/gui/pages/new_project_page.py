# -*- coding: utf-8 -*-
__autor__ = "Francesco"
__version__ = "0101 2022/03/19"
import tkinter
from customtkinter import *
from tkinter import StringVar, filedialog, messagebox, scrolledtext
from PIL import Image
from PIL.ImageTk import PhotoImage

from genericpath import isdir

from ...lib import project_lib
from ...gui import main_application
from ..pages import new_project_enum
from .new_project_pages import recent_project_page
from .new_project_pages import edit_description_page


PROJECT_SETTINGS_FILE = "project_settings.json"


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

        self.title = CTkLabel(master=self,
                              text="Nuovo progetto",
                              text_font=("Roboto Medium", 20))  # font name and size in px
        self.title.grid(row=0, column=1, pady=20)

        self.recent_button = CTkButton(
            self,
            text="",
            width=50,
            height=50,
            corner_radius=10,
            image=PhotoImage(Image.open(project_lib.get_image_path(
                "recent_icon.png")).resize((30, 30))),
            fg_color=("gray65", "gray25"),  # <- custom tuple-color
            command=lambda: self.change_page(new_project_enum.NewProjectPageEnum.RECENT))
        self.recent_button.grid(
            row=0, column=0, columnspan=3, padx=10, pady=10, sticky="en")

        self.entry_text = StringVar()
        self.project_name_entry = self.init_CTkEntry()
        self.project_name_entry.grid(
            row=1, column=0, columnspan=3, padx=20, pady=15)
        self.add_entry_text_trace()

        self.directory_frame = CTkFrame(master=self)
        self.directory_frame.grid(
            row=2, column=0, columnspan=3, pady=10, padx=15)

        self.directory_frame.columnconfigure(0, weight=1)
        self.directory_frame.columnconfigure(1, weight=1)
        self.directory_frame.columnconfigure(2, weight=1)

        self.root_display = CTkLabel(self.directory_frame,
                                     width=400,
                                     height=45)
        self.root_display.grid(
            row=0, column=0, columnspan=2, padx=10, sticky="e")

        self.chose_directory_button = CTkButton(
            self.directory_frame,
            height=45,
            width=45,
            image=PhotoImage(Image.open(project_lib.get_image_path(
                "add-folder_ico.png")).resize((30, 30))),
            text="",
            fg_color=("gray65", "gray25"),  # <- custom tuple-color
            command=self.chose_directory)
        self.chose_directory_button.grid(row=0, column=2, sticky="w")

        self.description_button = CTkButton(
            self,
            text="Descrizione",
            compound="right",
            image=PhotoImage(Image.open(project_lib.get_image_path(
                "description_icon.png")).resize((30, 30))),
            fg_color=("gray65", "gray25"),  # <- custom tuple-color
            command=lambda: self.change_page(new_project_enum.NewProjectPageEnum.DESCRIPRION))
        self.description_button.grid(row=3, column=1, padx=40, pady=15)

        supported_lenguage = project_lib.get_key_value_JSON(
            "config.json", "supported_leguages").keys()
        self.lenguage_optionmenu_var = StringVar(
            value="Scegli linguaggio")  # set initial value
        self.lenguage_combobox = CTkOptionMenu(
            master=self,
            values=list(supported_lenguage),
            fg_color=("gray65", "gray25"),
            command=self.optionmenu_callback,
            variable=self.lenguage_optionmenu_var)
        self.lenguage_combobox.grid(row=4, column=1, padx=30, pady=15)

        self.auto_readme = False
        self.auto_readme_switch = CTkSwitch(master=self,
                                            text="Auto Readme",
                                            command=self.change_auto_readme)
        self.auto_readme_switch.grid(row=5, column=1, padx=40, pady=15)
        self.auto_readme_switch.config(state=tkinter.DISABLED)

        self.lenguage_button = CTkButton(
            self,
            height=40,
            text="Crea Progetto",
            compound="right",
            image=PhotoImage(Image.open(project_lib.get_image_path(
                "submit_icon.png")).resize((30, 30))),
            fg_color=("gray65", "gray25"),  # <- custom tuple-color
            command=self.submit_all)
        self.lenguage_button.grid(
            row=6, column=0, columnspan=3, padx=10, pady=10, sticky="se")

        self.set_default_values()

    def optionmenu_callback(self, choice):

        project_lib.update_key_JSON(
            PROJECT_SETTINGS_FILE, "linguaggio_selezionato", choice)

    def set_default_values(self):

        title: str = project_lib.get_key_value_JSON(
            PROJECT_SETTINGS_FILE, "nome_progetto")
        if title != "":
            self.project_name_entry.insert(0, title)
        else:
            self.entry_text = StringVar()
            self.project_name_entry = self.init_CTkEntry()
            self.project_name_entry.grid(
                row=1, column=0, columnspan=3, padx=20, pady=20)
            self.add_entry_text_trace()

        directory = project_lib.get_key_value_JSON(
            PROJECT_SETTINGS_FILE, "percorso")
        self.root_display.set_text(directory)

    def init_CTkEntry(self):
        return CTkEntry(master=self,
                        width=500,
                        height=45,
                        placeholder_text="Titolo progetto",
                        textvariable=self.entry_text)

    def add_entry_text_trace(self):
        self.entry_text.trace("w", lambda name, index, mode,
                              var=self.entry_text: self.change_projec_title(var))

    def change_auto_readme(self):
        self.auto_readme = not self.auto_readme
        project_lib.update_key_JSON(
            PROJECT_SETTINGS_FILE, "auto_readme", self.auto_readme)

    def change_projec_title(self, entry_text: StringVar):
        project_lib.update_key_JSON(
            PROJECT_SETTINGS_FILE, "nome_progetto", entry_text.get())

    def chose_directory(self):
        directory = filedialog.askdirectory()
        self.root_display.set_text(directory.replace("\\", "/"))
        project_lib.update_key_JSON(
            PROJECT_SETTINGS_FILE, "percorso", directory)

    def change_page(self, page_type):
        match page_type:
            case new_project_enum.NewProjectPageEnum.DESCRIPRION:
                self.app.change_right_frame(
                    edit_description_page.EditDescriptionPage(self.app, self.app))

            case new_project_enum.NewProjectPageEnum.RECENT:
                self.app.change_right_frame(
                    recent_project_page.RecentProjectPage(self.app, self.app))

            case _:
                pass

    def project_title_check(self, project_title):
        if (project_title == "" or len(project_title) < 3):
            messagebox.showerror(
                "Invalid Input", "Inserire un titolo valido o\ncaratteri minimi 3")
            return True
        if any((c in "/\\:,.") for c in project_title):
            messagebox.showerror(
                "Invalid Input", "Inserire un titolo valido \ncaratteri /\\:,. non consentiti")
            return True
        return False

    def lenguage_selected_check(self):
        if project_lib.get_key_value_JSON(PROJECT_SETTINGS_FILE, "linguaggio_selezionato") == "":
            messagebox.showerror(
                "Error", "Devi selezionare minimo 1 linguaggio")
            self.lenguage_combobox.open_dropdown_menu()
            return True
        return False

    def project_directory_check(self):
        if not isdir(project_lib.get_key_value_JSON(PROJECT_SETTINGS_FILE, "percorso")):
            messagebox.showerror(
                "Error", "Selezionare un percorso valido")
            return True
        return False

    def submit_all(self):

        project_title = self.project_name_entry.get()
        if self.project_title_check(project_title) or \
                self.lenguage_selected_check() or \
                self.project_directory_check():
            return
        project_lib.update_key_JSON(
            PROJECT_SETTINGS_FILE, "nome_progetto", project_title)

        if project_lib.get_key_value_JSON(PROJECT_SETTINGS_FILE, "descrizione") == "":
            empty_description = messagebox.askquestion("Empty description",
                                                       'La descrizione é vuota, vuoi aggiungerne una?', icon='warning')
            if empty_description == "yes":
                self.change_page(new_project_enum.NewProjectPageEnum.DESCRIPRION)
                return

        exist, perBin, perDoc = project_lib.make_project_dir()

        if not exist:
            try:
                project_lib.create_project_file(
                    perBin,
                    perDoc)
            except Exception:
                return

        else:
            messagebox.showerror(
                "Error", "Progetto giá esistente")
            return

        project_lib.default_project_settings_values()
        self.set_default_values()


        


        messagebox.showinfo("Confirm", "Progetto creato con successo")
