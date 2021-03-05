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

from os.path import join
import webbrowser
from gui.pages.page import *
from conf.base import OUTPUT_FILES_DIRECTORY


class CustomPopUp:

    def __init__(self, master):
        self.master = master
        self.label_font = ("Dialog", 11, "bold italic")

    def plotly_popup(self, url):
        self.master.protocol('WM_DELETE_WINDOW', lambda: self.store_link(url, self.master))
        self.master.focus()
        self.master['padx'] = 20
        self.master['pady'] = 20
        self.master.title("Plotly 3D")

        if platform_type == "Windows":
            self.center(self.master, 480, 150)
        else:
            self.center(self.master, 510, 150)

        main_label = Label(self.master, text="You successfully sent some data to your account on plotly.\n"
                                             "View your plot in your browser at:", font=self.label_font)
        main_label.grid(row=0)

        link = Label(self.master, text=url, fg="blue", cursor="hand2", font=self.label_font)
        link.grid(row=1)
        link.bind("<Button-1>", lambda event, root2=self.master: self.callback(url, self.master))

        self.master.bind("<FocusOut>", lambda event: self.alarm(self.master))

        view_graph_button = ttk.Button(self.master, text="View 3D Graph\non plotly",
                                       command=lambda: self.callback(url, self.master))
        view_graph_button.grid(row=2, padx=80, pady=15, sticky="w")

        view_later_button = ttk.Button(self.master, text="View Later",
                                       command=lambda: self.store_link(url, self.master))
        view_later_button.grid(row=2, padx=80, pady=15, sticky="e")

    @staticmethod
    def alarm(master):
        master.bell()
        master.focus_force()

    @staticmethod
    def store_link(url, root2):
        with open(join(OUTPUT_FILES_DIRECTORY, 'plotly_link.txt'), "w") as f:
            f.write(url)
            f.close()

        root2.destroy()

        message_info = f"Plotly 3D url stored in plaintext for later usage under the {OUTPUT_FILES_DIRECTORY} folder" \
                       " with name Plotly_link.txt"
        messagebox.showinfo("Saved!", message_info)

    @staticmethod
    def callback(url, root2):
        with open(join(OUTPUT_FILES_DIRECTORY, 'plotly_link.txt'), "w") as f:
            f.write(url)
            f.close()

        root2.destroy()

        message_info = f"Plotly 3D url stored in plaintext for later usage under the {OUTPUT_FILES_DIRECTORY} folder" \
                       " with name Plotly_link.txt"
        messagebox.showinfo("Saved!", message_info)
        webbrowser.open_new(r"{}".format(url))

    @staticmethod
    def center(master, size_x, size_y):
        w = master.winfo_screenwidth()
        h = master.winfo_screenheight()
        size = (size_x, size_y)
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        master.geometry("%dx%d+%d+%d" % (size + (x, y)))
