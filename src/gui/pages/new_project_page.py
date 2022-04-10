# -*- coding: utf-8 -*-
__autor__ = "Francesco"
__version__ = "0101 2022/03/19"
from customtkinter import *
from tkinter import StringVar, messagebox, scrolledtext

from ...lib import project_lib


PROJECT_SETTINGS_FILE = "project_settings.json"


class NewProjectPage(CTkFrame):
    def __init__(self, master):

        super().__init__(master)

        # configure grid layout (3x7)
        for i in [0, 1, 2, 3]:
            self.rowconfigure(i, weight=1)
        self.rowconfigure(5, weight=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.title = CTkLabel(master=self,
                              text="Nuovo progetto",
                              text_font=("Roboto Medium", 20))  # font name and size in px
        self.title.grid(row=0, column=1, pady=20)

        self.entry_text = StringVar()

        self.project_name_entry = self.init_CTkEntry()
        self.set_default_values()

        self.project_name_entry.grid(
            row=1, column=0, columnspan=3, padx=20, pady=20)

        self.add_entry_text_trace()

        self.description_window_open = False
        self.lenguage_button = CTkButton(
            self, text="Inserisci descrizione",
            fg_color=("gray75", "gray30"),  # <- custom tuple-color
            command=self.create_description_toplevel)
        self.lenguage_button.grid(row=2, column=1, padx=40)

        self.lenguage_window_open = False
        self.lenguage_button = CTkButton(
            self, text="Scegli linguaggio",
            fg_color=("gray75", "gray30"),  # <- custom tuple-color
            command=self.create_lenguage_toplevel)
        self.lenguage_button.grid(row=3, column=1, padx=30)

        self.auto_readme = False
        self.auto_readme_switch = CTkSwitch(master=self,
                                            text="Abilitare AutoReadme",
                                            command=self.change_auto_readme)
        self.auto_readme_switch.grid(row=4, column=1, padx=40, pady=30)

        self.lenguage_button = CTkButton(
            self, text="Crea Progetto",
            fg_color=("gray75", "gray30"),  # <- custom tuple-color
            command=self.submit_all)
        self.lenguage_button.grid(
            row=5, column=0, columnspan=3, padx=30, pady=30, sticky="se")

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

    def create_lenguage_toplevel(self):
        def on_closing():
            if not self.lenguage_selected_check():
                return

            self.lenguage_window_open = False
            self.lenguages_window.destroy()

        def select_lenguage(lenguage):
            try:
                value = lenguage_switch[lenguage].get()
            except KeyError:
                return
            selected_lenguage_list: list = project_lib.get_key_value_JSON(
                PROJECT_SETTINGS_FILE, "linguaggi_selezionati")
            if value:
                selected_lenguage_list.append(lenguage)
            else:
                try:
                    selected_lenguage_list.remove(lenguage)
                except ValueError:
                    pass
            project_lib.update_key_JSON(
                PROJECT_SETTINGS_FILE, "linguaggi_selezionati", selected_lenguage_list)

        if not self.lenguage_window_open:
            self.lenguage_window_open = True
            self.lenguages_window = CTkToplevel(self)
            self.lenguages_window.geometry("350x300")

            self.lenguages_window.protocol("WM_DELETE_WINDOW", on_closing)

            self.lenguages_window.columnconfigure(0, weight=1)
            self.lenguages_window.rowconfigure(1, weight=1)

            frame = CTkFrame(master=self.lenguages_window,
                             corner_radius=10)
            frame.grid(row=1, column=0, padx=20, pady=20, sticky="nswe")
            # configure grid layout (3x7)
            for i in range(3):
                frame.rowconfigure(i, weight=1)
            frame.rowconfigure(7, weight=10)
            frame.columnconfigure(0, weight=1)

            # create label on CTkToplevel self.lenguages_window

            label = CTkLabel(self.lenguages_window, text="Selezione dei linguaggi",
                             text_font=("Roboto Medium", 17))
            label.grid(row=0, column=0, pady=10)

            supported_leguages = project_lib.get_key_value_JSON(
                "config.json", "supported_leguages")

            lenguage_switch = {}
            selected_lenguage_list: list = project_lib.get_key_value_JSON(
                PROJECT_SETTINGS_FILE, "linguaggi_selezionati")
            for lenguage in supported_leguages:
                i += 1
                var = CTkSwitch(master=frame,
                                text=lenguage,
                                command=lambda bound_lenguage=lenguage: select_lenguage(
                                    bound_lenguage))
                var.grid(row=i, column=0, pady=10)
                if lenguage in selected_lenguage_list:
                    var.select()

                lenguage_switch[lenguage] = var
            submit_button = CTkButton(master=frame,
                                      text="Fatto",
                                      fg_color=("gray75", "gray30"),
                                      command=on_closing)
            submit_button.grid(row=7, column=0, pady=10, padx=10, sticky="se")

        elif self.lenguages_window != None:
            self.lenguages_window.focus_force()

    def create_description_toplevel(self):
        
        def clear_text():
            text_area.delete("1.0", "end")

        def on_closing():

            description = text_area.get("1.0", tkinter.END).rstrip("\n")

            project_lib.update_key_JSON(
                PROJECT_SETTINGS_FILE, "descrizione", description)

            self.description_window_open = False
            self.description_window.destroy()

        if not self.description_window_open:
            self.description_window_open = True
            self.description_window = CTkToplevel(self)
            self.description_window.geometry("350x300")

            self.description_window.protocol("WM_DELETE_WINDOW", on_closing)

            self.description_window.columnconfigure(0, weight=1)
            self.description_window.rowconfigure(1, weight=1)

            frame = CTkFrame(master=self.description_window,
                             corner_radius=10)
            frame.grid(row=1, column=0, padx=20, pady=20, sticky="nswe")
            # configure grid layout (3x7)
            for i in range(3):
                frame.rowconfigure(i, weight=1)
            frame.rowconfigure(5, weight=10)
            frame.columnconfigure(0, weight=1)

            # create label on CTkToplevel self.description_window

            label = CTkLabel(self.description_window, text="Descrizione",
                             text_font=("Roboto Medium", 17))
            label.grid(row=0, column=0, pady=10)

            text_area = scrolledtext.ScrolledText(frame, wrap=tkinter.WORD,
                                                  width=40, height=8,
                                                  font=("Roboto Medium", 10))
            text_area.insert(tkinter.INSERT,
                             project_lib.get_key_value_JSON(PROJECT_SETTINGS_FILE, "descrizione").rstrip("\n"))

            text_area.grid(column=0, row=0, pady=10, padx=10)

            # placing cursor in text area
            text_area.focus()

            submit_button = CTkButton(master=frame,
                                      text="Fatto",
                                      fg_color=("gray75", "gray30"),
                                      command=on_closing)
            submit_button.grid(row=5, column=0, pady=10, padx=10, sticky="se")

            clear_button = CTkButton(master=frame,
                                     text="Cancella",
                                     fg_color=("gray75", "gray30"),
                                     command=clear_text)
            clear_button.grid(row=5, column=0, pady=10, padx=10, sticky="sw")

        elif self.description_window != None:
            self.description_window.focus_force()

    def project_title_check(self, project_title):
        if (project_title == "" or len(project_title) < 3):
            messagebox.showerror(
                "Invalid Input", "Inserire un titolo valido o\ncaratteri minimi 3")
            return False
        if any((c in "/\\:,.") for c in project_title):
            messagebox.showerror(
                "Invalid Input", "Inserire un titolo valido \ncaratteri /\\:,. non consentiti")
            return False
        return True

    def lenguage_selected_check(self):
        if project_lib.get_key_value_JSON(PROJECT_SETTINGS_FILE, "linguaggi_selezionati") == []:
            messagebox.showerror(
                "Error", "Devi selezionare minimo 1 linguaggio")
            self.create_lenguage_toplevel()
            return False
        return True

    def submit_all(self):
    
        project_title = self.project_name_entry.get()
        if not self.project_title_check(project_title) or not self.lenguage_selected_check():
            return
        project_lib.update_key_JSON(
            PROJECT_SETTINGS_FILE, "nome_progetto", project_title)

        if project_lib.get_key_value_JSON(PROJECT_SETTINGS_FILE, "descrizione") == "":
            empty_description = messagebox.askquestion("Empty description",
                                                       'La descrizione é vuota, vuoi aggiungerne una?', icon='warning')
            if empty_description == "yes":
                self.create_description_toplevel()
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

        for widget in list(self.children.values()):
            if widget.__class__ == CTkToplevel:
                widget.destroy()
        self.description_window_open = False
        self.lenguage_window_open = False
        messagebox.showinfo("Confirm", "Progetto creato con successo")
