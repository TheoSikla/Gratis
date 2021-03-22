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

from tkinter import ttk, PhotoImage, TclError

from conf.base import LIGHT_THEME_IMAGE_PATH, DARK_THEME_IMAGE_PATH
from conf.settings import Themes, commit_settings, load_settings
from conf.strings import SETTINGS_PAGE_THEMES_TAB_TEXT, SETTINGS_PAGE_LIGHT_THEME_BUTTON_TEXT, \
    SETTINGS_PAGE_DARK_THEME_BUTTON_TEXT
from conf.styles import BUTTON_INTERNAL_PAD_Y
from gui.pages.page import Page


class SettingsPage(Page):
    def __init__(self, parent, controller):
        super(SettingsPage, self).__init__(parent)

        self.controller = controller

        # Settings Frame configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create setting tabs
        tab_internal_pad = 10
        tab_control = ttk.Notebook(self)

        # Themes tab
        themes_tab_frame = ttk.Frame(tab_control)

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

        try:
            light_theme_label = ttk.Label(master=light_theme_frame, text=SETTINGS_PAGE_LIGHT_THEME_BUTTON_TEXT)
            light_theme_label.grid(row=0, column=1, sticky='s')
            light_theme_image = PhotoImage(file=LIGHT_THEME_IMAGE_PATH)
            light_theme_button = ttk.Button(master=light_theme_frame, text=SETTINGS_PAGE_LIGHT_THEME_BUTTON_TEXT,
                                            command=self.light_theme_button_on_click, image=light_theme_image,
                                            style='Settings.TButton')
            light_theme_button.image = light_theme_image
            light_theme_button.grid(row=1, column=1)

            dark_theme_label = ttk.Label(master=dark_theme_frame, text=SETTINGS_PAGE_DARK_THEME_BUTTON_TEXT)
            dark_theme_label.grid(row=0, column=1, sticky='s')
            dark_theme_image = PhotoImage(file=DARK_THEME_IMAGE_PATH)
            dark_theme_button = ttk.Button(master=dark_theme_frame, text=SETTINGS_PAGE_DARK_THEME_BUTTON_TEXT,
                                           command=self.dark_theme_button_on_click, image=dark_theme_image,
                                           style='Settings.TButton')
            dark_theme_button.image = dark_theme_image
            dark_theme_button.grid(row=1, column=1)
        except TclError:
            light_theme_button = ttk.Button(master=light_theme_frame, text=SETTINGS_PAGE_LIGHT_THEME_BUTTON_TEXT,
                                            command=self.light_theme_button_on_click)
            light_theme_button.grid(row=1, column=1, ipady=BUTTON_INTERNAL_PAD_Y)

            dark_theme_image = PhotoImage(file=DARK_THEME_IMAGE_PATH)
            dark_theme_button = ttk.Button(master=dark_theme_frame, text=SETTINGS_PAGE_DARK_THEME_BUTTON_TEXT,
                                           command=self.dark_theme_button_on_click)
            dark_theme_button.grid(row=1, column=1, ipady=BUTTON_INTERNAL_PAD_Y)

        tab_control.add(themes_tab_frame, text=f'{SETTINGS_PAGE_THEMES_TAB_TEXT: ^{tab_internal_pad}s}')
        tab_control.grid(row=0, column=0, sticky="nsew")

    def light_theme_button_on_click(self):
        settings = load_settings()
        settings['theme'] = Themes.LIGHT.value
        commit_settings(settings)
        self.refresh_gui()

    def dark_theme_button_on_click(self):
        settings = load_settings()
        settings['theme'] = Themes.DARK.value
        commit_settings(settings)
        self.refresh_gui()

    def refresh_gui(self):
        self.controller.master.load_style()
