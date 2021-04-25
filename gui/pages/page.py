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

from tkinter import ttk, END


class Page(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)

    def retrieve_frame(self, controller, frame_name: str):
        return next(val for val in controller.frames.keys() if val.__name__ == frame_name)

    def refresh_widget_style(self, style):
        pass

    @staticmethod
    def handle_text_widget_style_refresh(text_area, style):
        text_area.configure(bg=style['scrollable_frame']['bg'], font=(
            style['scrollable_frame']['font']['family'],
            style['scrollable_frame']['font']['size'],
            style['scrollable_frame']['font']['style']
        ))
        text_area.tag_configure('custom', foreground=style['scrollable_frame']['inserted_text']['fg'])
        existing_text = text_area.get("1.0", END)
        text_area.delete('1.0', END)
        text_area.insert(END, existing_text, 'custom')
