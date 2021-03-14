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

import sys
from time import time
from tkinter import ttk, Label, Scrollbar, Text, FLAT, Frame, StringVar, END, messagebox, Toplevel

from conf.base import MAIN_FRAME_BACKGROUND, BUTTON_FONT, LABEL_BACKGROUND, LABEL_FONT_LARGE, \
    SCROLLABLE_FRAME_BACKGROUND, SCROLLABLE_FRAME_FONT, FRAME_BACKGROUND, VISUALIZE_PAGE_MAIN_LABEL_TEXT, \
    GRAPH_TYPE_MATRIX_TEXT, GRAPH_TYPE_LIST_TEXT, VISUALIZE_PAGE_PAJEK_BUTTON_TEXT, VISUALIZE_PAGE_PLOTLY_BUTTON_TEXT, \
    VISUALIZE_PAGE_MATPLOTLIB_BUTTON_TEXT, VISUALIZE_PAGE_BACK_BUTTON_TEXT, VISUALIZE_PAGE_EXIT_BUTTON_TEXT, \
    VISUALIZE_PAGE_VISUALIZATION_VIA_MATRIX_LIST_ERROR, VISUALIZE_PAGE_VISUALIZATION_COMPLETED_SUCCESS, \
    VISUALIZE_PAGE_VISUALIZATION_FAILED_ERROR, VISUALIZE_PAGE_3D_VISUALIZATION_VIA_MATRIX_LIST_ERROR, \
    VISUALIZE_PAGE_PLOTLY_FAILED_ERROR, VISUALIZE_PAGE_PLOTLY_WAIT_INFO, VISUALIZE_PAGE_PLOTLY_GRAPH_CREATE_SUCCESS, \
    VISUALIZE_PAGE_PLOTLY_FAILED_NO_GRAPH_GENERATED_ERROR
from gui.pages.custom_pop_up import CustomPopUp
from gui.pages.login_creads import LoginCreds
from gui.pages.page import Page
from os_recon.define_os import transform


class GraphVisualizePage(Page):
    def __init__(self, parent, controller):
        super(GraphVisualizePage, self).__init__(parent)

        self.configure(bg=MAIN_FRAME_BACKGROUND)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(20, weight=1)

        # Button font
        self.button_font = BUTTON_FONT

        # Main Label
        self.main_label = Label(self, bg=LABEL_BACKGROUND, text=VISUALIZE_PAGE_MAIN_LABEL_TEXT, font=LABEL_FONT_LARGE)
        self.main_label.grid(row=1, column=1, padx=20)

        # Text Area Frame
        # create a Frame for the Text and Scrollbar
        self.my_frame_inner = ttk.Frame(self)
        # create a Scrollbar and associate it with txt
        self.my_scroll = Scrollbar(self.my_frame_inner, orient='vertical')
        # create a Text widget
        self.text_area = Text(self.my_frame_inner, background=SCROLLABLE_FRAME_BACKGROUND,
                              yscrollcommand=self.my_scroll.set, width=35, height=23, relief=FLAT, borderwidth=5)
        self.text_area.bind("<FocusIn>", self.defocus)
        self.text_area.config(font=SCROLLABLE_FRAME_FONT, undo=True, wrap='word')
        self.my_scroll.config(command=self.text_area.yview)

        self.my_frame_inner.grid(row=1, column=2, rowspan=13, columnspan=2, sticky='nesw')
        self.text_area.grid(row=1, column=2, rowspan=13)
        self.my_scroll.grid(row=1, column=3, rowspan=13, columnspan=2, sticky='nesw')

        # Buttons Frame
        self.buttons_frames = Frame(self, bg=FRAME_BACKGROUND)
        self.buttons_frames.grid_propagate(0)
        self.buttons_frames.configure(height=250, width=400)
        self.buttons_frames.grid(row=2, column=1, padx=10)

        self.adjacency_type_selected = StringVar()
        self.matrix = ttk.Radiobutton(self.buttons_frames, text=GRAPH_TYPE_MATRIX_TEXT, value="Matrix",
                                      variable=self.adjacency_type_selected)
        self.matrix.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        self.list = ttk.Radiobutton(self.buttons_frames, text=GRAPH_TYPE_LIST_TEXT, value="List",
                                    variable=self.adjacency_type_selected)
        self.list.grid(row=0, column=1, padx=30, pady=10, sticky="w")

        # Pajek Visualize Button
        self.pajek_visualize_button = ttk.Button(self.buttons_frames, text=VISUALIZE_PAGE_PAJEK_BUTTON_TEXT,
                                                 command=self.pajek_visualize)
        self.pajek_visualize_button.grid(row=1, column=0, ipady=10, ipadx=15)

        # Plotly Visualize Button
        self.plotly_visualize_button = ttk.Button(self.buttons_frames, text=VISUALIZE_PAGE_PLOTLY_BUTTON_TEXT,
                                                  command=self.Spawn_Login_Creds)
        self.plotly_visualize_button.grid(row=1, column=1, ipady=10, ipadx=15)

        # 2D Matplotlib Visualize Button
        self.matplotlib_visualize_button = ttk.Button(self.buttons_frames, text=VISUALIZE_PAGE_MATPLOTLIB_BUTTON_TEXT,
                                                      command=self.Plot_2D)
        self.matplotlib_visualize_button.grid(row=2, column=0, ipady=10, ipadx=15, pady=10)

        # Back Button
        self.back_button = ttk.Button(self.buttons_frames, text=VISUALIZE_PAGE_BACK_BUTTON_TEXT,
                                      command=lambda: self.back(controller))
        self.back_button.grid(row=3, column=0, ipady=10, ipadx=15, pady=10)

        # Exit Button
        self.exit_button = ttk.Button(self.buttons_frames, text=VISUALIZE_PAGE_EXIT_BUTTON_TEXT,
                                      command=lambda: sys.exit(0))
        self.exit_button.grid(row=3, column=1, ipady=10, ipadx=15, pady=10, padx=45)

    @staticmethod
    def defocus(event):
        event.widget.master.focus_set()

    def back(self, controller):
        self.text_area.delete('1.0', END)
        self.text_area.update()

        controller.show_frame(self.retrieve_frame(controller, 'MainPage'), transform)

    def pajek_visualize(self):
        """ Visualizes the generated graph with the appropriate file format that pajek needs. """
        from visualize.pajek_visualize import Visualizer

        if self.adjacency_type_selected.get() == "":
            messagebox.showerror('Error!', VISUALIZE_PAGE_VISUALIZATION_VIA_MATRIX_LIST_ERROR)
        elif self.adjacency_type_selected.get() == "Matrix":
            if Visualizer.pajek_visualize_matrix():
                messagebox.showinfo('Success!', VISUALIZE_PAGE_VISUALIZATION_COMPLETED_SUCCESS)
            else:
                messagebox.showerror("Error", VISUALIZE_PAGE_VISUALIZATION_FAILED_ERROR)
        elif self.adjacency_type_selected.get() == "List":
            if Visualizer.pajek_visualize_list():
                messagebox.showinfo('Success!', VISUALIZE_PAGE_VISUALIZATION_COMPLETED_SUCCESS)
            else:
                messagebox.showerror("Error", VISUALIZE_PAGE_VISUALIZATION_FAILED_ERROR)

    def Spawn_Login_Creds(self):
        if self.adjacency_type_selected.get() == "":
            messagebox.showerror("Error", VISUALIZE_PAGE_3D_VISUALIZATION_VIA_MATRIX_LIST_ERROR)
        else:
            root2 = Toplevel()
            creds_GUI = LoginCreds(root2)
            self.master.wait_window(root2)

            if creds_GUI.username_entry_result == "" or creds_GUI.api_key_entry_result == "":
                self.text_area.delete('1.0', END)
                self.text_area.update()
                self.text_area.insert(END, VISUALIZE_PAGE_PLOTLY_FAILED_ERROR)
                self.text_area.update()
            else:
                self.plotly_visualize(creds_GUI.username_entry_result, creds_GUI.api_key_entry_result,
                                      creds_GUI.filename_entry_result)

    def plotly_visualize(self, username, api_key, output_filename):
        """ Visualizes the generated graph in 3D form with the appropriate file format that plotly needs. """

        from visualize.plotly_3d import Plotly3D
        plotly_visualizer = Plotly3D(edges_pixels=5)
        start = time()

        self.text_area.delete('1.0', END)
        self.text_area.insert(END, VISUALIZE_PAGE_PLOTLY_WAIT_INFO)
        self.text_area.update()

        try:
            plot_result = False

            if self.adjacency_type_selected.get() == "Matrix":
                plot_result = plotly_visualizer.plotly_visualize_matrix(username, api_key, output_filename)
            elif self.adjacency_type_selected.get() == "List":
                plot_result = plotly_visualizer.plotly_visualize_list(username, api_key, output_filename)

            if plot_result is True:
                end_3d = time() - start
                self.text_area.insert(END, VISUALIZE_PAGE_PLOTLY_GRAPH_CREATE_SUCCESS)
                message3 = "[+] Elapsed time: {:>.2f} sec\n".format(end_3d)
                self.text_area.insert(END, message3)
                self.text_area.update()
                self.Spawn_Custom_Popup(plotly_visualizer.link)
            elif plot_result == "File not found":
                self.text_area.delete('1.0', END)
                messagebox.showerror("Error", VISUALIZE_PAGE_PLOTLY_FAILED_NO_GRAPH_GENERATED_ERROR)
            else:
                self.text_area.delete('1.0', END)
                self.text_area.update()
                self.text_area.insert(END, VISUALIZE_PAGE_PLOTLY_FAILED_ERROR)
                self.text_area.update()
                self.Spawn_Login_Creds()
        except TypeError:
            self.text_area.delete('1.0', END)
            self.text_area.update()
            self.text_area.insert(END, VISUALIZE_PAGE_PLOTLY_FAILED_ERROR)
            self.text_area.update()

    def Plot_2D(self):
        import visualize.plot_2d

        plot = visualize.plot_2d.Plot2D()

        if self.adjacency_type_selected.get() == "":
            messagebox.showerror('Error!', VISUALIZE_PAGE_VISUALIZATION_VIA_MATRIX_LIST_ERROR)
        elif self.adjacency_type_selected.get() == "Matrix":
            if plot.graph_topology_matrix():
                plot.extract_possibilities()
                plot.plot_2d("Matrix")
            else:
                messagebox.showerror("Error", VISUALIZE_PAGE_VISUALIZATION_FAILED_ERROR)
        elif self.adjacency_type_selected.get() == "List":
            if plot.graph_topology_list():
                plot.extract_possibilities()
                plot.plot_2d("List")
            else:
                messagebox.showerror("Error", VISUALIZE_PAGE_VISUALIZATION_FAILED_ERROR)

    def Spawn_Custom_Popup(self, url):
        root3 = Toplevel()
        custom_popup = CustomPopUp(root3)
        custom_popup.plotly_popup(url)
        self.master.wait_window(root3)
