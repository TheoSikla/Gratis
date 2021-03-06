"""
                Copyright (C) 2020 Theodoros Siklafidis

    This file is part of GRATIS.

    GRATIS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GRATIS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GRATIS. If not, see <https://www.gnu.org/licenses/>.
"""

from tkinter import *
from tkinter import ttk
from gui.pages import *
from os_recon.define_os import transform
from conf.base import *


class App(Tk):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.center()
        # Create required directories
        self.create_directories()

        # Root - Frame Configuration
        self.title(APP_NAME)
        self.config(bg=MAIN_FRAME_BACKGROUND)
        self['padx'] = MAIN_FRAME_PADX
        self['pady'] = MAIN_FRAME_PADY
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ttk style configuration
        self.button_font = BUTTON_FONT
        self.style = ttk.Style()
        self.style.configure('TButton', background=BUTTON_BACKGROUND, foreground=BUTTON_FOREGROUND,
                             relief=BUTTON_RELIEF, width=BUTTON_WIDTH)
        self.style.configure('TFrame', background=FRAME_BACKGROUND)
        self.style.configure('TRadiobutton', background=RADIOBUTTON_BACKGROUND, foreground=RADIOBUTTON_FOREGROUND,
                             relief=RADIOBUTTON_RELIEF, font=self.button_font)
        self.style.configure('TCheckbutton', background=CHECKBUTTON_BACKGROUND, foreground=CHECKBUTTON_FOREGROUND,
                             relief=CHECKBUTTON_RELIEF, font=self.button_font)
        self.style.configure('TLabel', background=CHECKBUTTON_BACKGROUND)

        # Main container for Frames
        container = ttk.Frame(self)
        container.grid(column=0, row=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary with all the Frames of the application
        self.frames = {}

        # Load all the Frames
        for F in (MainPage, GraphGeneratePage, GraphAnalyzePage, GraphVisualizePage, GraphHistoryPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # Initiate the MainFrame
        self.show_frame(MainPage, transform)

    def show_frame(self, cont, size):
        self.geometry(size)
        self.update()
        self.update_idletasks()
        self.center()
        frame = self.frames[cont]
        frame.tkraise()

    def center(self):
        size_x = self.winfo_width()
        size_y = self.winfo_height()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = (size_x, size_y)
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2

        self.geometry("%dx%d+%d+%d" % (size + (x, y)))

    @staticmethod
    def create_directories():
        # Create the output folder if it doesn't exist.
        if not os.path.exists(OUTPUT_FILES_DIRECTORY):
            os.makedirs(OUTPUT_FILES_DIRECTORY)


if __name__ == "__main__":
    GUI = App()
    GUI.center()
    GUI.mainloop()
