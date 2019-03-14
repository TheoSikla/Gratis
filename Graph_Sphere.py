from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from os_recon.define_os import transform, platform_type
from Support_Folders.multithreading import StoppableThread

from Analyze.Analyze import *
from Analyze.Geodesic_Paths import find_geodesics
from Analyze.Centrality import closeness_centrality
from Analyze.Paths import find_all_paths, find_shortest_paths
from Analyze.Betweenness_Centrality import betweenness_centrality

from sqlite3_db.Database import *
import webbrowser

from time import time


class App(Tk):

    def __init__(self, *args, **kwargs):
        # Root initiate
        Tk.__init__(self)
        # ================================

        self.center()

        # Create required directories
        self.create_directories()
        # ================================

        # Root - Frame Configuration
        # self.title("Graph Sphere")
        self.config(bg="azure3")
        self['padx'] = 20
        self['pady'] = 20
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # =================================

        # ttk style configuration
        self.button_font = ("Dialog", 9, "bold italic")
        self.style = ttk.Style()
        self.style.configure('TButton', background='seashell3', foreground='black', relief='flat', width=15)
        self.style.configure('TFrame', background='azure3')
        self.style.configure('TRadiobutton', background='azure3', foreground='black', relief='flat',
                             font=self.button_font)
        self.style.configure('TCheckbutton', background='azure3', foreground='black', relief='flat',
                             font=self.button_font)
        # ================================

        # Main container for Frames
        container = ttk.Frame(self)
        container.grid(column=0, row=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # =================================

        # List with all the Frames of the application
        self.frames = {}
        # =================================

        # Load all the Frames
        for F in (MainPage, GraphGeneratePage, GraphAnalyzePage, GraphVisualizePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        # =================================

        # Initiate the MainFrame
        # self.show_frame(MainPage, transform)
        self.show_frame(GraphAnalyzePage, transform)
        # =================================

    def show_frame(self, cont, size):
        self.geometry(size)
        self.update()
        self.update_idletasks()
        self.center()
        frame = self.frames[cont]
        frame.tkraise()

    def center(self):

        size_x = self.winfo_width()

        size_y = self.winfo_height()

        w = self.winfo_screenwidth()

        h = self.winfo_screenheight()

        size = (size_x, size_y)
        x = w / 2 - size[0] / 2

        y = h / 2 - size[1] / 2

        self.geometry("%dx%d+%d+%d" % (size + (x, y)))

    @staticmethod
    def create_directories():
        # Create the output folder if it doesn't exist.
        if not os.path.exists("Output_Files"):
            os.makedirs("Output_Files")
        # ================================


class MainPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # MainPage Frame configuration
        self.configure(bg="azure3")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(7, weight=1)
        # ================================

        # Button configuration variables
        self.ipady = 10
        # ================================

        # Main Label
        self.main_label = Label(self, bg="azure3", text="Welcome to Graph Sphere\n",
                                font=("Arial", 20, "bold"))
        # self.main_label.grid(row=1, column=1, columnspan=3)
        # ================================

        # Generate area button
        self.generate_area = ttk.Button(self, text="Generate Graph",
                                        command=lambda: controller.show_frame(GraphGeneratePage, transform))
        self.generate_area.grid(row=2, column=1, ipady=self.ipady, padx=30)
        # ================================

        # Analyze area button
        self.analyze_area = ttk.Button(self, text="Analyze Graph",
                                       command=lambda: controller.show_frame(GraphAnalyzePage, transform))
        self.analyze_area.grid(row=2, column=2, ipady=self.ipady, padx=30)
        # ================================

        # Visualize area button
        self.visualise_area = ttk.Button(self, text="Visualize Graph",
                                         command=lambda: controller.show_frame(GraphVisualizePage, transform))
        self.visualise_area.grid(row=2, column=3, ipady=self.ipady, padx=30)
        # ================================

        # Exit button
        self.exit = ttk.Button(self, text="Exit", command=lambda: sys.exit(0))
        self.exit.grid(row=3, column=3, ipady=self.ipady, pady=20)
        # ================================


class GraphGeneratePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

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

        # Main Label
        self.main_label = Label(self, bg="azure3", text="Generate a graph\n",
                                font=("Arial", 20, "bold"))
        self.main_label.grid(row=1, column=1)
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

        self.my_frame_inner.grid(row=1, column=2, rowspan=13, columnspan=2, sticky='nesw')
        self.text_area.grid(row=1, column=2, rowspan=13)
        self.my_scroll.grid(row=1, column=3, rowspan=13, columnspan=2, sticky='nesw')
        # ================================

        # Type Label
        self.main_label = Label(self, bg="azure3", text="Select type of graph:\n",
                                font=("Arial", 10, "bold"))
        self.main_label.grid(row=2, column=1)
        # ================================

        self.chosen_graph = StringVar()
        self.chosen_graph.set(self.graph_types[1])

        self.graphs = ttk.OptionMenu(self, self.chosen_graph, *self.graph_types, command=self.show_parameters)
        self.graphs.grid(row=3, column=1, pady=10)

        # Parameter's Frame
        self.parameters_frame = ttk.Frame(self)
        self.parameters_frame.grid_propagate(0)
        self.parameters_frame.configure(height=230, width=400)
        self.parameters_frame.grid(row=6, column=1)

        # Incremental Growth, Preferential Attachment Checkbuttons for Scale-free Radiobutton

        self.adjacency_type_selected = StringVar()
        self.matrix = ttk.Radiobutton(self.parameters_frame, text="Adjacency Matrix", value="Matrix",
                                      variable=self.adjacency_type_selected)
        self.matrix.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        self.list = ttk.Radiobutton(self.parameters_frame, text="Adjacency List", value="List",
                                    variable=self.adjacency_type_selected)
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
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid_propagate(0)
        if platform_type == "Windows":
            self.buttons_frame.configure(height=50, width=560)
        else:
            self.buttons_frame.configure(height=50, width=670)
        self.buttons_frame.grid(row=7, column=1, padx=10)
        # ================================

        # ================================

        # Generate button
        self.generate_button = ttk.Button(self.buttons_frame, text="GENERATE", command=self.thread_generate)
        self.generate_button.grid(row=0, column=0, ipady=10, ipadx=10, padx=10)
        # ================================

        # Back button
        self.back_button = ttk.Button(self.buttons_frame, text="BACK", command=lambda: self.back(controller))
        self.back_button.grid(row=0, column=1, ipady=10, ipadx=10, padx=10)
        # ================================

        # Exit Button
        self.exit_button = ttk.Button(self.buttons_frame, text="EXIT", command=self.exit)
        self.exit_button.grid(row=0, column=2, ipady=10, ipadx=10, padx=10)
        # ============================================

        # Cancel Button
        self.cancel_button = ttk.Button(self.buttons_frame, text="Cancel", command=self.cancel)
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

    @staticmethod
    def back(controller):
        controller.show_frame(MainPage, transform)

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

                from Graphs.Homogeneous import Homogeneous
                self.cancel_button.configure(state=NORMAL)
                self.generate_button.configure(state=DISABLED)
                self.back_button.configure(state=DISABLED)

                start = time()

                Homogeneous_Graph = Homogeneous()
                Homogeneous_Graph.create_homogeneous_graph(self.adjacency_type_selected.get(),
                                                           self.number_of_vertices_entry_result.get(), self.thread)

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
                    from Graphs.Random_Fixed_Graph import RandomFixedGraph
                    self.cancel_button.configure(state=NORMAL)
                    self.generate_button.config(state=DISABLED)
                    self.back_button.configure(state=DISABLED)

                    start = time()

                    Random_Fixed_Graph = RandomFixedGraph()
                    Random_Fixed_Graph.create_random_fixed_graph(self.adjacency_type_selected.get(),
                                                                 self.number_of_vertices_entry_result.get(),
                                                                 self.graph_degree_result.get(), self.seed_result.get(),
                                                                 self.thread)

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
                        from Graphs.Scale_Free_Graph_PA import ScaleFreeGraphPA
                        self.cancel_button.configure(state=NORMAL)
                        self.generate_button.config(state=DISABLED)
                        self.back_button.configure(state=DISABLED)

                        start = time()

                        ScaleFreeGraphPA = ScaleFreeGraphPA()
                        ScaleFreeGraphPA.create_scale_free_graph(self.adjacency_type_selected.get(),
                                                                 self.number_of_vertices_entry_result.get(),
                                                                 self.seed_result.get(), self.thread)

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
                        from Graphs.Full_Scale_Free_Graph import Full_Scale_Free_Graph
                        self.cancel_button.configure(state=NORMAL)
                        self.generate_button.config(state=DISABLED)

                        start = time()

                        Full_Scale_Free_Graph = Full_Scale_Free_Graph()
                        Full_Scale_Free_Graph.create_full_scale_free_graph(self.adjacency_type_selected.get(),
                                                                           self.number_of_vertices_entry_result.get(),
                                                                           self.number_of_initial_nodes_result.get(),
                                                                           self.seed_result.get(), self.thread)

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
                    from Graphs.ER_Graph import ER_Graph
                    self.cancel_button.configure(state=NORMAL)
                    self.generate_button.config(state=DISABLED)
                    self.back_button.configure(state=DISABLED)

                    start = time()

                    ER_Graph = ER_Graph()
                    ER_Graph.create_er_graph(self.adjacency_type_selected.get(),
                                             self.number_of_vertices_entry_result.get(),
                                             float(self.probability_result.get()), self.seed_result.get(), self.thread)

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

                from Graphs.ER_Graph import ER_Graph
                self.cancel_button.configure(state=NORMAL)
                self.generate_button.config(state=DISABLED)
                self.back_button.configure(state=DISABLED)

                start = time()

                ER_Graph = ER_Graph()
                ER_Graph.create_custom_er_graph(self.adjacency_type_selected.get(),
                                                self.number_of_vertices_entry_result.get(),
                                                self.number_of_edges_result.get(),
                                                float(self.probability_result.get()),
                                                self.seed_result.get(),
                                                self.thread)

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
                        from Graphs.Scale_Free_Graph_PA import ScaleFreeGraphPA
                        self.cancel_button.configure(state=NORMAL)
                        self.generate_button.config(state=DISABLED)
                        self.back_button.configure(state=DISABLED)

                        start = time()

                        ScaleFreeGraphPA = ScaleFreeGraphPA()
                        ScaleFreeGraphPA.create_custom_scale_free_graph(self.adjacency_type_selected.get(),
                                                                        self.number_of_vertices_entry_result.get(),
                                                                        self.number_of_edges_result.get(),
                                                                        self.seed_result.get(), self.thread)

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
                        from Graphs.Full_Scale_Free_Graph import Full_Scale_Free_Graph
                        self.cancel_button.configure(state=NORMAL)
                        self.generate_button.config(state=DISABLED)

                        start = time()

                        Full_Scale_Free_Graph = Full_Scale_Free_Graph()
                        Full_Scale_Free_Graph.create_full_scale_free_graph(self.adjacency_type_selected.get(),
                                                                           self.number_of_vertices_entry_result.get(),
                                                                           self.number_of_initial_nodes_result.get(),
                                                                           self.seed_result.get(), self.thread,
                                                                           self.initial_connections_per_node_result
                                                                           .get())  # --> Custom Full Scale-Free Graph.

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


class GraphAnalyzePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # MainPage Frame configuration
        self.configure(bg="azure3")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(20, weight=1)
        # ================================

        # Thread define
        self.thread_analyze = StoppableThread(target=self.analyze_button_func)
        # ================================

        # Button font
        self.button_font = ("Dialog", 9, "bold italic")
        # ================================

        # Main Label
        self.main_label = Label(self, bg="azure3", text="Analyze a graph\n",
                                font=("Arial", 20, "bold"))
        self.main_label.grid(row=1, column=1, padx=20)
        # ================================

        # Text Area Frame
        # create a Frame for the Text and Scrollbar
        self.my_frame_inner = ttk.Frame(self)
        # create a Scrollbar and associate it with txt
        self.my_scroll = Scrollbar(self.my_frame_inner, orient='vertical')
        # create a Text widget
        self.text_area = Text(self.my_frame_inner, background="lavender blush", yscrollcommand=self.my_scroll.set,
                              width=60,
                              height=23, relief=FLAT, borderwidth=5)
        self.text_area.bind("<FocusIn>", self.defocus)
        self.text_area.config(font=("consolas", 11), undo=True, wrap='word')
        self.my_scroll.config(command=self.text_area.yview)

        self.my_frame_inner.grid(row=1, column=2, rowspan=13, columnspan=2, sticky='nesw')
        self.text_area.grid(row=1, column=2, rowspan=13)
        self.my_scroll.grid(row=1, column=3, rowspan=13, columnspan=2, sticky='nesw')
        # ================================

        # Type Label
        self.main_label = Label(self, bg="azure3", text="Select type of file:\n",
                                font=("Arial", 10, "bold"))
        self.main_label.grid(row=2, column=1)
        # ================================

        # Type of graph being generated
        self.file_types = ['', 'Last Generated Graph', 'Pajek file']
        # ================================

        self.chosen_file_type = StringVar()
        self.chosen_file_type.set(self.file_types[1])

        self.graphs = ttk.OptionMenu(self, self.chosen_file_type, *self.file_types, command=self.show_parameters)
        self.graphs.grid(row=3, column=1, sticky="n")

        # Parameter's Frame
        self.parameters_frame = ttk.Frame(self)
        self.parameters_frame.grid_propagate(0)
        self.parameters_frame.configure(height=205, width=430)
        self.parameters_frame.grid(row=4, column=1, padx=10, pady=10)

        self.classpath_label = Label(self.parameters_frame, bg="azure3", text="Classpath:", font=self.button_font)

        self.classpath_result = StringVar()
        self.classpath_entry_box = ttk.Entry(self.parameters_frame, textvariable=self.classpath_result, width=35)
        # ==============================================================================================================

        # Adjacency Matrix, List Radiobuttons
        self.adjacency_type_selected = StringVar()
        self.matrix = ttk.Radiobutton(self.parameters_frame, text="Adjacency Matrix", value="Matrix",
                                      variable=self.adjacency_type_selected)
        self.matrix.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        self.list = ttk.Radiobutton(self.parameters_frame, text="Adjacency List", value="List",
                                    variable=self.adjacency_type_selected)
        self.list.grid(row=0, column=1, padx=30, pady=10, sticky="w")
        # ==============================================================================================================

        self.metrics_label = Label(self.parameters_frame, bg="azure3", text="Calculate metrics",
                                   font=("Arial", 10, "bold"))
        self.metrics_label.grid(row=1, column=0, columnspan=2)

        # Geodesic path, closeness centrality, betweenness centrality
        self.Edges = None
        self.Edges_dict = None
        self.Vertices = None
        self.geodesic_paths = None

        self.geodesic_path_selected = BooleanVar(False)
        self.geodesic_path = ttk.Checkbutton(self.parameters_frame, text="Geodesic Paths",
                                             variable=self.geodesic_path_selected)
        self.geodesic_path.grid(row=2, column=0, padx=30, pady=10, sticky="w")

        self.closeness_centrality_selected = BooleanVar(False)
        self.closeness_centrality = ttk.Checkbutton(self.parameters_frame, text="Closeness Centrality",
                                                    variable=self.closeness_centrality_selected)
        self.closeness_centrality.grid(row=2, column=1, padx=30, pady=10, sticky="w")

        self.betweenness_centrality_selected = BooleanVar(False)
        self.betweenness_centrality = ttk.Checkbutton(self.parameters_frame, text="Betweenness Centrality",
                                                      variable=self.betweenness_centrality_selected)
        self.betweenness_centrality.grid(row=3, column=0, padx=30, pady=10, sticky="w")
        # ==============================================================================================================

        # Analyze Button
        self.analyze_button = ttk.Button(self.parameters_frame, text="Analyze",
                                         command=lambda: self.thread_generate())
        self.analyze_button.grid(row=4, column=0, sticky="w", ipady=10, ipadx=10, pady=10, padx=30)
        # ============================================

        # Log Button
        self.log_button = ttk.Button(self.parameters_frame, text="Save output", command=self.save_output)
        self.log_button.grid(row=4, column=1, sticky="w", ipady=10, ipadx=10, pady=10, padx=30)
        # ============================================

        # Cancel Button
        self.cancel_button = ttk.Button(self.parameters_frame, text="Cancel", command=self.cancel)
        # ============================================

        # Browse Button
        browse_icon = PhotoImage(file='./images{}folder.png'.format(path_escape))
        self.browse_button = Button(self.parameters_frame, image=browse_icon, command=lambda: self.browse())
        self.browse_button.image = browse_icon
        self.browse_button.config(bg='azure3', relief='sunken', borderwidth=0)
        # ================================

        # Other Button's Frame
        self.rest_button_frame = Frame(self, bg="azure3")
        self.rest_button_frame.grid_propagate(0)
        self.rest_button_frame.configure(height=90, width=430)
        self.rest_button_frame.grid(row=5, column=1, padx=10, pady=20)

        # Back Button
        self.back_button = ttk.Button(self.rest_button_frame, text="Back", command=lambda: self.back(controller))
        self.back_button.grid(row=1, column=0, sticky="w", ipady=10, ipadx=10, pady=10, padx=(30, 70))
        # ================================

        # Exit Button
        self.exit_button = ttk.Button(self.rest_button_frame, text="Exit", command=lambda: sys.exit(0))
        self.exit_button.grid(row=1, column=1, sticky="w", ipady=10, ipadx=10, pady=10, padx=30)
        # ================================

    @staticmethod
    def defocus(event):
        event.widget.master.focus_set()

    def show_parameters(self, *args):
        if self.chosen_file_type.get() == "Pajek file":
            self.classpath_result.set("")

            self.matrix.grid_forget()
            self.list.grid_forget()
            self.metrics_label.grid_forget()
            self.geodesic_path.grid_forget()
            self.closeness_centrality.grid_forget()
            self.betweenness_centrality.grid_forget()

            self.classpath_label.grid(row=0, column=0, pady=10)
            self.classpath_entry_box.grid(row=0, column=0, columnspan=2, padx=(85, 0), pady=10)
            self.browse_button.grid(row=0, column=0, columnspan=3, sticky='e', padx=(0, 20), pady=(0, 3))
            self.metrics_label.grid(row=1, column=0, columnspan=2)
            self.geodesic_path.grid(row=2, column=0, padx=30, pady=10, sticky="w")
            self.closeness_centrality.grid(row=2, column=1, padx=30, pady=10, sticky="w")
            self.betweenness_centrality.grid(row=3, column=0, padx=30, pady=10, sticky="w")
            self.analyze_button.grid(row=4, column=0, sticky="w", ipady=10, ipadx=10, pady=10, padx=30)

        elif self.chosen_file_type.get() == "Last Generated Graph":
            self.classpath_label.grid_forget()
            self.classpath_entry_box.grid_forget()
            self.browse_button.grid_forget()

            self.matrix.grid(row=0, column=0, padx=30, pady=10, sticky="w")
            self.list.grid(row=0, column=1, padx=30, pady=10, sticky="w")
            self.metrics_label.grid(row=1, column=0, columnspan=2)
            self.geodesic_path.grid(row=2, column=0, padx=30, pady=10, sticky="w")
            self.closeness_centrality.grid(row=2, column=1, padx=30, pady=10, sticky="w")
            self.betweenness_centrality.grid(row=3, column=0, padx=30, pady=10, sticky="w")
            self.analyze_button.grid(row=4, column=0, ipady=10, ipadx=10, pady=10)

    def calculate_geodesic_paths(self):
        geodesic_paths = None

        message = "[*] Calculating Geodesic path for each node...\n"
        self.text_area.insert(END, message)
        self.text_area.update()

        if self.adjacency_type_selected.get() == "Matrix":
            try:

                geodesic_paths = find_geodesics(self.Edges, self.Vertices, self.text_area, self.thread_analyze)

                message = "\n[+] Finished Geodesic path analysis.\n"
                self.text_area.insert(END, message)
                self.text_area.update()

            except FileNotFoundError:
                message = "Please make sure that you have generated a graph!"
                messagebox.showerror("Error!", message)

                message = "\n[-] Failed to perform analysis.\n"
                self.text_area.insert(END, message)
                self.text_area.update()

        elif self.adjacency_type_selected.get() == "List":
            geodesic_paths = find_geodesics(self.Edges, self.Vertices, self.text_area, self.thread_analyze)

            message = "\n[+] Finished Geodesic path analysis.\n"
            self.text_area.insert(END, message)
            self.text_area.update()

        return geodesic_paths

    def calculate_closeness_centrality(self, geodesic_paths):
        message = "\n[*] Calculating Closeness Centrality of the graph...\n"
        self.text_area.insert(END, message)
        self.text_area.update()

        closeness_centrality(self.Vertices, geodesic_paths, self.text_area, self.thread_analyze)

        message = "\n[+] Finished Closeness Centrality analysis.\n"
        self.text_area.insert(END, message)
        self.text_area.see("end")
        self.text_area.update()

    def calculate_betweenness_centrality(self):
        message = "\n[*] Calculating Betweenness Centrality of each node...\n"
        self.text_area.insert(END, message)
        self.text_area.see("end")
        self.text_area.update()

        self.tuple_list_to_dict_list()

        all_paths = {}
        for i in range(self.Vertices):
            all_paths[str(i)] = {}
            for j in range(self.Vertices):
                paths = find_all_paths(self.Edges_dict, str(i), str(j), self.thread_analyze)  # All paths from i to j.
                all_paths[str(i)][str(j)] = paths

                # print("v{} ==> v{}: {}".format(i + 1, j + 1, paths))

        shortest_paths = find_shortest_paths(all_paths, self.thread_analyze)
        betweenness_centrality(shortest_paths, self.Vertices, self.text_area, self.thread_analyze)

        # for k, v in all_paths.items():
        #     for key, value in v.items():
        #         print("{} ==> {}: {}".format(k, key, value))

        # for k, v in all_paths.items():
        #     print("{{{}".format(k))
        #     print("\t", end="")
        #     for key, value in v.items():
        #         print("{{{}:\n\t\t[".format(key))
        #         print("\t\t", end="")
        #
        #         for path in value:
        #             if len(path) != 0:
        #                 print("\t{}".format(path))
        #                 print("\t\t", end="")
        #             else:
        #                 pass
        #         print(" ]")
        #         print("\t", end="")
        #     print()

    def thread_generate(self):
        self.thread_analyze = StoppableThread(target=self.analyze_button_func, daemon=True)
        self.thread_analyze.start()

    def cancel(self):
        if self.thread_analyze.is_alive():
            message = "[+] Terminating graph analysis...\n"
            self.text_area.insert(END, message)
            self.text_area.update()

            while self.thread_analyze.is_alive():
                self.thread_analyze.stop()

            message = "[!] Graph analysis was canceled!\n"
            self.text_area.insert(END, message)
            self.text_area.see("end")
            self.text_area.update()

            self.cancel_button.grid_forget()
            self.analyze_button.config(state=NORMAL)
            self.back_button.configure(state=NORMAL)

    def save_output(self):
        if not self.text_area.compare("end-1c", "==", "1.0"):
            with open("Output_Files{}log.txt".format(path_escape), "w") as f:
                f.write(self.text_area.get("1.0", "end-1c"))
                message = "Successfully saved output to Output_Files\\log.txt!"
                messagebox.showinfo("Success!", message)
        else:
            message = "No available output to save!"
            messagebox.showerror("Error!", message)

    @staticmethod
    def matrix_to_tuple_list(path_to_matrix_file):
        converted_list = []
        i = 0
        j = 0
        with open(path_to_matrix_file) as f:
            # Number of Vertices
            first_row = f.readline()
            counter = 0
            for char in first_row:
                if char != "\n":
                    counter += 1
            Vertices = counter
            f.seek(0)
            # ===============================================
            for k in range(Vertices):

                line = f.readline()

                for char in line:
                    if char != '\n':
                        if char == "1":
                            converted_list.append((str(i), str(j), 1))  # (From, To, Weight)
                        else:
                            pass
                        j += 1
                i += 1
                j = 0
        f.close()
        return converted_list, Vertices

    @staticmethod
    def list_file_to_tuple_list(path_to_list_file):
        converted_list = []
        with open(path_to_list_file, buffering=20000) as f:
            # Number of Vertices
            Vertices = int(f.readlines()[-1].split(':')[0]) + 1
            f.seek(0)
            # ===============================================

            for i in range(Vertices):

                node = f.readline().split(':')[1]

                neighbors = re.findall(r'(\d*[^,\n])', node)
                for neighbor in neighbors:
                    converted_list.append((str(i), str(neighbor), 1))  # (From, To, Weight)

        f.close()

        return converted_list, Vertices

    @staticmethod
    def dict_list_to_tuple_list(dictionary):
        converted_list = []

        for k, v in dictionary.items():
            for value in v:
                converted_list.append((k, value, 1))  # (From, To, Weight)

        return converted_list, len(dictionary)

    def tuple_list_to_dict_list(self):
        self.Edges_dict = {}

        for i in range(self.Vertices):
            self.Edges_dict[str(i)] = []

        for tup in self.Edges:
            self.Edges_dict[str(tup[0])].append(str(tup[1]))

    def browse(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("net files", "*.net"),
                                                                                              ("all files", "*.*")))
        self.classpath_result.set(filename)

    def analyze_button_func(self):
        self.cancel_button.grid(row=4, column=1, sticky="w", ipady=10, ipadx=10, pady=10, padx=30)
        self.analyze_button.config(state=DISABLED)
        self.back_button.config(state=DISABLED)

        if self.chosen_file_type.get() == "Last Generated Graph":

            analyzer.read_analysis(self.adjacency_type_selected.get(), self.text_area)

            if self.adjacency_type_selected.get() == "Matrix" or self.adjacency_type_selected.get() == "List":
                if self.geodesic_path_selected.get() is True or self.closeness_centrality_selected.get() is True \
                        or self.betweenness_centrality_selected.get() is True:

                    if self.adjacency_type_selected.get() == "Matrix":
                        try:
                            self.Edges, self.Vertices = self.matrix_to_tuple_list("Output_Files{}matrix.txt"
                                                                                  .format(path_escape))

                        except FileNotFoundError:
                            message = "Please make sure that you have generated a graph!"
                            messagebox.showerror("Error!", message)

                            message = "[-] Failed to perform analysis.\n"
                            self.text_area.insert(END, message)
                            self.text_area.update()
                    else:
                        try:
                            self.Edges, self.Vertices = self.list_file_to_tuple_list("Output_Files{}list.txt"
                                                                                     .format(path_escape))
                            print(self.Edges)

                        except FileNotFoundError:
                            message = "Please make sure that you have generated a graph!"
                            messagebox.showerror("Error!", message)

                            message = "[-] Failed to perform analysis.\n"
                            self.text_area.insert(END, message)
                            self.text_area.update()

                    if self.Edges is not None and self.Vertices is not None:

                        if self.geodesic_path_selected.get() is True:
                            self.geodesic_paths = self.calculate_geodesic_paths()

                            if self.closeness_centrality_selected.get() is True:
                                self.calculate_closeness_centrality(self.geodesic_paths)

                            if self.betweenness_centrality_selected.get() is True:
                                self.calculate_betweenness_centrality()

                        elif self.closeness_centrality_selected.get() is True:
                            self.geodesic_paths = self.calculate_geodesic_paths()
                            self.calculate_closeness_centrality(self.geodesic_paths)

                            if self.betweenness_centrality_selected.get() is True:
                                self.calculate_betweenness_centrality()

                        elif self.betweenness_centrality_selected.get() is True:
                            self.calculate_betweenness_centrality()

                        message = "\n[+] Finished last generated graph analysis!\n"
                        self.text_area.insert(END, message)
                        self.text_area.see("end")
                        self.text_area.update()

            else:
                message = "You must choose either adjacency matrix or adjacency list!"
                messagebox.showerror("Error!", message)

        elif self.chosen_file_type.get() == "Pajek file":
            self.adjacency_type_selected.set("List")
            if analyzer.analyze_pajek_file(self.text_area, self.classpath_result.get()):

                if self.geodesic_path_selected.get() is True or self.closeness_centrality_selected.get() is True \
                        or self.betweenness_centrality_selected.get() is True:

                    dictionary = analyzer.pajek_file_to_dict(self.classpath_result.get())
                    self.Edges, self.Vertices = self.dict_list_to_tuple_list(dictionary)

                    if self.Edges is not None and self.Vertices is not None:

                        if self.geodesic_path_selected.get() is True:
                            self.geodesic_paths = self.calculate_geodesic_paths()

                            if self.closeness_centrality_selected.get() is True:
                                self.calculate_closeness_centrality(self.geodesic_paths)

                            if self.betweenness_centrality_selected.get() is True:
                                self.calculate_betweenness_centrality()

                        elif self.closeness_centrality_selected.get() is True:
                            self.geodesic_paths = self.calculate_geodesic_paths()
                            self.calculate_closeness_centrality(self.geodesic_paths)

                            if self.betweenness_centrality_selected.get() is True:
                                self.calculate_betweenness_centrality()

                        elif self.betweenness_centrality_selected.get() is True:
                            self.calculate_betweenness_centrality()

                        message = "\n[+] Finished last generated graph analysis!\n"
                        self.text_area.insert(END, message)
                        self.text_area.see("end")
                        self.text_area.update()

        self.cancel_button.grid_forget()
        self.analyze_button.config(state=NORMAL)
        self.back_button.config(state=NORMAL)

    def back(self, controller):
        self.classpath_result.set("")
        self.text_area.delete('1.0', END)
        self.text_area.update()

        controller.show_frame(MainPage, transform)


class GraphVisualizePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # MainPage Frame configuration
        self.configure(bg="azure3")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(20, weight=1)
        # ================================

        # Button font
        self.button_font = ("Dialog", 9, "bold italic")
        # ================================

        # Main Label
        self.main_label = Label(self, bg="azure3", text="Visualize a graph\n",
                                font=("Arial", 20, "bold"))
        self.main_label.grid(row=1, column=1, padx=20)
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

        self.my_frame_inner.grid(row=1, column=2, rowspan=13, columnspan=2, sticky='nesw')
        self.text_area.grid(row=1, column=2, rowspan=13)
        self.my_scroll.grid(row=1, column=3, rowspan=13, columnspan=2, sticky='nesw')
        # ================================

        # Buttons Frame
        self.buttons_frame = Frame(self, bg="azure3")
        self.buttons_frame.grid_propagate(0)
        self.buttons_frame.configure(height=250, width=400)
        self.buttons_frame.grid(row=2, column=1, padx=10)
        # ================================

        self.adjacency_type_selected = StringVar()
        self.matrix = ttk.Radiobutton(self.buttons_frame, text="Adjacency Matrix", value="Matrix",
                                      variable=self.adjacency_type_selected)
        self.matrix.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        self.list = ttk.Radiobutton(self.buttons_frame, text="Adjacency List", value="List",
                                    variable=self.adjacency_type_selected)
        self.list.grid(row=0, column=1, padx=30, pady=10, sticky="w")

        # Pajek Visualize Button
        self.pajek_visualize_button = ttk.Button(self.buttons_frame, text="Pajek Visualize",
                                                 command=self.pajek_visualize)
        self.pajek_visualize_button.grid(row=1, column=0, ipady=10, ipadx=15)
        # ============================================

        # Plotly Visualize Button
        self.plotly_visualize_button = ttk.Button(self.buttons_frame, text="Plotly 3D Visualize",
                                                  command=self.Spawn_Login_Creds)
        self.plotly_visualize_button.grid(row=1, column=1, ipady=10, ipadx=15)
        # ============================================

        # 2D Matplotlib Visualize Button
        self.matplotlib_visualize_button = ttk.Button(self.buttons_frame, text="2D Matplotlib\nVisualize",
                                                      command=self.Plot_2D)
        self.matplotlib_visualize_button.grid(row=2, column=0, ipady=10, ipadx=15, pady=10)
        # ============================================

        # Back Button
        self.back_button = ttk.Button(self.buttons_frame, text="Back", command=lambda: self.back(controller))
        self.back_button.grid(row=3, column=0, ipady=10, ipadx=15, pady=10)
        # ================================

        # Exit Button
        self.exit_button = ttk.Button(self.buttons_frame, text="Exit", command=lambda: sys.exit(0))
        self.exit_button.grid(row=3, column=1, ipady=10, ipadx=15, pady=10, padx=45)
        # ================================

    @staticmethod
    def defocus(event):
        event.widget.master.focus_set()

    def back(self, controller):
        self.text_area.delete('1.0', END)
        self.text_area.update()

        controller.show_frame(MainPage, transform)

    def pajek_visualize(self):
        """ Visualizes the generated graph with the appropriate file format that pajek needs. """
        from Visualize.Pajek_Visualize import Visualizer

        if self.adjacency_type_selected.get() == "":
            message = "You must choose visualisation via matrix or list generated!"
            messagebox.showerror('Error!', message)

        elif self.adjacency_type_selected.get() == "Matrix":
            if Visualizer.pajek_visualize_matrix():
                message = "Visualization was successfully completed!"
                messagebox.showinfo('Success!', message)
            else:
                message = "Visualization failed!\n" \
                          "Make sure that you have generated a graph."
                messagebox.showerror("Error", message)

        elif self.adjacency_type_selected.get() == "List":
            if Visualizer.pajek_visualize_list():
                message = "Visualization was successfully completed!"
                messagebox.showinfo('Success!', message)
            else:
                message = "Visualization failed!\n" \
                          "Make sure that you have generated a graph."
                messagebox.showerror("Error", message)

    def Spawn_Login_Creds(self):

        if self.adjacency_type_selected.get() == "":
            message = "You must choose 3D visualisation via matrix or list generated!"
            messagebox.showerror("Error", message)

        else:
            root2 = Toplevel()
            creds_GUI = LoginCreds(root2)
            self.master.wait_window(root2)

            if creds_GUI.username_entry_result == "" or creds_GUI.api_key_entry_result == "":
                self.text_area.delete('1.0', END)
                self.text_area.update()

                message1 = "[-] Failed to create 3D Graph with Plotly.\n\n"
                self.text_area.insert(END, message1)
                self.text_area.update()

            else:
                self.plotly_visualize(creds_GUI.username_entry_result, creds_GUI.api_key_entry_result,
                                      creds_GUI.filename_entry_result)

    def plotly_visualize(self, username, api_key, output_filename):
        """ Visualizes the generated graph in 3D form with the appropriate file format that plotly needs. """

        from Visualize.Plotly3D import plotly_visualizer

        start = time()

        self.text_area.delete('1.0', END)
        message1 = "[+] Please wait while 3D Plotly Graph is being created.\n" \
                   "This will probably take a moment...\n\n"
        self.text_area.insert(END, message1)
        self.text_area.update()

        try:
            plot_result = False

            if self.adjacency_type_selected.get() == "Matrix":
                plot_result = plotly_visualizer.plotly_visualize_matrix(username, api_key, output_filename)

            elif self.adjacency_type_selected.get() == "List":
                plot_result = plotly_visualizer.plotly_visualize_list(username, api_key, output_filename)

            if plot_result is True:

                end_3d = time() - start
                message2 = "[+] The 3D Plotly Graph was generated successfully!\n\n"
                self.text_area.insert(END, message2)

                message3 = "[+] Elapsed time: {:>.2f} sec\n".format(end_3d)
                self.text_area.insert(END, message3)
                self.text_area.update()

                self.Spawn_Custom_Popup(plotly_visualizer.link)

            elif plot_result == "File not found":

                self.text_area.delete('1.0', END)

                message = "3D Visualization failed!\n" \
                          "Make sure that you have generated a graph."
                messagebox.showerror("Error", message)

            else:
                self.text_area.delete('1.0', END)
                self.text_area.update()

                message1 = "[-] Failed to create 3D Graph with Plotly.\n\n"
                self.text_area.insert(END, message1)
                self.text_area.update()

                self.Spawn_Login_Creds()

        except TypeError:
            self.text_area.delete('1.0', END)
            self.text_area.update()

            message1 = "[-] Failed to create 3D Graph with Plotly.\n\n"
            self.text_area.insert(END, message1)
            self.text_area.update()

    def Plot_2D(self):
        import Visualize.Plot_2D

        plot = Visualize.Plot_2D.Plot_2D()

        if self.adjacency_type_selected.get() == "":
            message = "You must choose visualisation via matrix or list generated!"
            messagebox.showerror('Error!', message)

        elif self.adjacency_type_selected.get() == "Matrix":
            if plot.graph_topology_matrix():
                plot.extract_possibilities()
                plot.plot_2d("Matrix")

            else:
                message = "Visualization failed!\n" \
                          "Make sure that you have generated a graph."
                messagebox.showerror("Error", message)

        elif self.adjacency_type_selected.get() == "List":
            if plot.graph_topology_list():
                plot.extract_possibilities()
                plot.plot_2d("List")

            else:
                message = "Visualization failed!\n" \
                          "Make sure that you have generated a graph."
                messagebox.showerror("Error", message)

    def Spawn_Custom_Popup(self, url):
        root3 = Toplevel()
        custom_popup = CustomPopUp(root3)
        custom_popup.Plotly_popup(url)
        self.master.wait_window(root3)


class LoginCreds:

    def __init__(self, master):
        self.master = master
        self.master.focus()
        self.forget_credentials_variable = BooleanVar(False)

        # Fonts & Styles
        self.label_font = ("Dialog", 11, "bold italic")
        self.button_font = ("Dialog", 9, "bold italic")

        self.master.style = ttk.Style()
        self.master.style.configure('TButton', background='seashell3', foreground='black', relief='flat', width=15)

        self.master.style.configure('TCheckbutton', background='azure3', foreground='black', relief='flat',
                                    font=self.button_font)

        self.master.style.configure('TLabel', background='azure3', foreground='black', relief='flat',
                                    font=self.button_font)

        self.master.style.configure('TEntry', background='azure3', foreground='black', relief='flat',
                                    font=self.button_font)
        # ================================

        self.master.title("Login")
        self.master.protocol('WM_DELETE_WINDOW', self.x_button)
        self.master.wait_visibility(self.master)
        self.master.config(bg="azure3")
        self.master["padx"] = 10
        self.master["pady"] = 10

        self.main_label = ttk.Label(self.master, text="Enter your plotly credentials in order to generate a 3D Graph.",
                                    font=("Arial", 13, "bold"))
        self.main_label.grid(row=0, columnspan=2, ipady=10)

        self.username_label = ttk.Label(self.master, text="Username")
        self.username_label.grid(row=1, column=0, pady=5, padx=5, sticky="e")

        self.username_entry_result = ""
        self.username_entry = Entry(self.master, text="Username")
        self.username_entry.grid(row=1, column=1, padx=5, ipadx=15, ipady=2, sticky="w")

        self.api_key_label = ttk.Label(self.master, text="API_Key")
        self.api_key_label.grid(row=2, column=0, pady=5, padx=5, sticky="e")

        self.api_key_entry_result = ""
        self.api_key_entry = Entry(self.master, text="API Key", show="*")
        self.api_key_entry.grid(row=2, column=1, padx=5, ipadx=15, ipady=2, sticky="w")

        self.filename_label = ttk.Label(self.master, text="Output Filename")
        self.filename_label.grid(row=3, column=0, pady=5, padx=5, sticky="e")

        self.filename_entry_result = ""
        self.filename_entry = Entry(self.master, text="Out Filename")
        self.filename_entry.grid(row=3, column=1, padx=5, ipadx=15, ipady=2, sticky="w")

        self.remember_me_variable = BooleanVar(False)
        self.remember_me_checkbutton = ttk.Checkbutton(self.master, text="Remember me",
                                                       variable=self.remember_me_variable)
        self.remember_me_checkbutton.grid(row=4, column=0, pady=10)

        self.no_account_label = Label(self.master, text="Don't have an account on Plotly?", fg="blue", bg="azure3",
                                      cursor="hand2", font=("Arial", 10, "bold"))
        self.no_account_label.grid(row=5, columnspan=2, pady=5)
        self.no_account_label.bind("<Button-1>", lambda event, url="https://plot.ly/feed/#/": self.callback(url))

        self.continue_button = ttk.Button(self.master, text="Continue",
                                          command=self.continue_button_func)
        self.continue_button.grid(row=6, column=0, pady=20, ipady=5)

        self.cancel_button = ttk.Button(self.master, text="Cancel",
                                        command=self.x_button)
        self.cancel_button.grid(row=6, column=1, pady=20, ipady=5)

        self.forget_credentials = ttk.Checkbutton(self.master, text="Forget my credentials",
                                                  variable=self.forget_credentials_variable)

        if self.credential_spawn():
            global temp_bg
            temp_bg = "light goldenrod"
            self.forget_credentials.grid(row=4, column=0, sticky="e", columnspan=2, padx=100)

        else:
            temp_bg = "white"

        self.username_entry.configure(background=temp_bg)
        self.api_key_entry.configure(background=temp_bg)

        self.center(self.master)

    def continue_button_func(self):
        if self.username_entry.get() == "" or self.api_key_entry.get() == "" or self.filename_entry.get() == "":
            message = "Please enter a Username an API key and an Output filename before continuing!"
            messagebox.showerror("Error!", message)
            self.master.lift()
            self.master.focus()
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
                connection_handler.Insert(self.username_entry_result, self.api_key_entry_result)

            if self.forget_credentials_variable.get():
                connection_handler.Delete()

            self.username_entry.delete(0, 'end')
            self.api_key_entry.delete(0, 'end')
            self.filename_entry.delete(0, 'end')
            self.master.destroy()

            if self.remember_me_variable.get():
                connection_handler.Insert(self.username_entry_result, self.api_key_entry_result)

    def x_button(self):
        self.username_entry_result = self.username_entry.get()
        self.api_key_entry_result = self.api_key_entry.get()

        if self.remember_me_variable.get() and self.username_entry.get() != "" and self.api_key_entry.get() != "":
            connection_handler.Insert(self.username_entry_result, self.api_key_entry_result)

        if self.forget_credentials_variable.get():
            connection_handler.Delete()

        self.username_entry.delete(0, 'end')
        self.api_key_entry.delete(0, 'end')
        self.filename_entry.delete(0, 'end')
        self.username_entry_result = ""
        self.api_key_entry_result = ""

        self.master.destroy()

    def credential_spawn(self):
        credentials = connection_handler.Get_creds()
        if connection_handler.Db_check():
            self.username_entry.insert(END, credentials[0])
            self.api_key_entry.insert(END, credentials[1])
            return True

        else:
            return False

    @staticmethod
    def callback(url):
        webbrowser.open_new(r"{}".format(url))

    @staticmethod
    def center(master):
        master.update()

        size_x = master.winfo_width()

        size_y = master.winfo_height()

        w = master.winfo_screenwidth()

        h = master.winfo_screenheight()

        size = (size_x, size_y)
        x = w / 2 - size[0] / 2

        y = h / 2 - size[1] / 2

        master.geometry("%dx%d+%d+%d" % (size + (x, y)))


class CustomPopUp:

    def __init__(self, master):
        self.master = master
        self.label_font = ("Dialog", 11, "bold italic")

    def Plotly_popup(self, url):
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

        self.master.bind("<FocusOut>", lambda event: self.Alarm(self.master))

        view_graph_button = ttk.Button(self.master, text="View 3D Graph\non plotly",
                                       command=lambda: self.callback(url, self.master))
        view_graph_button.grid(row=2, padx=80, pady=15, sticky="w")

        view_later_button = ttk.Button(self.master, text="View Later",
                                       command=lambda: self.store_link(url, self.master))
        view_later_button.grid(row=2, padx=80, pady=15, sticky="e")

    @staticmethod
    def Alarm(master):
        master.bell()
        master.focus_force()

    @staticmethod
    def store_link(url, root2):
        with open("Output_Files{}Plotly_link.txt".format(path_escape), "w") as f:
            f.write(url)
            f.close()

        root2.destroy()

        message_info = "Plotly 3D url stored in plaintext for later usage under the Output_Files folder" \
                       " with name Plotly_link.txt"
        messagebox.showinfo("Saved!", message_info)

    @staticmethod
    def callback(url, root2):
        with open("Output_Files{}Plotly_link.txt".format(path_escape), "w") as f:
            f.write(url)
            f.close()

        root2.destroy()

        message_info = "Plotly 3D url stored in plaintext for later usage under the Output_Files folder" \
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


if __name__ == "__main__":
    GUI = App()
    GUI.center()
    connection_handler = Connection()
    GUI.mainloop()
