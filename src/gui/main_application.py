import tkinter

from PIL import Image
from PIL.ImageTk import PhotoImage
from customtkinter import *

from .pages import main_page, settings_page, new_project_page, settings_page_enum, new_project_enum
from .pages.new_project_pages import edit_description_page, recent_project_page
from .pages.settings_pages import edit_header_page, edit_variables_page
from ..gui import main_page_enum
from ..lib import project_lib

# Modes: "System" (standard), "Dark", "Light"
set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
set_default_color_theme("blue")


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

        self.frame_right = main_page.MainPage(self)
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
                                            fg_color=("gray65", "gray25"),
                                            command=lambda: self.chose_frame(main_page_enum.MainPageEnum.NEW_PROJECT))
        self.new_project_button.grid(row=2, column=0, pady=10, padx=20)

        self.sort_project_button = CTkButton(master=self.frame_left,
                                             text="Ordina Progetti",
                                             # <- custom tuple-color
                                             fg_color=("gray65", "gray25"),
                                             command=lambda: self.chose_frame(main_page_enum.MainPageEnum.SORT_PROJECT))
        self.sort_project_button.grid(row=3, column=0, pady=10, padx=20)
        self.sort_project_button.configure(state=tkinter.DISABLED)

        self.settings_button = CTkButton(master=self.frame_left,
                                         text="Settings",
                                         height=35,
                                         compound="right",
                                         image=PhotoImage(Image.open(project_lib.get_image_path(
                                             "settings_icon.png")).resize((30, 30))),
                                         # <- custom tuple-color
                                         fg_color=("gray65", "gray25"),
                                         command=lambda: self.chose_frame(main_page_enum.MainPageEnum.SETTINGS))
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
            case main_page_enum.MainPageEnum.NEW_PROJECT:
                self.change_right_frame(new_project_page.NewProjectPage(self, self))

            case main_page_enum.MainPageEnum.SORT_PROJECT:
                # TODO sort project
                pass

            case main_page_enum.MainPageEnum.SETTINGS:
                self.change_right_frame(settings_page.SettingsPage(self, self))

            case new_project_enum.NewProjectPageEnum.DESCRIPTION:
                self.change_right_frame(
                    edit_description_page.EditDescriptionPage(self, self))

            case new_project_enum.NewProjectPageEnum.RECENT:
                self.change_right_frame(
                    recent_project_page.RecentProjectPage(self, self))

            case settings_page_enum.SettingsPageEnum.EDIT_HEADER:
                self.change_right_frame(edit_header_page.EditHeadersPage(self, self))

            case settings_page_enum.SettingsPageEnum.EDIT_VARIABLE:
                self.change_right_frame(edit_variables_page.EditVariablePage(self, self))

            case settings_page_enum.SettingsPageEnum.EDIT_FLAG:
                pass

            case _:
                self.change_right_frame(main_page.MainPage(self))

    def change_mode(self):
        if self.switch_dark_mode.get() == 1:
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")

    def clear_frame_right(self):
        self.frame_right.destroy()

    def on_closing(self):
        self.destroy()

    def start(self):
        self.mainloop()
