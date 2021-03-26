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

import webbrowser
from os.path import join
from tkinter import ttk, messagebox

from conf.base import OUTPUT_FILES_DIRECTORY, LABEL_LINK_CURSOR
from gui.pages.page import Page


class CustomPopUp(Page):
    def __init__(self, parent, controller, kwargs):
        super(CustomPopUp, self).__init__(parent)
        self.controller = controller
        self.url = kwargs['url']
        self.controller.protocol('WM_DELETE_WINDOW', lambda: self.store_link(self.url, self.controller))

        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

        main_label = ttk.Label(self, text="You successfully sent some data to your account on plotly.\n"
                                          "View your plot in your browser at:", font=("Dialog", 11, "bold italic"))
        main_label.grid(row=0, column=0, columnspan=3)

        link = ttk.Label(self, text=self.url, style='Link.TLabel', cursor=LABEL_LINK_CURSOR)
        link.grid(row=1, column=1)
        link.bind("<Button-1>", lambda event, root2=self.controller: self.callback(self.url, self.controller))

        self.master.bind("<FocusOut>", lambda event: self.alarm(self.controller))

        view_graph_button = ttk.Button(self, text="View on plotly",
                                       command=lambda: self.callback(self.url, self.controller))
        view_graph_button.grid(row=2, column=1, pady=20, ipady=5, sticky="w")

        view_later_button = ttk.Button(self, text="View Later",
                                       command=lambda: self.store_link(self.url, self.controller))
        view_later_button.grid(row=2, column=1, pady=20, ipady=5, sticky="e")

    @staticmethod
    def alarm(controller):
        controller.bell()
        controller.focus_force()

    @staticmethod
    def store_link(url, root2):
        with open(join(OUTPUT_FILES_DIRECTORY, 'plotly_link.txt'), "w") as f:
            f.write(url)
            f.close()

        root2.destroy()

        message_info = f"Plotly 3D url stored in plaintext for later usage under the {OUTPUT_FILES_DIRECTORY} folder" \
                       " with name plotly_link.txt"
        messagebox.showinfo("Saved!", message_info)

    @staticmethod
    def callback(url, root2):
        with open(join(OUTPUT_FILES_DIRECTORY, 'plotly_link.txt'), "w") as f:
            f.write(url)
            f.close()

        root2.destroy()

        message_info = f"Plotly 3D url stored in plaintext for later usage under the {OUTPUT_FILES_DIRECTORY} folder" \
                       " with name plotly_link.txt"
        messagebox.showinfo("Saved!", message_info)
        webbrowser.open_new(r"{}".format(url))
