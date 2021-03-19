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

from tkinter import ttk

from conf.strings import SETTINGS_PAGE_THEMES_TAB_TEXT, SETTINGS_PAGE_LIGHT_THEME_BUTTON_TEXT, \
    SETTINGS_PAGE_DARK_THEME_BUTTON_TEXT
from conf.styles import MAIN_FRAME_BACKGROUND, BUTTON_BACKGROUND, BUTTON_FOREGROUND, BUTTON_WIDTH, BUTTON_RELIEF, \
    NOTEBOOK_TAB_BACKGROUND, NOTEBOOK_TAB_FOREGROUND, NOTEBOOK_TAB_FONT, NOTEBOOK_TAB_BACKGROUND_SELECTED, \
    BUTTON_INTERNAL_PAD_Y, FRAME_BACKGROUND
from gui.pages.page import Page


class SettingsPage(Page):

    def __init__(self, parent, controller):
        super(SettingsPage, self).__init__(parent)

        self.style = ttk.Style()
        self.style.configure('settings.TButton', background=BUTTON_BACKGROUND, foreground=BUTTON_FOREGROUND,
                             relief=BUTTON_RELIEF, width=BUTTON_WIDTH)
        self.style.configure('settings.TFrame', background=FRAME_BACKGROUND)
        self.style.configure('settings.TNotebook', tabmargins=[5, 10, 1, 1])
        self.style.configure('settings.TNotebook.Tab', padding=[5, 5, 5, 5], borderwidth=0,
                             background=NOTEBOOK_TAB_BACKGROUND, foreground=NOTEBOOK_TAB_FOREGROUND,
                             font=NOTEBOOK_TAB_FONT)
        self.style.map('settings.TNotebook.Tab', background=[("selected", NOTEBOOK_TAB_BACKGROUND_SELECTED)],
                       expand=[("selected", [0, 0, 0, 0])])

        # Settings Frame configuration
        self.configure(bg=MAIN_FRAME_BACKGROUND)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create setting tabs
        tab_internal_pad = 10
        tab_control = ttk.Notebook(self, style='settings.TNotebook')

        # Themes tab
        themes_tab_frame = ttk.Frame(tab_control, style='settings.TFrame')

        for i in range(5):
            themes_tab_frame.grid_rowconfigure(i, weight=1)
        themes_tab_frame.grid_columnconfigure(0, weight=1)
        themes_tab_frame.grid_columnconfigure(1, weight=1)

        light_theme_frame = ttk.Frame(themes_tab_frame)
        light_theme_frame.grid(row=0, column=0, sticky="nsew")
        dark_theme_frame = ttk.Frame(themes_tab_frame)
        dark_theme_frame.grid(row=0, column=1, sticky="nsew")
        for i in range(3):
            light_theme_frame.grid_rowconfigure(i, weight=1)
            light_theme_frame.grid_columnconfigure(i, weight=1)
            dark_theme_frame.grid_rowconfigure(i, weight=1)
            dark_theme_frame.grid_columnconfigure(i, weight=1)

        light_theme_button = ttk.Button(master=light_theme_frame, text=SETTINGS_PAGE_LIGHT_THEME_BUTTON_TEXT,
                                        style='settings.TButton')
        light_theme_button.grid(row=1, column=1, ipady=BUTTON_INTERNAL_PAD_Y)

        dark_theme_button = ttk.Button(master=dark_theme_frame, text=SETTINGS_PAGE_DARK_THEME_BUTTON_TEXT,
                                       style='settings.TButton')
        dark_theme_button.grid(row=1, column=1, ipady=BUTTON_INTERNAL_PAD_Y)

        tab_control.add(themes_tab_frame, text=f'{SETTINGS_PAGE_THEMES_TAB_TEXT: ^{tab_internal_pad}s}')
        tab_control.grid(row=0, column=0, sticky="nsew")
