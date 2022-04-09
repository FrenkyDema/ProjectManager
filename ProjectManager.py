from enum import Enum
from pathlib import Path
import sys
import os
import json
import re
from customtkinter import *
from tkinter import StringVar, messagebox, scrolledtext
import project_lib

PROJECT_SETTINGS_FILE = "project_settings.json"
CONFIG_FILE = "config.json"


class MainPageEnum(Enum):
    SETTINGS = 1
    NEW_PROJECT = 2
    SORT_PROJECT = 3


class SettingsPageEnum(Enum):
    EDIT_HEADER = 1
    EDIT_VARIABLE = 2
    EDIT_FLAG = 3


class App(CTk):
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Project Manager")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)

        # ============ create two frames ============

        # configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame_left = CTkFrame(master=self,
                                   width=180,
                                   corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = MainPage(self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout
        # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)
        # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)

        self.label_1 = CTkLabel(master=self.frame_left,
                                text="ProjectManager",
                                text_font=("Roboto Medium", -16),
                                )  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.new_project_button = CTkButton(master=self.frame_left,
                                            text="Nuovo Progetto",
                                            # <- custom tuple-color
                                            fg_color=("gray75", "gray30"),
                                            command=lambda: self.chose_frame(MainPageEnum.NEW_PROJECT))
        self.new_project_button.grid(row=2, column=0, pady=10, padx=20)

        self.sort_project_button = CTkButton(master=self.frame_left,
                                             text="Ordina Progetti",
                                             # <- custom tuple-color
                                             fg_color=("gray75", "gray30"),
                                             command=lambda: self.chose_frame(MainPageEnum.SORT_PROJECT))
        self.sort_project_button.grid(row=3, column=0, pady=10, padx=20)
        self.sort_project_button.config(state=tkinter.DISABLED)

        self.settings_button = CTkButton(master=self.frame_left,
                                         text="Settings",
                                         # <- custom tuple-color
                                         fg_color=("gray75", "gray30"),
                                         command=lambda: self.chose_frame(MainPageEnum.SETTINGS))
        self.settings_button.grid(
            row=9, column=0, pady=10, padx=20, sticky="w")

        self.switch_dark_mode = CTkSwitch(master=self.frame_left,
                                          text="Dark Mode",
                                          command=self.change_mode)
        self.switch_dark_mode.select()
        self.switch_dark_mode.grid(
            row=10, column=0, pady=10, padx=20, sticky="w")

    def change_right_frame(self, frame: CTkFrame):
        self.clear_frame_right()

        self.frame_right = frame

        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

    def chose_frame(self, page_type):
        match page_type:
            case MainPageEnum.NEW_PROJECT:
                self.change_right_frame(NewProjectPage(self))

            case MainPageEnum.SORT_PROJECT:
                # TODO sort project
                pass

            case MainPageEnum.SETTINGS:
                self.change_right_frame(SettingsPage(self, self))

            case _:
                self.change_right_frame(MainPage(self))

    def change_mode(self):
        if self.switch_dark_mode.get() == 1:
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")

    def clear_frame_right(self):
        self.frame_right.destroy()

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


class MainPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # configure grid layout (3x7)
        for i in [0, 1, 2, 3]:
            self.rowconfigure(i, weight=1)
        self.rowconfigure(7, weight=10)
        self.columnconfigure(0, weight=1)

        title = CTkLabel(master=self,
                         text="Project Manager",
                         text_font=("Roboto Medium", 20))  # font name and size in px
        title.grid(row=0, column=0, pady=20)

        self.label_info_1 = CTkLabel(master=self,
                                     text="Questa apprlicazione é stata creata per permettere un\n" +
                                          "ottimizzazione nella gestione del proprio progetto.\n\n" +
                                          "Clicca su uno dei bottoni qui a fianco " +
                                          "per scegliere cosa fare.",
                                     height=100,
                                     # <- custom tuple-color
                                     fg_color=("white", "gray38"),
                                     justify=tkinter.CENTER,
                                     text_font=("Roboto Medium", -15))
        self.label_info_1.grid(row=1, column=0, sticky="nwe", padx=15, pady=15)


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


class SettingsPage(CTkFrame):
    def __init__(self, master, app: App):
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
            fg_color=("gray75", "gray30"),
            command=lambda: self.change_page(SettingsPageEnum.EDIT_HEADER))
        button_1.grid(row=1, column=1,
                      padx=20, sticky="we")

        edit_variable_button = CTkButton(
            master=self,
            text="Modifica variabili",
            fg_color=("gray75", "gray30"),
            command=lambda: self.change_page(SettingsPageEnum.EDIT_VARIABLE))
        edit_variable_button.grid(row=2, column=1,
                                  padx=20, sticky="we")
        edit_variable_button.config(state=tkinter.DISABLED)

        edit_flag_button = CTkButton(
            master=self, text="Modifica flags",
            fg_color=("gray75", "gray30"),
            command=lambda: self.change_page(SettingsPageEnum.EDIT_FLAG))
        edit_flag_button.grid(row=3, column=1,
                              padx=20, sticky="we")
        edit_flag_button.config(state=tkinter.DISABLED)

    def change_page(self, page_type):
        match page_type:
            case SettingsPageEnum.EDIT_HEADER:
                self.app.change_right_frame(
                    EditHeadersPage(self.app, self.app))

            case SettingsPageEnum.EDIT_VARIABLE:
                pass

            case SettingsPageEnum.EDIT_FLAG:
                pass

            case _:
                pass


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
                on_closing(window, messagebox.askyesno(
                    "Save", "Salvare modifiche?"))

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

                window.protocol("WM_DELETE_WINDOW",
                                lambda: save_request(window))

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


if __name__ == "__main__":

    app = App()
    app.start()
