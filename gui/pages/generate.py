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

from time import time
from gui.pages.page import *
from graphs.graph import GraphRepresentationType


class GraphGeneratePage(Page):

    def __init__(self, parent, controller):
        super(GraphGeneratePage, self).__init__(parent)

        self.parent = parent
        self.controller = controller

        # MainPage Frame configuration
        self.configure(bg="azure3")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(20, weight=1)
        # ================================

        # Thread define
        self.thread = StoppableThread(target=self.generate)
        # ================================

        # Button font
        self.button_font = ("Dialog", 9, "bold italic")
        # ================================

        # Validators
        self.vcmd_int = (self.master.register(self.validate_int),
                         '%P', '%d')
        self.vcmd_float = (self.master.register(self.validate_float),
                           '%P', '%S', '%d')
        # ================================

        # Type of graph being generated
        self.graph_types = ['', 'Homogeneous', 'Random Fixed Graph', 'Scale-Free', 'ER Random Graph',
                            'Custom ER Random Graph', 'Custom Scale-Free Graph']
        # ================================

        self.rle_var = BooleanVar(False)
        self.rle = ttk.Checkbutton(self, text="Run Length Encoder", variable=self.rle_var)
        # self.rle.grid(row=1, column=2, sticky="w")

        # Main Label
        self.main_label = Label(self, bg="azure3", text="Generate a graph\n",
                                font=("Arial", 20, "bold"))
        self.main_label.grid(row=2, column=1)
        # ================================

        # Text Area Frame
        # create a Frame for the Text and Scrollbar
        self.my_frame_inner = ttk.Frame(self)
        # create a Scrollbar and associate it with txt
        self.my_scroll = Scrollbar(self.my_frame_inner, orient='vertical')
        # create a Text widget
        self.text_area = Text(self.my_frame_inner, background="lavender blush", yscrollcommand=self.my_scroll.set,
                              width=35,
                              height=23, relief=FLAT, borderwidth=5)
        self.text_area.bind("<FocusIn>", self.defocus)
        self.text_area.config(font=("consolas", 11), undo=True, wrap='word')
        self.my_scroll.config(command=self.text_area.yview)

        self.my_frame_inner.grid(row=2, column=2, rowspan=13, columnspan=2, sticky='nesw')
        self.text_area.grid(row=2, column=2, rowspan=13)
        self.my_scroll.grid(row=2, column=3, rowspan=13, columnspan=2, sticky='nesw')
        # ================================

        # Type Label
        self.main_label = Label(self, bg="azure3", text="Select type of graph:\n",
                                font=("Arial", 10, "bold"))
        self.main_label.grid(row=3, column=1)
        # ================================

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
        self.matrix = ttk.Radiobutton(self.parameters_frame, text="Adjacency Matrix",
                                      value=GraphRepresentationType.MATRIX,
                                      variable=self.adjacency_type_selected,
                                      command=self.handle_run_length_encoder_button)
        self.matrix.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        self.list = ttk.Radiobutton(self.parameters_frame, text="Adjacency List",
                                    value=GraphRepresentationType.LIST,
                                    variable=self.adjacency_type_selected,
                                    command=self.handle_run_length_encoder_button)
        self.list.grid(row=0, column=1, padx=30, pady=10, sticky="w")

        self.incremental_growth_selected = BooleanVar()
        self.incremental_growth = ttk.Checkbutton(self.parameters_frame, text="Incremental Growth",
                                                  variable=self.incremental_growth_selected,
                                                  command=self.incremental_growth_func)

        self.preferential_attachment_selected = BooleanVar()
        self.preferential_attachment = ttk.Checkbutton(self.parameters_frame, text="Preferential Attachment",
                                                       variable=self.preferential_attachment_selected,
                                                       command=self.preferential_attachment_func)
        # ==============================================================================================================

        # Parameter's Labels

        self.number_of_vertices_label = Label(self.parameters_frame, bg="azure3", text="Number of Vertices:",
                                              font=self.button_font)
        self.number_of_vertices_label.grid(row=2, column=0, pady=10, sticky="e", padx=10)

        self.graph_degree_label = Label(self.parameters_frame, bg="azure3", text="Graph Degree:", font=self.button_font)

        self.number_of_edges_label = Label(self.parameters_frame, bg="azure3", text="Number of Edges:",
                                           font=self.button_font)

        self.number_of_initial_nodes_label = Label(self.parameters_frame, bg="azure3", text="Number of Initial Nodes:",
                                                   font=self.button_font)

        self.initial_connections_per_node_label = Label(self.parameters_frame, bg="azure3",
                                                        text="Initial Connections per Node:", font=self.button_font)

        self.probability_label = Label(self.parameters_frame, bg="azure3", text="Probability:", font=self.button_font)

        self.seed_label = Label(self.parameters_frame, bg="azure3", text="Seed:", font=self.button_font)

        self.classpath_label = Label(self.parameters_frame, bg="azure3", text="Classpath:", font=self.button_font)

        # ==============================================================================================================

        ''' Entries for "Enter number of vertices", "Graph Degree", "Number of Edges", "Number of Initial Nodes",
            "Initial Connections per Node", "Probability", "Seed", "Classpath". '''

        self.number_of_vertices_entry_result = IntVar()
        self.number_of_vertices_entry_box = Entry(self.parameters_frame,
                                                  textvariable=self.number_of_vertices_entry_result,
                                                  width=12, validate='key', validatecommand=self.vcmd_int)
        self.number_of_vertices_entry_box.grid(row=2, column=1, sticky="w")

        self.graph_degree_result = IntVar()
        self.graph_degree_entry_box = Entry(self.parameters_frame, disabledbackground="grey50",
                                            disabledforeground="grey50",
                                            textvariable=self.graph_degree_result, width=12, validate='key',
                                            validatecommand=self.vcmd_int)

        self.number_of_edges_result = IntVar()
        self.number_of_edges_entry_box = Entry(self.parameters_frame, disabledbackground="grey50",
                                               disabledforeground="grey50",
                                               textvariable=self.number_of_edges_result, width=12, validate='key',
                                               validatecommand=self.vcmd_int)

        self.number_of_initial_nodes_result = IntVar()
        self.number_of_initial_nodes_entry_box = Entry(self.parameters_frame, disabledbackground="grey50",
                                                       disabledforeground="grey50",
                                                       textvariable=self.number_of_initial_nodes_result, width=12,
                                                       validate='key', validatecommand=self.vcmd_int)

        self.initial_connections_per_node_result = IntVar()
        self.initial_connections_per_node_entry_box = Entry(self.parameters_frame, disabledbackground="grey50",
                                                            disabledforeground="grey50",
                                                            textvariable=self.initial_connections_per_node_result,
                                                            width=12, validate='key',
                                                            validatecommand=self.vcmd_int)

        self.probability_result = StringVar()
        self.probability_result.set("0.0")
        self.probability_entry_box = Entry(self.parameters_frame, disabledbackground="grey50",
                                           disabledforeground="grey50",
                                           textvariable=self.probability_result, width=12, validate='key',
                                           validatecommand=self.vcmd_float)

        self.seed_result = IntVar()
        self.seed_entry_box = Entry(self.parameters_frame, disabledbackground="grey50", disabledforeground="grey50",
                                    textvariable=self.seed_result, width=12, validate='key',
                                    validatecommand=self.vcmd_int)

        self.classpath_result = StringVar()
        self.classpath_entry_box = Entry(self.parameters_frame, disabledbackground="grey50",
                                         disabledforeground="grey50",
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
        # ================================

        # ================================

        # Generate button
        self.generate_button = ttk.Button(self.buttons_frames, text="GENERATE", command=self.thread_generate)
        self.generate_button.grid(row=0, column=0, ipady=10, ipadx=10, padx=10)
        # ================================

        # Back button
        self.back_button = ttk.Button(self.buttons_frames, text="BACK", command=lambda: self.back(self.controller))
        self.back_button.grid(row=0, column=1, ipady=10, ipadx=10, padx=10)
        # ================================

        # Exit Button
        self.exit_button = ttk.Button(self.buttons_frames, text="EXIT", command=self.exit)
        self.exit_button.grid(row=0, column=2, ipady=10, ipadx=10, padx=10)
        # ============================================

        # Cancel Button
        self.cancel_button = ttk.Button(self.buttons_frames, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=0, column=3, ipady=10, ipadx=10, padx=10)
        self.cancel_button.configure(state=DISABLED)
        # ============================================

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

        if self.chosen_graph.get() == 'Homogeneous':

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

        elif self.chosen_graph.get() == 'Random Fixed Graph':

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

        elif self.chosen_graph.get() == 'Scale-Free':

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

        elif self.chosen_graph.get() == 'ER Random Graph':
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

        elif self.chosen_graph.get() == 'Custom ER Random Graph':
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

        elif self.chosen_graph.get() == 'Custom Scale-Free Graph':
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
        if self.chosen_graph.get() == 'Scale-Free':
            if self.incremental_growth_selected.get() is False:
                self.number_of_initial_nodes_label.grid_forget()
                self.number_of_initial_nodes_entry_box.grid_forget()

            elif self.incremental_growth_selected.get() is True:
                self.number_of_initial_nodes_label.grid(row=5, column=0, pady=10, sticky="e", padx=10)
                self.number_of_initial_nodes_entry_box.grid(row=5, column=1, sticky="w")

        if self.chosen_graph.get() == 'Custom Scale-Free Graph':
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
        if self.chosen_graph.get() == 'Scale-Free':
            if self.preferential_attachment_selected.get() is True:
                self.number_of_initial_nodes_label.grid(row=5, column=0, pady=10, sticky="e", padx=10)
                self.number_of_initial_nodes_entry_box.grid(row=5, column=1, sticky="w")

            if self.incremental_growth_selected.get() is False:
                self.number_of_initial_nodes_label.grid_forget()
                self.number_of_initial_nodes_entry_box.grid_forget()

        if self.chosen_graph.get() == 'Custom Scale-Free Graph':
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
        controller.show_frame(self.retrieve_frame(controller, 'MainPage'), transform)

    @staticmethod
    def exit():
        sys.exit(0)

    def thread_generate(self):
        self.thread = StoppableThread(target=self.generate, daemon=True)
        self.thread.start()

    def cancel(self):
        if self.thread.is_alive():
            message = "[+] Terminating graph creation...\n"
            self.text_area.insert(END, message)
            self.text_area.update()

            while self.thread.is_alive():
                self.thread.stop()

            message = "[!] Graph creation was canceled!\n"
            self.text_area.insert(END, message)
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
            message = "- Number of vertices must be non zero!"
            messagebox.showerror("Error", message)

        elif self.number_of_vertices_entry_result.get() == 1:
            message = "- Number of vertices must be greater than one!"
            messagebox.showerror("Error", message)

        elif self.adjacency_type_selected.get() == "":
            message = "- You must select either adjacency matrix or adjacency list!"
            messagebox.showerror("Error", message)

        else:
            if self.chosen_graph.get() == 'Scale-Free' and self.incremental_growth_selected.get() and \
                    self.preferential_attachment_selected.get():

                message1 = "[+] Please wait while Full Scale-Free graph is being generated...\n\n"

            elif self.chosen_graph.get() == 'Custom Scale-Free Graph' and self.incremental_growth_selected.get() and \
                    self.preferential_attachment_selected.get():

                message1 = "[+] Please wait while Custom Full Scale-Free graph is being generated...\n\n"

            else:
                message1 = "[+] Please wait while {} graph is being generated...\n\n".format(self.chosen_graph.get())

            message2 = "[+] The graph was generated successfully!\n\n"

            if self.chosen_graph.get() == 'Homogeneous':
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

            elif self.chosen_graph.get() == 'Random Fixed Graph':
                if self.graph_degree_result.get() == 0:
                    message = "- Graph degree must be greater than 0\n"
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

            elif self.chosen_graph.get() == 'Scale-Free':
                if not self.preferential_attachment_selected.get() and not self.incremental_growth_selected.get():
                    message = "- You must either create a Scale-Free graph with preferential attachment or " \
                              "a Scale-Free graph with incremental growth and preferential attachment!"
                    messagebox.showerror("Error", message)

                elif not self.preferential_attachment_selected.get() and self.incremental_growth_selected.get():
                    message = "- Incremental growth cannot be solely selected!"
                    messagebox.showerror("Error", message)

                elif self.preferential_attachment_selected.get() and not self.incremental_growth_selected.get():

                    if self.number_of_vertices_entry_result.get() in [0, 1]:
                        message = "- Number of vertices must be greater than 1 in order\n" \
                                  "to generate a Scale-Free Graph."
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
                        message = "- Number of initial nodes must be non zero!"
                        messagebox.showerror("Error", message)

                    elif self.number_of_vertices_entry_result.get() == self.number_of_initial_nodes_result.get() == 1:
                        message = "- Number of vertices and number of initial node cannot be simultaneously equal to 1."
                        messagebox.showerror("Error", message)

                    elif self.number_of_vertices_entry_result.get() < self.number_of_initial_nodes_result.get():
                        message = "- Number of vertices must not be less than the number of initial nodes."
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

            elif self.chosen_graph.get() == 'ER Random Graph':
                if float(self.probability_result.get()) == 0.0:
                    message = "- Probability must be greater than 0.0!"
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

            elif self.chosen_graph.get() == 'Custom ER Random Graph':
                if self.number_of_edges_result.get() == 0:
                    message = "- Number of edges must be greater than 0."
                    messagebox.showerror("Error", message)
                    sys.exit(0)

                elif float(self.probability_result.get()) == 0.0:
                    message = "- Probability must be greater than 0.0!"
                    messagebox.showerror("Error", message)
                    sys.exit(0)

                elif self.number_of_edges_result.get() > (pow(self.number_of_vertices_entry_result.get(), 2)
                                                          - self.number_of_vertices_entry_result.get()) // 2:

                    message1 = "[-] Critical error: Cannot have that much edges with this number of nodes.\n"

                    self.text_area.insert(END, message1)
                    self.text_area.update()

                    self.cancel()
                    sys.exit(0)

                elif self.number_of_edges_result.get() == (pow(self.number_of_vertices_entry_result.get(), 2)
                                                           - self.number_of_vertices_entry_result.get()) // 2:

                    message4 = "[!] Warning: You will end up with a Homogeneous graph!\n\n"

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

            elif self.chosen_graph.get() == 'Custom Scale-Free Graph':
                if not self.preferential_attachment_selected.get() and not self.incremental_growth_selected.get():
                    message = "- You must either create a Custom Scale-Free graph with preferential attachment or " \
                              "a Custom Scale-Free graph with incremental growth and preferential attachment!"
                    messagebox.showerror("Error", message)

                elif not self.preferential_attachment_selected.get() and self.incremental_growth_selected.get():
                    message = "- Incremental growth cannot be solely selected!"
                    messagebox.showerror("Error", message)

                elif self.preferential_attachment_selected.get() and not self.incremental_growth_selected.get():

                    if self.number_of_vertices_entry_result.get() in [0, 1]:
                        message = "- Number of vertices must be greater than 1 in order\n" \
                                  "to generate a Custom Scale-Free Graph."
                        messagebox.showerror("Error", message)

                    elif self.number_of_edges_result.get() == 0:
                        message = "- Number of maximum edges that the graph can have" \
                                  " must be greater than 0."
                        messagebox.showerror("Error", message)

                    elif self.number_of_edges_result.get() > self.number_of_vertices_entry_result.get() \
                            * (self.number_of_vertices_entry_result.get() - 1) / 2:
                        message = "- Cannot have that much edges with this number of Vertices."
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
                        message = "- Number of initial nodes must be non zero!"
                        messagebox.showerror("Error", message)

                    elif self.initial_connections_per_node_result.get() == 0:
                        message = "- Number of initial connections per node must be non zero!"
                        messagebox.showerror("Error", message)

                    elif self.number_of_vertices_entry_result.get() == self.number_of_initial_nodes_result.get() == 1:
                        message = "- Number of vertices and number of initial node cannot be simultaneously equal to 1."
                        messagebox.showerror("Error", message)

                    elif self.number_of_vertices_entry_result.get() < self.number_of_initial_nodes_result.get():
                        message = "- Number of vertices must not be less than the number of initial nodes."
                        messagebox.showerror("Error", message)

                    elif self.initial_connections_per_node_result.get() > \
                            (pow(self.number_of_initial_nodes_result.get(), 2)
                             - self.number_of_initial_nodes_result.get()) // 2:

                        message = "- Cannot have that much edges with this number of initial nodes."
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

                if self.chosen_graph.get() == 'Random Fixed Graph' and self.graph_degree_result.get() == 0:
                    pass

                elif ((self.chosen_graph.get() == 'Scale-Free'
                       and not self.incremental_growth_selected.get()
                       and not self.preferential_attachment_selected.get())

                      or (self.incremental_growth_selected.get()
                          and not self.preferential_attachment_selected.get())

                      or (self.chosen_graph.get() == 'Scale-Free'
                          and self.incremental_growth_selected.get()
                          and self.preferential_attachment_selected.get()
                          and self.number_of_initial_nodes_result.get() == 0)

                      or (self.number_of_vertices_entry_result.get() == self.number_of_initial_nodes_result.get() == 1)

                      or (self.number_of_vertices_entry_result.get() < self.number_of_initial_nodes_result.get())

                      or (self.chosen_graph.get() == 'Scale-Free' and self.number_of_vertices_entry_result.get()
                          in [0, 1])):

                    pass

                elif self.chosen_graph.get() == 'ER Random Graph' and float(self.probability_result.get()) == 0.0:
                    pass

                elif ((self.chosen_graph.get() == 'Custom ER Random Graph'
                       and (float(self.probability_result.get()) == 0.0))
                      or (self.chosen_graph.get() == 'Custom ER Random Graph'
                          and self.number_of_edges_result.get() == 0)
                      or (self.chosen_graph.get() == 'Custom ER Random Graph'
                          and self.number_of_edges_result.get() >
                          (pow(self.number_of_vertices_entry_result.get(), 2)
                           - self.number_of_vertices_entry_result.get()) // 2)):
                    pass

                elif ((self.chosen_graph.get() == 'Custom Scale-Free Graph'
                       and not self.incremental_growth_selected.get()
                       and not self.preferential_attachment_selected.get())

                      or (self.chosen_graph.get() == 'Custom Scale-Free Graph'
                          and self.preferential_attachment_selected.get()
                          and not self.incremental_growth_selected.get()
                          and self.number_of_edges_result.get() == 0)

                      or (self.chosen_graph.get() == 'Custom Scale-Free Graph'
                          and self.incremental_growth_selected.get()
                          and (self.number_of_initial_nodes_result.get() == 0
                               or self.initial_connections_per_node_result.get() == 0))):

                    pass

                else:
                    message3 = "[+] Elapsed time: {:>.2f} sec\n".format(end)
                    self.text_area.insert(END, message2)
                    self.text_area.insert(END, message3)
                    self.text_area.update()

            except NameError:
                pass
