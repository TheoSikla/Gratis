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
from tkinter import ttk, BooleanVar, Text, FLAT, StringVar, IntVar, DISABLED, NORMAL, END, \
    TclError, messagebox

from conf.base import BUTTON_FONT, LABEL_FONT_LARGE, \
    GENERATE_PAGE_MAIN_LABEL_TEXT, \
    SCROLLABLE_FRAME_FONT, SCROLLABLE_FRAME_BACKGROUND, GENERATE_PAGE_SELECT_GRAPH_LABEL_TEXT, LABEL_FONT_MEDIUM, \
    GRAPH_TYPE_MATRIX_TEXT, GRAPH_TYPE_LIST_TEXT, GENERATE_PAGE_INCREMENTAL_GROWTH_TEXT, \
    GENERATE_PAGE_PREFERENTIAL_ATTACHMENT_TEXT, GENERATE_PAGE_NUMBER_OF_VERTICES_LABEL_TEXT, \
    GENERATE_PAGE_NUMBER_OF_INITIAL_NODES_LABEL_TEXT, \
    GENERATE_PAGE_GRAPH_DEGREE_LABEL_TEXT, GENERATE_PAGE_NUMBER_OF_EDGES_LABEL_TEXT, \
    GENERATE_PAGE_INITIAL_CONNECTIONS_PER_NODE_LABEL_TEXT, \
    GENERATE_PAGE_PROBABILITY_LABEL_TEXT, GENERATE_PAGE_SEED_LABEL_TEXT, GENERATE_PAGE_CLASSPATH_LABEL_TEXT, \
    GENERATE_PAGE_GENERATE_BUTTON_TEXT, GENERATE_PAGE_BACK_BUTTON_TEXT, GENERATE_PAGE_EXIT_BUTTON_TEXT, \
    GENERATE_PAGE_CANCEL_BUTTON_TEXT, GENERATE_PAGE_GRAPH_CREATION_CANCEL_IN_PROGRESS_INFO, \
    GENERATE_PAGE_GRAPH_CREATION_CANCEL_COMPLETED_INFO, GENERATE_PAGE_VERTICES_NON_ZERO_ERROR, \
    GENERATE_PAGE_VERTICES_GREATER_THAN_ONE_ERROR, GENERATE_PAGE_ADJACENCY_TYPE_SELECT_ERROR, \
    GENERATE_PAGE_FULL_SCALE_FREE_GENERATE_INFO, GENERATE_PAGE_CUSTOM_FULL_SCALE_FREE_GENERATE_INFO, \
    GENERATE_PAGE_GRAPH_CREATION_SUCCESS, GENERATE_PAGE_GRAPH_DEGREE_GREATER_THAN_ZERO_ERROR, \
    GENERATE_PAGE_SCALE_FREE_PROPERTIES_ERROR, GENERATE_PAGE_INCREMENTAL_GROWTH_ONLY_ERROR, \
    GENERATE_PAGE_SCALE_FREE_VERTICES_GREATER_THAN_ONE_ERROR, GENERATE_PAGE_SCALE_FREE_INITIAL_NODES_NON_ZERO_ERROR, \
    GENERATE_PAGE_SCALE_FREE_VERTICES_INITIAL_NODES_NUMBER_EQUAL_ONE_ERROR, \
    GENERATE_PAGE_SCALE_FREE_VERTICES_LESS_THAN_INITIAL_NODES_ERROR, \
    GENERATE_PAGE_ER_PROBABILITY_GREATER_THAN_ZERO_ERROR, GENERATE_PAGE_CUSTOM_ER_EDGES_GREATER_THAN_ZERO_ERROR, \
    GENERATE_PAGE_CUSTOM_ER_PROBABILITY_GREATER_THAN_ZERO_ERROR, GENERATE_PAGE_CUSTOM_ER_INVALID_NUMBER_OF_EDGES_ERROR, \
    GENERATE_PAGE_CUSTOM_ER_HOMOGENEOUS_WARNING, GENERATE_PAGE_CUSTOM_SCALE_FREE_PROPERTIES_ERROR, \
    GENERATE_PAGE_CUSTOM_SCALE_FREE_VERTICES_GREATER_THAN_ONE_ERROR, \
    GENERATE_PAGE_CUSTOM_SCALE_FREE_MAX_NUMBER_OF_EDGES_GREATER_THAN_ZERO_ERROR, \
    GENERATE_PAGE_CUSTOM_SCALE_FREE_INVALID_NUMBER_OF_EDGES_ERROR, \
    GENERATE_PAGE_CUSTOM_SCALE_FREE_INITIAL_NODES_NON_ZERO_ERROR, \
    GENERATE_PAGE_CUSTOM_SCALE_FREE_INITIAL_CONNECTIONS_PER_NODE_NON_ZERO_ERROR, \
    GENERATE_PAGE_CUSTOM_SCALE_FREE_VERTICES_INITIAL_NODES_NUMBER_EQUAL_ONE_ERROR, \
    GENERATE_PAGE_CUSTOM_SCALE_FREE_VERTICES_LESS_THAN_INITIAL_NODES_ERROR, MAIN_WINDOW_DIMENSIONS_STR
from graphs.graph import GraphRepresentationType, AVAILABLE_GRAPH_TYPES, GraphType
from gui.pages.page import Page
from os_recon.define_os import platform_type
from support_folders.multithreading import StoppableThread


class GraphGeneratePage(Page):

    def __init__(self, parent, controller):
        super(GraphGeneratePage, self).__init__(parent)

        self.parent = parent
        self.controller = controller

        # MainPage Frame configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(20, weight=1)

        # Thread define
        self.thread = StoppableThread(target=self.generate)

        # Button font
        self.button_font = BUTTON_FONT

        # Validators
        self.vcmd_int = (self.master.register(self.validate_int), '%P', '%d')
        self.vcmd_float = (self.master.register(self.validate_float), '%P', '%S', '%d')

        # Type of graph being generated
        self.graph_types = [''] + AVAILABLE_GRAPH_TYPES

        self.rle_var = BooleanVar(False)
        self.rle = ttk.Checkbutton(self, text="Run Length Encoder", variable=self.rle_var)
        # self.rle.grid(row=1, column=2, sticky="w")

        # Main Label
        self.main_label = ttk.Label(self, text=GENERATE_PAGE_MAIN_LABEL_TEXT, font=LABEL_FONT_LARGE)
        self.main_label.grid(row=2, column=1)

        # Text Area Frame
        # create a Frame for the Text and Scrollbar
        self.my_frame_inner = ttk.Frame(self)
        # create a Scrollbar and associate it with txt
        self.my_scroll = ttk.Scrollbar(self.my_frame_inner, orient='vertical')
        # create a Text widget
        self.text_area = Text(self.my_frame_inner, width=35, height=23, relief=FLAT, borderwidth=5,
                              background=SCROLLABLE_FRAME_BACKGROUND,
                              yscrollcommand=self.my_scroll.set)
        self.text_area.bind("<FocusIn>", self.defocus)
        self.text_area.config(font=SCROLLABLE_FRAME_FONT, undo=True, wrap='word')
        self.my_scroll.config(command=self.text_area.yview)

        self.my_frame_inner.grid(row=2, column=2, rowspan=13, columnspan=2, sticky='nesw')
        self.text_area.grid(row=2, column=2, rowspan=13)
        self.my_scroll.grid(row=2, column=3, rowspan=13, columnspan=2, sticky='nesw')

        # Type Label
        self.main_label = ttk.Label(self, text=GENERATE_PAGE_SELECT_GRAPH_LABEL_TEXT, font=LABEL_FONT_MEDIUM)
        self.main_label.grid(row=3, column=1)

        self.chosen_graph = StringVar()
        self.chosen_graph.set(self.graph_types[1])

        self.graphs = ttk.OptionMenu(self, self.chosen_graph, *self.graph_types, command=self.show_parameters)
        self.graphs.grid(row=4, column=1, pady=10)

        # Parameter's Frame
        self.parameters_frame = ttk.Frame(self)
        self.parameters_frame.grid_propagate(0)
        self.parameters_frame.configure(height=230, width=400)
        self.parameters_frame.grid(row=6, column=1)

        # Incremental Growth, Preferential Attachment Checkbuttons for Scale-free Radiobutton
        self.adjacency_type_selected = StringVar()
        self.matrix = ttk.Radiobutton(self.parameters_frame, text=GRAPH_TYPE_MATRIX_TEXT,
                                      value=GraphRepresentationType.MATRIX.value,
                                      variable=self.adjacency_type_selected,
                                      command=self.handle_run_length_encoder_button)
        self.matrix.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        self.list = ttk.Radiobutton(self.parameters_frame, text=GRAPH_TYPE_LIST_TEXT,
                                    value=GraphRepresentationType.LIST.value,
                                    variable=self.adjacency_type_selected,
                                    command=self.handle_run_length_encoder_button)
        self.list.grid(row=0, column=1, padx=30, pady=10, sticky="w")

        self.incremental_growth_selected = BooleanVar()
        self.incremental_growth = ttk.Checkbutton(self.parameters_frame, text=GENERATE_PAGE_INCREMENTAL_GROWTH_TEXT,
                                                  variable=self.incremental_growth_selected,
                                                  command=self.incremental_growth_func)

        self.preferential_attachment_selected = BooleanVar()
        self.preferential_attachment = ttk.Checkbutton(self.parameters_frame,
                                                       text=GENERATE_PAGE_PREFERENTIAL_ATTACHMENT_TEXT,
                                                       variable=self.preferential_attachment_selected,
                                                       command=self.preferential_attachment_func)
        # ==============================================================================================================

        # Parameter's Labels
        self.number_of_vertices_label = ttk.Label(self.parameters_frame, font=self.button_font,
                                                  text=GENERATE_PAGE_NUMBER_OF_VERTICES_LABEL_TEXT)
        self.number_of_vertices_label.grid(row=2, column=0, pady=10, sticky="e", padx=10)

        self.graph_degree_label = ttk.Label(self.parameters_frame, font=self.button_font,
                                            text=GENERATE_PAGE_GRAPH_DEGREE_LABEL_TEXT)

        self.number_of_edges_label = ttk.Label(self.parameters_frame, font=self.button_font,
                                               text=GENERATE_PAGE_NUMBER_OF_EDGES_LABEL_TEXT)

        self.number_of_initial_nodes_label = ttk.Label(self.parameters_frame, font=self.button_font,
                                                       text=GENERATE_PAGE_NUMBER_OF_INITIAL_NODES_LABEL_TEXT)

        self.initial_connections_per_node_label = ttk.Label(self.parameters_frame, font=self.button_font,
                                                            text=GENERATE_PAGE_INITIAL_CONNECTIONS_PER_NODE_LABEL_TEXT)

        self.probability_label = ttk.Label(self.parameters_frame, font=self.button_font,
                                           text=GENERATE_PAGE_PROBABILITY_LABEL_TEXT)

        self.seed_label = ttk.Label(self.parameters_frame, font=self.button_font, text=GENERATE_PAGE_SEED_LABEL_TEXT)

        self.classpath_label = ttk.Label(self.parameters_frame, font=self.button_font,
                                         text=GENERATE_PAGE_CLASSPATH_LABEL_TEXT)

        # ==============================================================================================================

        ''' Entries for "Enter number of vertices", "Graph Degree", "Number of Edges", "Number of Initial Nodes",
            "Initial Connections per Node", "Probability", "Seed", "Classpath". '''

        self.number_of_vertices_entry_result = IntVar()
        self.number_of_vertices_entry_box = ttk.Entry(self.parameters_frame,
                                                      textvariable=self.number_of_vertices_entry_result,
                                                      width=12, validate='key', validatecommand=self.vcmd_int)
        self.number_of_vertices_entry_box.grid(row=2, column=1, sticky="w")

        self.graph_degree_result = IntVar()
        self.graph_degree_entry_box = ttk.Entry(self.parameters_frame,
                                                textvariable=self.graph_degree_result, width=12, validate='key',
                                                validatecommand=self.vcmd_int)

        self.number_of_edges_result = IntVar()
        self.number_of_edges_entry_box = ttk.Entry(self.parameters_frame,
                                                   textvariable=self.number_of_edges_result, width=12, validate='key',
                                                   validatecommand=self.vcmd_int)

        self.number_of_initial_nodes_result = IntVar()
        self.number_of_initial_nodes_entry_box = ttk.Entry(self.parameters_frame,
                                                           textvariable=self.number_of_initial_nodes_result, width=12,
                                                           validate='key', validatecommand=self.vcmd_int)

        self.initial_connections_per_node_result = IntVar()
        self.initial_connections_per_node_entry_box = ttk.Entry(self.parameters_frame,
                                                                textvariable=self.initial_connections_per_node_result,
                                                                width=12, validate='key',
                                                                validatecommand=self.vcmd_int)

        self.probability_result = StringVar()
        self.probability_result.set("0.0")
        self.probability_entry_box = ttk.Entry(self.parameters_frame,
                                               textvariable=self.probability_result, width=12, validate='key',
                                               validatecommand=self.vcmd_float)

        self.seed_result = IntVar()
        self.seed_entry_box = ttk.Entry(self.parameters_frame,
                                        textvariable=self.seed_result, width=12, validate='key',
                                        validatecommand=self.vcmd_int)

        self.classpath_result = StringVar()
        self.classpath_entry_box = ttk.Entry(self.parameters_frame,
                                             textvariable=self.classpath_result, width=30)
        # ==============================================================================================================

        # Buttons Frame
        self.buttons_frames = ttk.Frame(self)
        self.buttons_frames.grid_propagate(0)
        if platform_type == "Windows":
            self.buttons_frames.configure(height=50, width=560)
        else:
            self.buttons_frames.configure(height=50, width=670)
        self.buttons_frames.grid(row=7, column=1, padx=10)

        # Generate button
        self.generate_button = ttk.Button(self.buttons_frames, text=GENERATE_PAGE_GENERATE_BUTTON_TEXT,
                                          command=self.thread_generate)
        self.generate_button.grid(row=0, column=0, ipady=10, ipadx=10, padx=10)

        # Back button
        self.back_button = ttk.Button(self.buttons_frames, text=GENERATE_PAGE_BACK_BUTTON_TEXT,
                                      command=lambda: self.back(self.controller))
        self.back_button.grid(row=0, column=1, ipady=10, ipadx=10, padx=10)

        # Exit Button
        self.exit_button = ttk.Button(self.buttons_frames, text=GENERATE_PAGE_EXIT_BUTTON_TEXT,
                                      command=self.exit)
        self.exit_button.grid(row=0, column=2, ipady=10, ipadx=10, padx=10)

        # Cancel Button
        self.cancel_button = ttk.Button(self.buttons_frames, text=GENERATE_PAGE_CANCEL_BUTTON_TEXT,
                                        command=self.cancel)
        self.cancel_button.grid(row=0, column=3, ipady=10, ipadx=10, padx=10)
        self.cancel_button.configure(state=DISABLED)

    @staticmethod
    def validate_int(inStr, acttyp):
        if acttyp == '1':
            if not inStr.isdigit():
                return False
        return True

    @staticmethod
    def validate_float(value_if_allowed, text, acttyp):
        if acttyp == '1':
            if text in '0123456789.':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        return True

    def show_parameters(self, *args):
        self.parameters_frame.grid(row=6, column=1, padx=10)

        if self.chosen_graph.get() == GraphType.HOMOGENEOUS.value:
            self.incremental_growth_selected.set(False)
            self.preferential_attachment_selected.set(False)
            self.incremental_growth.grid_forget()
            self.preferential_attachment.grid_forget()
            self.graph_degree_label.grid_forget()
            self.number_of_edges_label.grid_forget()
            self.number_of_initial_nodes_label.grid_forget()
            self.initial_connections_per_node_label.grid_forget()
            self.probability_label.grid_forget()
            self.seed_label.grid_forget()
            self.classpath_label.grid_forget()
            self.graph_degree_entry_box.grid_forget()
            self.number_of_edges_entry_box.grid_forget()
            self.number_of_initial_nodes_entry_box.grid_forget()
            self.initial_connections_per_node_entry_box.grid_forget()
            self.probability_entry_box.grid_forget()
            self.seed_entry_box.grid_forget()
            self.classpath_entry_box.grid_forget()

            self.number_of_vertices_label.grid(row=2, column=0, pady=10, sticky="e", padx=10)
            self.number_of_vertices_entry_box.grid(row=2, column=1, sticky="w")

        elif self.chosen_graph.get() == GraphType.RANDOM_FIXED.value:
            self.incremental_growth_selected.set(False)
            self.preferential_attachment_selected.set(False)
            self.incremental_growth.grid_forget()
            self.preferential_attachment.grid_forget()
            self.number_of_vertices_entry_box.grid_forget()
            self.number_of_edges_label.grid_forget()
            self.number_of_initial_nodes_label.grid_forget()
            self.initial_connections_per_node_label.grid_forget()
            self.probability_label.grid_forget()
            self.classpath_label.grid_forget()
            self.number_of_edges_entry_box.grid_forget()
            self.number_of_initial_nodes_entry_box.grid_forget()
            self.initial_connections_per_node_entry_box.grid_forget()
            self.probability_entry_box.grid_forget()
            self.classpath_entry_box.grid_forget()

            self.number_of_vertices_label.grid(row=2, column=0, pady=10, sticky="e", padx=10)
            self.number_of_vertices_entry_box.grid(row=2, column=1, sticky="w")

            self.graph_degree_label.grid(row=3, column=0, pady=10, sticky="e", padx=10)
            self.graph_degree_entry_box.grid(row=3, column=1, sticky="w")

            self.seed_label.grid(row=8, column=0, pady=10, sticky="e", padx=10)
            self.seed_entry_box.grid(row=8, column=1, sticky="w")

        elif self.chosen_graph.get() == GraphType.SCALE_FREE.value:
            self.incremental_growth_selected.set(False)
            self.preferential_attachment_selected.set(False)
            self.number_of_vertices_entry_box.grid_forget()
            self.graph_degree_label.grid_forget()
            self.number_of_edges_label.grid_forget()
            self.number_of_initial_nodes_label.grid_forget()
            self.initial_connections_per_node_label.grid_forget()
            self.probability_label.grid_forget()
            self.classpath_label.grid_forget()
            self.graph_degree_entry_box.grid_forget()
            self.number_of_edges_entry_box.grid_forget()
            self.number_of_initial_nodes_entry_box.grid_forget()
            self.initial_connections_per_node_entry_box.grid_forget()
            self.probability_entry_box.grid_forget()
            self.classpath_entry_box.grid_forget()

            self.incremental_growth.grid(row=1, column=0, sticky="w", padx=30)
            self.preferential_attachment.grid(row=1, column=1, sticky="w", padx=30)

            self.number_of_vertices_label.grid(row=2, column=0, pady=10, sticky="e", padx=10)
            self.number_of_vertices_entry_box.grid(row=2, column=1, sticky="w")

            self.seed_label.grid(row=8, column=0, pady=10, sticky="e", padx=10)
            self.seed_entry_box.grid(row=8, column=1, sticky="w")

        elif self.chosen_graph.get() == GraphType.ER.value:
            self.incremental_growth_selected.set(False)
            self.preferential_attachment_selected.set(False)
            self.incremental_growth.grid_forget()
            self.preferential_attachment.grid_forget()
            self.graph_degree_label.grid_forget()
            self.number_of_edges_label.grid_forget()
            self.number_of_initial_nodes_label.grid_forget()
            self.initial_connections_per_node_label.grid_forget()
            self.classpath_label.grid_forget()
            self.graph_degree_entry_box.grid_forget()
            self.number_of_edges_entry_box.grid_forget()
            self.number_of_initial_nodes_entry_box.grid_forget()
            self.initial_connections_per_node_entry_box.grid_forget()
            self.classpath_entry_box.grid_forget()

            self.number_of_vertices_label.grid(row=2, column=0, pady=10, sticky="e", padx=10)
            self.probability_label.grid(row=7, column=0, pady=10, sticky="e", padx=10)
            self.seed_label.grid(row=8, column=0, sticky="e")

            self.number_of_vertices_entry_box.grid(row=2, column=1, sticky="w")
            self.probability_entry_box.grid(row=7, column=1, sticky="w")
            self.seed_entry_box.grid(row=8, column=1, sticky="w")

        elif self.chosen_graph.get() == GraphType.CUSTOM_ER.value:
            self.incremental_growth_selected.set(False)
            self.preferential_attachment_selected.set(False)
            self.incremental_growth.grid_forget()
            self.preferential_attachment.grid_forget()
            self.graph_degree_label.grid_forget()
            self.number_of_initial_nodes_label.grid_forget()
            self.initial_connections_per_node_label.grid_forget()
            self.classpath_label.grid_forget()
            self.graph_degree_entry_box.grid_forget()
            self.number_of_initial_nodes_entry_box.grid_forget()
            self.initial_connections_per_node_entry_box.grid_forget()
            self.classpath_entry_box.grid_forget()

            self.number_of_vertices_label.grid(row=2, column=0, pady=10, sticky="e", padx=10)
            self.number_of_edges_label.grid(row=4, column=0, pady=10, sticky="e", padx=10)
            self.probability_label.grid(row=7, column=0, pady=10, sticky="e", padx=10)
            self.seed_label.grid(row=8, column=0, pady=10, sticky="e", padx=10)

            self.number_of_vertices_entry_box.grid(row=2, column=1, sticky="w")
            self.number_of_edges_entry_box.grid(row=4, column=1, sticky="w")
            self.probability_entry_box.grid(row=7, column=1, sticky="w")
            self.seed_entry_box.grid(row=8, column=1, sticky="w")

        elif self.chosen_graph.get() == GraphType.CUSTOM_SCALE_FREE.value:
            self.incremental_growth_selected.set(False)
            self.preferential_attachment_selected.set(False)
            self.graph_degree_label.grid_forget()
            self.number_of_edges_label.grid_forget()
            self.number_of_initial_nodes_label.grid_forget()
            self.initial_connections_per_node_label.grid_forget()
            self.probability_label.grid_forget()
            self.classpath_label.grid_forget()
            self.graph_degree_entry_box.grid_forget()
            self.number_of_edges_entry_box.grid_forget()
            self.number_of_initial_nodes_entry_box.grid_forget()
            self.initial_connections_per_node_entry_box.grid_forget()
            self.probability_entry_box.grid_forget()
            self.classpath_entry_box.grid_forget()

            self.incremental_growth.grid(row=1, column=0, sticky="w", padx=30)
            self.preferential_attachment.grid(row=1, column=1, sticky="w", padx=30)

            self.number_of_vertices_label.grid(row=2, column=0, pady=10, sticky="e", padx=10)
            self.number_of_vertices_entry_box.grid(row=2, column=1, sticky="w")

            self.seed_label.grid(row=8, column=0, pady=10, sticky="e", padx=10)
            self.seed_entry_box.grid(row=8, column=1, sticky="w")

    @staticmethod
    def defocus(event):
        event.widget.master.focus_set()

    def handle_run_length_encoder_button(self):
        if self.adjacency_type_selected.get() == str(GraphRepresentationType.LIST):
            self.rle.configure(state=DISABLED)
            self.rle_var.set(False)
        else:
            self.rle.configure(state=NORMAL)

    def preferential_attachment_func(self):
        if self.chosen_graph.get() == GraphType.SCALE_FREE.value:
            if self.incremental_growth_selected.get() is False:
                self.number_of_initial_nodes_label.grid_forget()
                self.number_of_initial_nodes_entry_box.grid_forget()

            elif self.incremental_growth_selected.get() is True:
                self.number_of_initial_nodes_label.grid(row=5, column=0, pady=10, sticky="e", padx=10)
                self.number_of_initial_nodes_entry_box.grid(row=5, column=1, sticky="w")

        if self.chosen_graph.get() == GraphType.CUSTOM_SCALE_FREE.value:
            if self.incremental_growth_selected.get() is False:

                self.number_of_edges_label.grid(row=4, column=0, pady=10, sticky="e", padx=10)
                self.number_of_edges_entry_box.grid(row=4, column=1, sticky="w")

                self.number_of_initial_nodes_label.grid_forget()
                self.number_of_initial_nodes_entry_box.grid_forget()

                self.initial_connections_per_node_label.grid_forget()
                self.initial_connections_per_node_entry_box.grid_forget()

            elif self.incremental_growth_selected.get() is True:
                self.number_of_edges_label.grid_forget()
                self.number_of_edges_entry_box.grid_forget()

                self.number_of_initial_nodes_label.grid(row=5, column=0, pady=10, sticky="e", padx=10)
                self.number_of_initial_nodes_entry_box.grid(row=5, column=1, sticky="w")

                self.initial_connections_per_node_label.grid(row=6, column=0, pady=10, sticky="e", padx=10)
                self.initial_connections_per_node_entry_box.grid(row=6, column=1, sticky="w")

            if self.preferential_attachment_selected.get() is True and self.incremental_growth_selected.get() is False:
                self.number_of_edges_label.grid(row=4, column=0, pady=10, sticky="e", padx=10)
                self.number_of_edges_entry_box.grid(row=4, column=1, sticky="w")

            else:
                self.number_of_edges_label.grid_forget()
                self.number_of_edges_entry_box.grid_forget()

    def incremental_growth_func(self):
        if self.chosen_graph.get() == GraphType.SCALE_FREE.value:
            if self.preferential_attachment_selected.get() is True:
                self.number_of_initial_nodes_label.grid(row=5, column=0, pady=10, sticky="e", padx=10)
                self.number_of_initial_nodes_entry_box.grid(row=5, column=1, sticky="w")

            if self.incremental_growth_selected.get() is False:
                self.number_of_initial_nodes_label.grid_forget()
                self.number_of_initial_nodes_entry_box.grid_forget()

        if self.chosen_graph.get() == GraphType.CUSTOM_SCALE_FREE.value:
            if self.preferential_attachment_selected.get() is True:
                self.number_of_initial_nodes_label.grid(row=5, column=0, pady=10, sticky="e", padx=10)
                self.number_of_initial_nodes_entry_box.grid(row=5, column=1, sticky="w")

                self.initial_connections_per_node_label.grid(row=6, column=0, pady=10, sticky="e", padx=10)
                self.initial_connections_per_node_entry_box.grid(row=6, column=1, sticky="w")

                self.number_of_edges_label.grid_forget()
                self.number_of_edges_entry_box.grid_forget()

            elif self.preferential_attachment_selected.get() is False:
                self.number_of_initial_nodes_label.grid_forget()
                self.number_of_initial_nodes_entry_box.grid_forget()

                self.initial_connections_per_node_label.grid_forget()
                self.initial_connections_per_node_entry_box.grid_forget()

                self.number_of_edges_label.grid_forget()
                self.number_of_edges_entry_box.grid_forget()

            if self.incremental_growth_selected.get() is False and self.preferential_attachment_selected.get() is True:
                self.number_of_initial_nodes_label.grid_forget()
                self.number_of_initial_nodes_entry_box.grid_forget()

                self.initial_connections_per_node_label.grid_forget()
                self.initial_connections_per_node_entry_box.grid_forget()

                self.number_of_edges_label.grid(row=4, column=0, pady=10, sticky="e", padx=10)
                self.number_of_edges_entry_box.grid(row=4, column=1, sticky="w")

            elif self.incremental_growth_selected.get() is False and self.preferential_attachment_selected.get() \
                    is False:
                self.number_of_initial_nodes_label.grid_forget()
                self.number_of_initial_nodes_entry_box.grid_forget()

                self.initial_connections_per_node_label.grid_forget()
                self.initial_connections_per_node_entry_box.grid_forget()

    def back(self, controller):
        controller.show_frame(self.retrieve_frame(controller, 'MainPage'), MAIN_WINDOW_DIMENSIONS_STR)

    @staticmethod
    def exit():
        sys.exit(0)

    def thread_generate(self):
        self.thread = StoppableThread(target=self.generate, daemon=True)
        self.thread.start()

    def cancel(self):
        if self.thread.is_alive():
            self.text_area.insert(END, GENERATE_PAGE_GRAPH_CREATION_CANCEL_IN_PROGRESS_INFO)
            self.text_area.update()

            while self.thread.is_alive():
                self.thread.stop()

            self.text_area.insert(END, GENERATE_PAGE_GRAPH_CREATION_CANCEL_COMPLETED_INFO)
            self.text_area.update()

            self.cancel_button.configure(state=DISABLED)
            self.generate_button.config(state=NORMAL)
            self.back_button.configure(state=NORMAL)

    def generate(self):
        """
            Generates the graph chosen by the user and writes the adjacency matrix to file so that the
            graph can be later visualized.
        """

        global end, message4

        try:
            self.number_of_vertices_entry_result.get() == ""
        except TclError:
            self.number_of_vertices_entry_result.set(0)

        try:
            self.graph_degree_result.get() == ""
        except TclError:
            self.graph_degree_result.set(0)

        try:
            self.number_of_edges_result.get() == ""
        except TclError:
            self.number_of_edges_result.set(0)
        try:
            self.number_of_initial_nodes_result.get() == ""
        except TclError:
            self.number_of_initial_nodes_result.set(0)
        try:
            self.initial_connections_per_node_result.get() == ""
        except TclError:
            self.initial_connections_per_node_result.set(0)
        try:
            float(self.probability_result.get())
        except (TclError, ValueError):
            self.probability_result.set("0.0")
        try:
            self.seed_result.get() == ""
        except TclError:
            self.seed_result.set(0)
        try:
            self.classpath_result.get() == ""
        except TclError:
            self.classpath_result.set(0)

        self.text_area.delete('1.0', END)
        self.text_area.update()

        if self.number_of_vertices_entry_result.get() == 0:
            messagebox.showerror("Error", GENERATE_PAGE_VERTICES_NON_ZERO_ERROR)

        elif self.number_of_vertices_entry_result.get() == 1:
            messagebox.showerror("Error", GENERATE_PAGE_VERTICES_GREATER_THAN_ONE_ERROR)

        elif self.adjacency_type_selected.get() == "":
            messagebox.showerror("Error", GENERATE_PAGE_ADJACENCY_TYPE_SELECT_ERROR)

        else:
            if self.chosen_graph.get() == GraphType.SCALE_FREE.value and self.incremental_growth_selected.get() and \
                    self.preferential_attachment_selected.get():
                message1 = GENERATE_PAGE_FULL_SCALE_FREE_GENERATE_INFO

            elif self.chosen_graph.get() == GraphType.CUSTOM_SCALE_FREE.value and \
                    self.incremental_growth_selected.get() and self.preferential_attachment_selected.get():
                message1 = GENERATE_PAGE_CUSTOM_FULL_SCALE_FREE_GENERATE_INFO
            else:
                message1 = "[+] Please wait while {} graph is being generated...\n\n".format(self.chosen_graph.get())

            if self.chosen_graph.get() == GraphType.HOMOGENEOUS.value:
                self.text_area.insert(END, message1)
                self.text_area.update()

                from graphs.homogeneous import Homogeneous
                self.cancel_button.configure(state=NORMAL)
                self.generate_button.configure(state=DISABLED)
                self.back_button.configure(state=DISABLED)

                start = time()

                homogeneous_graph = Homogeneous(self.adjacency_type_selected.get())
                homogeneous_graph.create_homogeneous_graph(self.number_of_vertices_entry_result.get(),
                                                           self.thread, rle=self.rle_var.get())

                end = time() - start

                self.cancel_button.configure(state=DISABLED)
                self.generate_button.config(state=NORMAL)
                self.back_button.configure(state=NORMAL)

            elif self.chosen_graph.get() == GraphType.RANDOM_FIXED.value:
                if self.graph_degree_result.get() == 0:
                    message = GENERATE_PAGE_GRAPH_DEGREE_GREATER_THAN_ZERO_ERROR
                    messagebox.showerror("Error", message)

                else:
                    self.text_area.insert(END, message1)
                    self.text_area.update()
                    from graphs.random_fixed_graph import RandomFixed
                    self.cancel_button.configure(state=NORMAL)
                    self.generate_button.config(state=DISABLED)
                    self.back_button.configure(state=DISABLED)

                    start = time()

                    random_fixed_graph = RandomFixed(self.adjacency_type_selected.get())
                    random_fixed_graph.create_random_fixed_graph(self.number_of_vertices_entry_result.get(),
                                                                 self.graph_degree_result.get(), self.seed_result.get(),
                                                                 self.thread, rle=self.rle_var.get())

                    end = time() - start

                    self.cancel_button.configure(state=DISABLED)
                    self.generate_button.config(state=NORMAL)
                    self.back_button.configure(state=NORMAL)

            elif self.chosen_graph.get() == GraphType.SCALE_FREE.value:
                if not self.preferential_attachment_selected.get() and not self.incremental_growth_selected.get():
                    message = GENERATE_PAGE_SCALE_FREE_PROPERTIES_ERROR
                    messagebox.showerror("Error", message)
                elif not self.preferential_attachment_selected.get() and self.incremental_growth_selected.get():
                    message = GENERATE_PAGE_INCREMENTAL_GROWTH_ONLY_ERROR
                    messagebox.showerror("Error", message)
                elif self.preferential_attachment_selected.get() and not self.incremental_growth_selected.get():
                    if self.number_of_vertices_entry_result.get() in [0, 1]:
                        message = GENERATE_PAGE_SCALE_FREE_VERTICES_GREATER_THAN_ONE_ERROR
                        messagebox.showerror("Error", message)
                    else:
                        self.text_area.insert(END, message1)
                        self.text_area.update()
                        from graphs.scale_free_graph_pa import ScaleFreePA
                        self.cancel_button.configure(state=NORMAL)
                        self.generate_button.config(state=DISABLED)
                        self.back_button.configure(state=DISABLED)

                        start = time()
                        scale_free_graph_pa = ScaleFreePA(self.adjacency_type_selected.get())
                        scale_free_graph_pa.create_scale_free_graph(self.number_of_vertices_entry_result.get(),
                                                                    self.seed_result.get(), self.thread,
                                                                    rle=self.rle_var.get())
                        end = time() - start

                        self.cancel_button.configure(state=DISABLED)
                        self.generate_button.config(state=NORMAL)
                        self.back_button.configure(state=NORMAL)

                else:
                    if self.number_of_initial_nodes_result.get() == 0:
                        message = GENERATE_PAGE_SCALE_FREE_INITIAL_NODES_NON_ZERO_ERROR
                        messagebox.showerror("Error", message)
                    elif self.number_of_vertices_entry_result.get() == self.number_of_initial_nodes_result.get() == 1:
                        message = GENERATE_PAGE_SCALE_FREE_VERTICES_INITIAL_NODES_NUMBER_EQUAL_ONE_ERROR
                        messagebox.showerror("Error", message)
                    elif self.number_of_vertices_entry_result.get() < self.number_of_initial_nodes_result.get():
                        message = GENERATE_PAGE_SCALE_FREE_VERTICES_LESS_THAN_INITIAL_NODES_ERROR
                        messagebox.showerror("Error", message)
                    else:
                        self.text_area.insert(END, message1)
                        self.text_area.update()
                        from graphs.full_scale_free_graph import FullScaleFree
                        self.cancel_button.configure(state=NORMAL)
                        self.generate_button.config(state=DISABLED)

                        start = time()

                        full_scale_free_graph = FullScaleFree(self.adjacency_type_selected.get())
                        full_scale_free_graph.create_full_scale_free_graph(self.number_of_vertices_entry_result.get(),
                                                                           self.number_of_initial_nodes_result.get(),
                                                                           self.seed_result.get(), self.thread,
                                                                           rle=self.rle_var.get())

                        end = time() - start

                        self.cancel_button.configure(state=DISABLED)
                        self.generate_button.config(state=NORMAL)

            elif self.chosen_graph.get() == GraphType.ER.value:
                if float(self.probability_result.get()) == 0.0:
                    message = GENERATE_PAGE_ER_PROBABILITY_GREATER_THAN_ZERO_ERROR
                    messagebox.showerror("Error", message)

                else:
                    self.text_area.insert(END, message1)
                    self.text_area.update()
                    from graphs.er_graph import ErdosRenyi
                    self.cancel_button.configure(state=NORMAL)
                    self.generate_button.config(state=DISABLED)
                    self.back_button.configure(state=DISABLED)

                    start = time()

                    erdos_renyi_graph = ErdosRenyi(self.adjacency_type_selected.get())
                    erdos_renyi_graph.create_er_graph(self.number_of_vertices_entry_result.get(),
                                                      float(self.probability_result.get()), self.seed_result.get(),
                                                      self.thread,
                                                      rle=self.rle_var.get())

                    end = time() - start

                    self.cancel_button.configure(state=DISABLED)
                    self.generate_button.config(state=NORMAL)
                    self.back_button.configure(state=NORMAL)

            elif self.chosen_graph.get() == GraphType.CUSTOM_ER.value:
                if self.number_of_edges_result.get() == 0:
                    message = GENERATE_PAGE_CUSTOM_ER_EDGES_GREATER_THAN_ZERO_ERROR
                    messagebox.showerror("Error", message)
                    sys.exit(0)

                elif float(self.probability_result.get()) == 0.0:
                    message = GENERATE_PAGE_CUSTOM_ER_PROBABILITY_GREATER_THAN_ZERO_ERROR
                    messagebox.showerror("Error", message)
                    sys.exit(0)

                elif self.number_of_edges_result.get() > (pow(self.number_of_vertices_entry_result.get(), 2)
                                                          - self.number_of_vertices_entry_result.get()) // 2:

                    message1 = GENERATE_PAGE_CUSTOM_ER_INVALID_NUMBER_OF_EDGES_ERROR

                    self.text_area.insert(END, message1)
                    self.text_area.update()

                    self.cancel()
                    sys.exit(0)

                elif self.number_of_edges_result.get() == (pow(self.number_of_vertices_entry_result.get(), 2)
                                                           - self.number_of_vertices_entry_result.get()) // 2:

                    message4 = GENERATE_PAGE_CUSTOM_ER_HOMOGENEOUS_WARNING

                    try:
                        self.text_area.insert(END, message4)
                        self.text_area.update()

                    except (UnboundLocalError, NameError):
                        pass
                    self.text_area.update()

                self.text_area.insert(END, message1)
                self.text_area.update()

                from graphs.er_graph import ErdosRenyi
                self.cancel_button.configure(state=NORMAL)
                self.generate_button.config(state=DISABLED)
                self.back_button.configure(state=DISABLED)

                start = time()

                erdos_renyi_graph = ErdosRenyi(self.adjacency_type_selected.get())
                erdos_renyi_graph.create_custom_er_graph(self.number_of_vertices_entry_result.get(),
                                                         self.number_of_edges_result.get(),
                                                         float(self.probability_result.get()),
                                                         self.seed_result.get(),
                                                         self.thread,
                                                         rle=self.rle_var.get())

                end = time() - start

                self.cancel_button.configure(state=DISABLED)
                self.generate_button.config(state=NORMAL)
                self.back_button.configure(state=NORMAL)

            elif self.chosen_graph.get() == GraphType.CUSTOM_SCALE_FREE.value:
                if not self.preferential_attachment_selected.get() and not self.incremental_growth_selected.get():
                    message = GENERATE_PAGE_CUSTOM_SCALE_FREE_PROPERTIES_ERROR
                    messagebox.showerror("Error", message)

                elif not self.preferential_attachment_selected.get() and self.incremental_growth_selected.get():
                    message = GENERATE_PAGE_INCREMENTAL_GROWTH_ONLY_ERROR
                    messagebox.showerror("Error", message)

                elif self.preferential_attachment_selected.get() and not self.incremental_growth_selected.get():

                    if self.number_of_vertices_entry_result.get() in [0, 1]:
                        message = GENERATE_PAGE_CUSTOM_SCALE_FREE_VERTICES_GREATER_THAN_ONE_ERROR
                        messagebox.showerror("Error", message)

                    elif self.number_of_edges_result.get() == 0:
                        message = GENERATE_PAGE_CUSTOM_SCALE_FREE_MAX_NUMBER_OF_EDGES_GREATER_THAN_ZERO_ERROR
                        messagebox.showerror("Error", message)

                    elif self.number_of_edges_result.get() > self.number_of_vertices_entry_result.get() \
                            * (self.number_of_vertices_entry_result.get() - 1) / 2:
                        message = GENERATE_PAGE_CUSTOM_SCALE_FREE_INVALID_NUMBER_OF_EDGES_ERROR
                        messagebox.showerror("Error", message)

                    else:

                        self.text_area.insert(END, message1)
                        self.text_area.update()
                        from graphs.scale_free_graph_pa import ScaleFreePA
                        self.cancel_button.configure(state=NORMAL)
                        self.generate_button.config(state=DISABLED)
                        self.back_button.configure(state=DISABLED)

                        start = time()

                        scale_free_graph_pa = ScaleFreePA(self.adjacency_type_selected.get())
                        scale_free_graph_pa.create_custom_scale_free_graph(self.number_of_vertices_entry_result.get(),
                                                                           self.number_of_edges_result.get(),
                                                                           self.seed_result.get(), self.thread,
                                                                           rle=self.rle_var.get())

                        end = time() - start

                        self.cancel_button.configure(state=DISABLED)
                        self.generate_button.config(state=NORMAL)
                        self.back_button.configure(state=NORMAL)

                else:

                    if self.number_of_initial_nodes_result.get() == 0:
                        message = GENERATE_PAGE_CUSTOM_SCALE_FREE_INITIAL_NODES_NON_ZERO_ERROR
                        messagebox.showerror("Error", message)

                    elif self.initial_connections_per_node_result.get() == 0:
                        message = GENERATE_PAGE_CUSTOM_SCALE_FREE_INITIAL_CONNECTIONS_PER_NODE_NON_ZERO_ERROR
                        messagebox.showerror("Error", message)

                    elif self.number_of_vertices_entry_result.get() == self.number_of_initial_nodes_result.get() == 1:
                        message = GENERATE_PAGE_CUSTOM_SCALE_FREE_VERTICES_INITIAL_NODES_NUMBER_EQUAL_ONE_ERROR
                        messagebox.showerror("Error", message)

                    elif self.number_of_vertices_entry_result.get() < self.number_of_initial_nodes_result.get():
                        message = GENERATE_PAGE_CUSTOM_SCALE_FREE_VERTICES_LESS_THAN_INITIAL_NODES_ERROR
                        messagebox.showerror("Error", message)

                    elif self.initial_connections_per_node_result.get() > \
                            (pow(self.number_of_initial_nodes_result.get(), 2)
                             - self.number_of_initial_nodes_result.get()) // 2:

                        message = GENERATE_PAGE_CUSTOM_SCALE_FREE_INVALID_NUMBER_OF_EDGES_ERROR
                        messagebox.showerror("Error", message)

                    else:
                        self.text_area.insert(END, message1)
                        self.text_area.update()
                        from graphs.full_scale_free_graph import FullScaleFree
                        self.cancel_button.configure(state=NORMAL)
                        self.generate_button.config(state=DISABLED)

                        start = time()

                        full_scale_free_graph = FullScaleFree(self.adjacency_type_selected.get())
                        full_scale_free_graph.create_full_scale_free_graph(
                            self.number_of_vertices_entry_result.get(),
                            self.number_of_initial_nodes_result.get(),
                            self.seed_result.get(),
                            self.thread,
                            self.initial_connections_per_node_result.get(),
                            rle=self.rle_var.get()
                        )  # --> Custom Full Scale-Free Graph.

                        end = time() - start

                        self.cancel_button.configure(state=DISABLED)
                        self.generate_button.config(state=NORMAL)

            try:

                if self.chosen_graph.get() == GraphType.RANDOM_FIXED.value and self.graph_degree_result.get() == 0:
                    pass

                elif ((self.chosen_graph.get() == GraphType.SCALE_FREE.value
                       and not self.incremental_growth_selected.get()
                       and not self.preferential_attachment_selected.get())

                      or (self.incremental_growth_selected.get()
                          and not self.preferential_attachment_selected.get())

                      or (self.chosen_graph.get() == GraphType.SCALE_FREE.value
                          and self.incremental_growth_selected.get()
                          and self.preferential_attachment_selected.get()
                          and self.number_of_initial_nodes_result.get() == 0)

                      or (self.number_of_vertices_entry_result.get() == self.number_of_initial_nodes_result.get() == 1)

                      or (self.number_of_vertices_entry_result.get() < self.number_of_initial_nodes_result.get())

                      or (self.chosen_graph.get() == GraphType.SCALE_FREE.value and
                          self.number_of_vertices_entry_result.get() in [0, 1])):

                    pass

                elif self.chosen_graph.get() == GraphType.CUSTOM_ER.value and \
                        float(self.probability_result.get()) == 0.0:
                    pass

                elif ((self.chosen_graph.get() == GraphType.CUSTOM_ER.value
                       and (float(self.probability_result.get()) == 0.0))
                      or (self.chosen_graph.get() == GraphType.CUSTOM_ER.value
                          and self.number_of_edges_result.get() == 0)
                      or (self.chosen_graph.get() == GraphType.CUSTOM_ER.value
                          and self.number_of_edges_result.get() >
                          (pow(self.number_of_vertices_entry_result.get(), 2)
                           - self.number_of_vertices_entry_result.get()) // 2)):
                    pass

                elif ((self.chosen_graph.get() == GraphType.CUSTOM_SCALE_FREE.value
                       and not self.incremental_growth_selected.get()
                       and not self.preferential_attachment_selected.get())

                      or (self.chosen_graph.get() == GraphType.CUSTOM_SCALE_FREE.value
                          and self.preferential_attachment_selected.get()
                          and not self.incremental_growth_selected.get()
                          and self.number_of_edges_result.get() == 0)

                      or (self.chosen_graph.get() == GraphType.CUSTOM_SCALE_FREE.value
                          and self.incremental_growth_selected.get()
                          and (self.number_of_initial_nodes_result.get() == 0
                               or self.initial_connections_per_node_result.get() == 0))):

                    pass

                else:
                    message3 = "[+] Elapsed time: {:>.2f} sec\n".format(end)
                    self.text_area.insert(END, GENERATE_PAGE_GRAPH_CREATION_SUCCESS)
                    self.text_area.insert(END, message3)
                    self.text_area.update()

            except NameError:
                pass

    def refresh_widget_style(self, style):
        super(GraphGeneratePage, self).refresh_widget_style(style=style)
        self.text_area.configure(bg=style['scrollable_frame']['bg'], font=(
            style['scrollable_frame']['font']['family'],
            style['scrollable_frame']['font']['size'],
            style['scrollable_frame']['font']['style']
        ))
