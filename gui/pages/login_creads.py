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
from tkinter import BooleanVar, messagebox, END
from tkinter import ttk

from gui.pages.page import Page
from sqlite3_db.database import User


class LoginCreds(Page):
    def __init__(self, parent, controller, kwargs=None):
        super(LoginCreds, self).__init__(parent)

        self.controller = controller
        self.forget_credentials_variable = BooleanVar(False)
        self.user_connection_handler = User()

        # Fonts & Styles
        self.label_font = ("Dialog", 11, "bold italic")
        self.button_font = ("Dialog", 9, "bold italic")

        self.controller.protocol('WM_DELETE_WINDOW', self.x_button)

        self.main_label = ttk.Label(self, text="Enter your plotly credentials in order to generate a 3D Graph.",
                                    font=("Arial", 13, "bold"))
        self.main_label.grid(row=0, columnspan=2, ipady=10)

        self.username_label = ttk.Label(self, text="Username")
        self.username_label.grid(row=1, column=0, pady=5, padx=5, sticky="e")

        self.username_entry_result = ""
        self.username_entry = ttk.Entry(self, text="Username")
        self.username_entry.grid(row=1, column=1, padx=5, ipadx=15, ipady=2, sticky="w")

        self.api_key_label = ttk.Label(self, text="API_Key")
        self.api_key_label.grid(row=2, column=0, pady=5, padx=5, sticky="e")

        self.api_key_entry_result = ""
        self.api_key_entry = ttk.Entry(self, text="API Key", show="*")
        self.api_key_entry.grid(row=2, column=1, padx=5, ipadx=15, ipady=2, sticky="w")

        self.filename_label = ttk.Label(self, text="Output Filename")
        self.filename_label.grid(row=3, column=0, pady=5, padx=5, sticky="e")

        self.filename_entry_result = ""
        self.filename_entry = ttk.Entry(self, text="Out Filename")
        self.filename_entry.grid(row=3, column=1, padx=5, ipadx=15, ipady=2, sticky="w")

        self.remember_me_variable = BooleanVar(False)
        self.remember_me_checkbutton = ttk.Checkbutton(self, text="Remember me",
                                                       variable=self.remember_me_variable)
        self.remember_me_checkbutton.grid(row=4, column=0, pady=10)

        self.no_account_label = ttk.Label(self, text="Don't have an account on Plotly?", cursor="hand2",
                                          font=("Arial", 10, "bold"))
        self.no_account_label.grid(row=5, columnspan=2, pady=5)
        self.no_account_label.bind("<Button-1>", lambda event, url="https://plot.ly/feed/#/": self.callback(url))

        self.continue_button = ttk.Button(self, text="Continue",
                                          command=self.continue_button_func)
        self.continue_button.grid(row=6, column=0, pady=20, ipady=5)

        self.cancel_button = ttk.Button(self, text="Cancel",
                                        command=self.x_button)
        self.cancel_button.grid(row=6, column=1, pady=20, ipady=5)

        self.forget_credentials = ttk.Checkbutton(self, text="Forget my credentials",
                                                  variable=self.forget_credentials_variable)

        if self.credential_spawn():
            global temp_bg
            temp_bg = "light goldenrod"
            self.forget_credentials.grid(row=4, column=0, sticky="e", columnspan=2, padx=100)

        else:
            temp_bg = "white"

        self.username_entry.configure(background=temp_bg)
        self.api_key_entry.configure(background=temp_bg)

    def continue_button_func(self):
        if self.username_entry.get() == "" or self.api_key_entry.get() == "" or self.filename_entry.get() == "":
            message = "Please enter a Username an API key and an Output filename before continuing!"
            messagebox.showerror("Error!", message)
            self.controller.lift()
            self.controller.focus()
            self.username_entry_result = ""
            self.api_key_entry_result = ""
            self.filename_entry_result = ""
            self.username_entry.delete(0, 'end')
            self.api_key_entry.delete(0, 'end')
            self.credential_spawn()

        else:
            self.username_entry_result = self.username_entry.get()
            self.api_key_entry_result = self.api_key_entry.get()
            self.filename_entry_result = self.filename_entry.get()
            if self.remember_me_variable.get():
                self.user_connection_handler.create(self.username_entry_result, self.api_key_entry_result)

            if self.forget_credentials_variable.get():
                self.user_connection_handler.delete()

            self.username_entry.delete(0, 'end')
            self.api_key_entry.delete(0, 'end')
            self.filename_entry.delete(0, 'end')
            self.controller.destroy()
            if self.remember_me_variable.get():
                self.user_connection_handler.create(self.username_entry_result, self.api_key_entry_result)

    def x_button(self):
        self.username_entry_result = self.username_entry.get()
        self.api_key_entry_result = self.api_key_entry.get()
        if self.remember_me_variable.get() and self.username_entry.get() != "" and self.api_key_entry.get() != "":
            self.user_connection_handler.create(self.username_entry_result, self.api_key_entry_result)

        if self.forget_credentials_variable.get():
            self.user_connection_handler.delete()

        self.username_entry.delete(0, 'end')
        self.api_key_entry.delete(0, 'end')
        self.filename_entry.delete(0, 'end')
        self.username_entry_result = ""
        self.api_key_entry_result = ""

        self.controller.destroy()

    def credential_spawn(self):
        credentials = self.user_connection_handler.get_credentials()
        if self.user_connection_handler.check_user():
            self.username_entry.insert(END, credentials[0])
            self.api_key_entry.insert(END, credentials[1])
            return True

        else:
            return False

    @staticmethod
    def callback(url):
        webbrowser.open_new(r"{}".format(url))
