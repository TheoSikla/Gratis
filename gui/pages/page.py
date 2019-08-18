from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlite3_db.Database import *
from gui.pages.mousewheel import *
from os_recon.define_os import transform, platform_type
from Support_Folders.multithreading import StoppableThread
from Support_Folders.run_length_encoder import RunLengthEncoder


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def retrieve_frame(self, controller, frame_name: str):
        return next(val for val in controller.frames.keys() if val.__name__ == frame_name)
