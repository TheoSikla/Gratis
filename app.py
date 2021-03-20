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
import sys
from argparse import RawTextHelpFormatter
from tkinter import Tk, ttk, Menu

from colorama import init

from cli.common import MessageType
from cli.utils import validate_model_cli_args, handle_graph_creation, communicate_cli_message
from conf.base import *
from graphs.graph import AVAILABLE_GRAPH_TYPES, AVAILABLE_GRAPH_TYPES_NUMBERED, AVAILABLE_GRAPH_REPRESENTATION_TYPES, \
    AVAILABLE_GRAPH_REPRESENTATION_TYPES_NUMBERED
from gui.pages.analyze import GraphAnalyzePage
from gui.pages.generate import GraphGeneratePage
from gui.pages.history import GraphHistoryPage
from gui.pages.main import MainPage
from gui.pages.settings import SettingsPage
from gui.pages.utils import spawn_top_level
from gui.pages.visualize import GraphVisualizePage


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
                             highlightbackground=BUTTON_IMAGE_BACKGROUND,
                             relief=BUTTON_RELIEF, width=BUTTON_WIDTH)
        self.style.configure('TFrame', background=FRAME_BACKGROUND)
        self.style.configure('TRadiobutton', background=RADIOBUTTON_BACKGROUND, foreground=RADIOBUTTON_FOREGROUND,
                             relief=RADIOBUTTON_RELIEF, font=self.button_font)
        self.style.configure('TCheckbutton', background=CHECKBUTTON_BACKGROUND, foreground=CHECKBUTTON_FOREGROUND,
                             relief=CHECKBUTTON_RELIEF, font=self.button_font)
        self.style.configure('TLabel', background=LABEL_BACKGROUND, foreground=LABEL_FOREGROUND)
        self.style.configure('HistoryPage.Counter.TLabel', background=LABEL_BACKGROUND,
                             foreground=LABEL_FOREGROUND, width=5, height=10)
        self.style.configure('HistoryPage.Content.TLabel', background=LABEL_BACKGROUND,
                             foreground=LABEL_FOREGROUND, width=10, justify="left", anchor="nw")

        # Build main menu
        # File menu
        file_menu = Menu(bg=MENU_ITEMS_BACKGROUND, tearoff=False)
        file_menu.add_command(label=FILE_SETTINGS_LABEL_TEXT, font=MENU_ITEMS_FONT,
                              command=lambda: spawn_top_level([SettingsPage], kwargs={
                                'master': self,
                                'title': FILE_SETTINGS_LABEL_TEXT,
                                'width': SETTINGS_WINDOW_WIDTH,
                                'height': SETTINGS_WINDOW_HEIGHT,
                                'bg': MAIN_FRAME_BACKGROUND
                              }, topmost=True))
        file_menu.add_command(label=FILE_EXIT_LABEL_TEXT, font=MENU_ITEMS_FONT, command=self.destroy)

        # Main menu
        menu = Menu(master=self, bg=MENU_BACKGROUND, fg=MENU_FOREGROUND, relief=MENU_RELIEF, font=MENU_FONT,
                    activebackground=MENU_BACKGROUND)
        file_menu.master = menu
        self.config(menu=menu)
        menu.add_cascade(label=FILE_LABEL_TEXT, menu=file_menu)
        menu.add_command(label='')

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
        self.show_frame(MainPage, MAIN_WINDOW_DIMENSIONS_STR)

    def load_style(self):
        style = reload()
        # ttk style configuration
        self.button_font = (
            style['button']['font']['family'],
            style['button']['font']['size'],
            style['button']['font']['style']
        )
        self.config(bg=style['main_frame_bg'])
        self.style = ttk.Style()
        self.style.configure('TButton', background=style['button']['bg'], foreground=style['button']['fg'],
                             relief=style['button']['relief'], width=style['button']['width'])
        self.style.configure('TFrame', background=style['frame']['bg'])
        self.style.configure('TRadiobutton', background=style['radiobutton']['bg'],
                             foreground=style['radiobutton']['fg'],
                             relief=style['radiobutton']['relief'], font=self.button_font)
        self.style.configure('TCheckbutton', background=style['checkbutton']['bg'],
                             foreground=style['checkbutton']['fg'],
                             relief=style['checkbutton']['relief'], font=self.button_font)
        self.style.configure('TLabel', background=style['label']['bg'], foreground=style['label']['fg'])
        self.style.configure('HistoryPage.Counter.TLabel', background=style['label']['bg'],
                             foreground=style['label']['fg'], width=5, height=10)
        self.style.configure('HistoryPage.Content.TLabel', background=style['label']['bg'],
                             foreground=style['label']['fg'], width=10, justify="left", anchor="nw")

        for frame in self.frames.values():
            frame.refresh_widget_style(style=style)

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
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    integer_metavar = '{1,2...}'
    parser.add_argument('-g', '--generate', action='store_true', help=ARGPARSE_HELP_STRINGS['generate'])
    parser.add_argument('-m', '--model', type=int, metavar=integer_metavar,
                        help=ARGPARSE_HELP_STRINGS['model'],
                        choices=range(1, len(AVAILABLE_GRAPH_TYPES) + 1))
    parser.add_argument('-gr', '--graph-representation', type=int, metavar=integer_metavar, default=1,
                        help=ARGPARSE_HELP_STRINGS['graph_representation'],
                        choices=range(1, len(AVAILABLE_GRAPH_REPRESENTATION_TYPES) + 1))
    parser.add_argument('-nov', '--number-of-vertices', type=int, metavar='',
                        help=ARGPARSE_HELP_STRINGS['number_of_vertices'])
    parser.add_argument('-noe', '--number-of-edges', type=int, metavar='',
                        help=ARGPARSE_HELP_STRINGS['number_of_edges'])
    parser.add_argument('-noin', '--number-of-initial-nodes', type=int, metavar='',
                        help=ARGPARSE_HELP_STRINGS['number_of_initial_nodes'])
    parser.add_argument('-gd', '--graph-degree', type=int, metavar='', help=ARGPARSE_HELP_STRINGS['graph_degree'])
    parser.add_argument('-icpn', '--initial-connections-per-node', type=int, metavar='',
                        help=ARGPARSE_HELP_STRINGS['initial_connections_per_node'])
    parser.add_argument('-p', '--probability', type=float, metavar='', help=ARGPARSE_HELP_STRINGS['probability'])
    parser.add_argument('-s', '--seed', type=int, metavar='', help=ARGPARSE_HELP_STRINGS['seed'])

    args = parser.parse_args()

    if not len(sys.argv) > 1:
        GUI = App()
        GUI.center()
        GUI.mainloop()
    else:
        if system() == 'Windows':
            init(convert=True)
        App.create_directories()
        if args.generate and args.model:
            args.model = AVAILABLE_GRAPH_TYPES_NUMBERED[args.model]
            args.graph_representation = AVAILABLE_GRAPH_REPRESENTATION_TYPES_NUMBERED[args.graph_representation]
            if not validate_model_cli_args(args):
                communicate_cli_message(message=f'Invalid arguments supplied for the creation of {args.model} graph',
                                        _type=MessageType.ERROR.value)
            else:
                handle_graph_creation(args)
