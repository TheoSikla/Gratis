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

from tkinter import Toplevel, ttk


def center_tk_window(window, height, width):
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    size = (height, width)
    x = w // 2 - size[0] // 2
    y = h // 2 - size[1] // 2
    window.geometry(f"{height}x{width}+{x}+{y}")


def get_top_level(frames, kwargs=None):
    title = kwargs.pop('title')
    width = kwargs.get('width')
    height = kwargs.get('height')

    top_level = Toplevel(**kwargs)
    # Hide the toplevel
    top_level.withdraw()
    top_level.geometry(center_tk_window(window=top_level, height=width, width=height))

    # Create main container frame that will hold all other frames
    top_level.grid_rowconfigure(0, weight=1)
    top_level.grid_columnconfigure(0, weight=1)
    container = ttk.Frame(top_level)
    container.grid(column=0, row=0, sticky="nsew")
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    top_level.__setattr__('container', container)

    # Render all the other frames
    top_level_frames = {}
    for frame in frames:
        _frame = frame(parent=container, controller=top_level)
        top_level_frames[frame] = _frame
        _frame.grid(row=0, column=0, sticky='nsew')

    top_level.__setattr__('frames', top_level_frames)

    # Define the title
    if title:
        top_level.title(title)

    # Raise the first frame
    top_level_frames[frames[0]].tkraise()

    # Make the toplevel visible again
    top_level.deiconify()
    return top_level


def spawn_top_level(frames, kwargs=None):
    top_level = get_top_level(frames, kwargs=kwargs)
    # Get the focus and wait for the toplevel
    top_level.grab_set()
    top_level.attributes('-topmost', True)
    top_level.wait_window(top_level)
