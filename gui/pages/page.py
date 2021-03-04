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
from tkinter import messagebox
from sqlite3_db.database import *
from gui.pages.mousewheel import *
from os_recon.define_os import transform, platform_type
from support_folders.multithreading import StoppableThread
from support_folders.run_length_encoder import RunLengthEncoder


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def retrieve_frame(self, controller, frame_name: str):
        return next(val for val in controller.frames.keys() if val.__name__ == frame_name)
