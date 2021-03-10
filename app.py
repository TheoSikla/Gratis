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

import argparse
from tkinter import *
from tkinter import ttk

from cli.common import MessageType
from cli.utils import validate_model_cli_args, handle_graph_creation, communicate_cli_message
from conf.base import *
from graphs.graph import AVAILABLE_GRAPH_TYPES, AVAILABLE_GRAPH_TYPES_NUMBERED, AVAILABLE_GRAPH_REPRESENTATION_TYPES, \
    AVAILABLE_GRAPH_REPRESENTATION_TYPES_NUMBERED
from gui.pages import *
from os_recon.define_os import transform


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
    parser = argparse.ArgumentParser()

    parser.add_argument('-g', '--generate', action='store_true', help='')
    parser.add_argument('-m', '--model', type=int, choices=range(1, len(AVAILABLE_GRAPH_TYPES) + 1), help='')
    parser.add_argument('-at', '--adjacency-type', type=int, help='', default=1,
                        choices=range(1, len(AVAILABLE_GRAPH_REPRESENTATION_TYPES) + 1))
    parser.add_argument('-nov', '--number-of-vertices', type=int, help='')
    parser.add_argument('-noe', '--number-of-edges', type=int, help='')
    parser.add_argument('-noin', '--number-of-initial-nodes', type=int, help='')
    parser.add_argument('-ga', '--graph-degree', type=int, help='')
    parser.add_argument('-icpn', '--initial-connections-per-node', type=int, help='')
    parser.add_argument('-p', '--probability', type=float, help='')
    parser.add_argument('-s', '--seed', type=int, help='')

    args = parser.parse_args()

    if not len(sys.argv) > 1:
        GUI = App()
        GUI.center()
        GUI.mainloop()
    else:
        if args.generate and args.model:
            args.model = AVAILABLE_GRAPH_TYPES_NUMBERED[args.model]
            args.adjacency_type = AVAILABLE_GRAPH_REPRESENTATION_TYPES_NUMBERED[args.adjacency_type]
            if not validate_model_cli_args(args):
                communicate_cli_message(message=f'Invalid arguments supplied for the creation of {args.model} graph',
                                        _type=MessageType.ERROR.value)
                sys.exit(1)
            else:
                handle_graph_creation(args)
