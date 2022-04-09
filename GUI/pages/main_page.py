# -*- coding: utf-8 -*-
__autor__ = "Francesco"
__version__ = "0101 2022/03/19"

from customtkinter import *


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
