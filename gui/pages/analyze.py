from gui.pages.page import *
from Analyze.Analyze import *
from tkinter import filedialog
from Analyze.Geodesic_Paths import find_geodesics
from Analyze.Centrality import closeness_centrality
from Analyze.Paths import find_all_paths, find_shortest_paths
from Analyze.Betweenness_Centrality import betweenness_centrality


class GraphAnalyzePage(Page):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Graph Analyze Frame configuration
        self.configure(bg="azure3")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.widget_pady = 10
        # ================================

        # Thread define
        self.thread_analyze = StoppableThread(target=self.analyze_button_func)
        # ================================

        # Button font
        self.button_font = ("Dialog", 9, "bold italic")
        # ================================

        # Define Frames
        # Parameter's Frame
        self.parameters_frame = Frame(self, bg="azure3", width=300)
        self.parameters_frame.grid_propagate(0)
        self.parameters_frame.columnconfigure(0, weight=1)
        self.parameters_frame.columnconfigure(1, weight=1)
        self.parameters_frame.rowconfigure(4, weight=1)
        self.parameters_frame.grid(row=0, column=0, sticky="news")

        self.parameters_frame_row_0_column_0 = Frame(self.parameters_frame, height=170, bg="azure3")
        self.parameters_frame_row_0_column_0.grid_propagate(0)
        self.parameters_frame_row_0_column_0.columnconfigure(0, weight=1)
        self.parameters_frame_row_0_column_0.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='news')

        self.parameters_frame_row_1_column_0 = Frame(self.parameters_frame, width=30, height=50, bg="azure3")
        self.parameters_frame_row_1_column_0.grid_propagate(0)
        self.parameters_frame_row_1_column_0.columnconfigure(0, weight=1)
        self.parameters_frame_row_1_column_0.rowconfigure(0, weight=1)
        self.parameters_frame_row_1_column_0.grid(row=1, column=0, padx=5, sticky='news')

        self.parameters_frame_row_1_column_1 = Frame(self.parameters_frame, width=30, height=50, bg="azure3")
        self.parameters_frame_row_1_column_1.grid_propagate(0)
        self.parameters_frame_row_1_column_1.columnconfigure(0, weight=1)
        self.parameters_frame_row_1_column_1.rowconfigure(0, weight=1)
        self.parameters_frame_row_1_column_1.grid(row=1, column=1, padx=5, sticky='news')

        self.parameters_frame_row_2_column_0 = Frame(self.parameters_frame, bg="azure3")
        self.parameters_frame_row_2_column_0.columnconfigure(0, weight=1)
        self.parameters_frame_row_2_column_0.grid(row=2, column=0, columnspan=2, sticky='news')

        self.parameters_frame_row_3_column_0 = Frame(self.parameters_frame, bg="azure3")
        self.parameters_frame_row_3_column_0.columnconfigure(0, weight=1)
        self.parameters_frame_row_3_column_0.grid(row=3, column=0, padx=5, pady=5, sticky='news')

        self.parameters_frame_row_3_column_1 = Frame(self.parameters_frame, bg="azure3")
        self.parameters_frame_row_3_column_1.columnconfigure(0, weight=1)
        self.parameters_frame_row_3_column_1.grid(row=3, column=1, padx=5, pady=5, sticky='news')

        self.buttons_frame = Frame(self.parameters_frame, bg="azure3")
        self.buttons_frame.columnconfigure(0, weight=1)
        self.buttons_frame.columnconfigure(1, weight=1)
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.rowconfigure(1, weight=1)
        self.buttons_frame.grid(row=4, columnspan=2, sticky="news")

        self.scroll_area_frame = ttk.Frame(self)
        self.scroll_area_frame.columnconfigure(0, weight=1)
        self.scroll_area_frame.rowconfigure(0, weight=1)
        self.scroll_area_frame.grid(row=0, column=1, sticky='news')

        # Main Label
        self.main_label = Label(self.parameters_frame_row_0_column_0, bg="azure3", text="Analyze a graph",
                                font=("Arial", 20, "bold"))
        self.main_label.grid(row=0, column=0, pady=self.widget_pady)
        # ================================

        # Type Label
        self.main_label = Label(self.parameters_frame_row_0_column_0, bg="azure3", text="Select type of file",
                                font=("Arial", 10, "bold"))
        self.main_label.grid(row=1, column=0, pady=self.widget_pady)
        # ================================

        # Type of graph being generated
        self.file_types = ['', 'Last Generated Graph', 'Pajek file']
        # ================================

        self.chosen_file_type = StringVar()
        self.chosen_file_type.set(self.file_types[1])

        self.graphs = ttk.OptionMenu(self.parameters_frame_row_0_column_0, self.chosen_file_type, *self.file_types, command=self.show_parameters)
        self.graphs.grid(row=2, column=0, pady=self.widget_pady)

        self.classpath_label = Label(self.parameters_frame_row_0_column_0, bg="azure3", text="Classpath:", font=self.button_font)

        self.classpath_result = StringVar()
        self.classpath_entry_box = ttk.Entry(self.parameters_frame_row_1_column_0, textvariable=self.classpath_result, width=25)
        # ==============================================================================================================

        # Adjacency Matrix, List Radiobuttons
        self.adjacency_type_selected = StringVar()
        self.matrix = ttk.Radiobutton(self.parameters_frame_row_1_column_0, text="Adjacency Matrix", value="Matrix",
                                      variable=self.adjacency_type_selected)
        self.matrix.grid(row=3, column=0)

        self.list = ttk.Radiobutton(self.parameters_frame_row_1_column_1, text="Adjacency List", value="List",
                                    variable=self.adjacency_type_selected)
        self.list.grid(row=3, column=0)
        # ==============================================================================================================

        self.metrics_label = Label(self.parameters_frame_row_2_column_0, bg="azure3", text="Calculate metrics",
                                   font=("Arial", 10, "bold"))
        self.metrics_label.grid(row=0, column=0, pady=self.widget_pady)

        # Geodesic path, closeness centrality, betweenness centrality
        self.Edges = None
        self.Edges_dict = None
        self.Vertices = None
        self.geodesic_paths = None

        self.geodesic_path_selected = BooleanVar(False)
        self.geodesic_path = ttk.Checkbutton(self.parameters_frame_row_3_column_0, text="Geodesic Paths",
                                             variable=self.geodesic_path_selected)
        self.geodesic_path.grid(row=0, column=0, pady=self.widget_pady)

        self.closeness_centrality_selected = BooleanVar(False)
        self.closeness_centrality = ttk.Checkbutton(self.parameters_frame_row_3_column_1, text="Closeness Centrality",
                                                    variable=self.closeness_centrality_selected)
        self.closeness_centrality.grid(row=0, column=0, pady=self.widget_pady)

        self.betweenness_centrality_selected = BooleanVar(False)
        self.betweenness_centrality = ttk.Checkbutton(self.parameters_frame_row_3_column_0, text="Betweenness Centrality",
                                                      variable=self.betweenness_centrality_selected)
        self.betweenness_centrality.grid(row=1, column=0, pady=self.widget_pady)
        # ==============================================================================================================

        # Analyze Button
        self.analyze_button = ttk.Button(self.buttons_frame, text="Analyze",
                                         command=lambda: self.thread_generate())
        self.analyze_button.grid(row=0, column=0, ipady=10, ipadx=10, pady=self.widget_pady)
        # ============================================

        # Log Button
        self.log_button = ttk.Button(self.buttons_frame, text="Save output", command=self.save_output)
        self.log_button.grid(row=0, column=1, ipady=10, ipadx=10, pady=self.widget_pady)
        # ============================================

        # Back Button
        self.back_button = ttk.Button(self.buttons_frame, text="Back", command=lambda: self.back(controller))
        self.back_button.grid(row=1, column=0, ipady=10, ipadx=10, pady=self.widget_pady)
        # ================================

        # Exit Button
        self.exit_button = ttk.Button(self.buttons_frame, text="Exit", command=lambda: sys.exit(0))
        self.exit_button.grid(row=1, column=1, ipady=10, ipadx=10, pady=self.widget_pady)
        # ================================

        # Cancel Button
        self.cancel_button = ttk.Button(self.buttons_frame, text="Cancel", command=self.cancel)
        # ============================================

        # Browse Button
        try:
            browse_icon = PhotoImage(file='./images{}folder.png'.format(path_escape))
            self.browse_button = Button(self.parameters_frame_row_1_column_1, image=browse_icon, command=lambda: self.browse())
            self.browse_button.image = browse_icon
            self.browse_button.config(bg='azure3', relief='flat', borderwidth=0, highlightbackground="azure3")
        except TclError:
            self.browse_button = Button(self.parameters_frame_row_1_column_1, text='Browse', command=lambda: self.browse())
            self.browse_button.config(bg='azure3', relief='flat', borderwidth=1)
        # ================================

        # Text Area Frame
        # create a Scrollbar and associate it with txt
        self.my_scroll = Scrollbar(self.scroll_area_frame, orient='vertical')
        # create a Text widget
        self.text_area = Text(self.scroll_area_frame, background="lavender blush", yscrollcommand=self.my_scroll.set, relief=FLAT,
                              width=35)
        self.text_area.bind("<FocusIn>", self.defocus)
        self.text_area.config(font=("consolas", 11), undo=True, wrap='word')
        self.my_scroll.config(command=self.text_area.yview)
        MousewheelSupport(self).add_support_to(self.text_area, yscrollbar=self.my_scroll, what="units")

        self.text_area.grid(row=0, column=0, sticky='news')
        self.my_scroll.grid(row=0, column=1, sticky='news')
        # ================================

    @staticmethod
    def defocus(event):
        event.widget.master.focus_set()

    def show_parameters(self, *args):
        if self.chosen_file_type.get() == "Pajek file":
            self.classpath_result.set("")

            self.matrix.grid_forget()
            self.list.grid_forget()

            self.classpath_label.grid(row=3, column=0)
            self.classpath_entry_box.grid(row=0, column=0, sticky="e")
            self.browse_button.grid(row=0, column=0, sticky="w")

        elif self.chosen_file_type.get() == "Last Generated Graph":
            self.classpath_label.grid_forget()
            self.classpath_entry_box.grid_forget()
            self.browse_button.grid_forget()

            self.matrix.grid(row=3, column=0)
            self.list.grid(row=3, column=0)

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
        filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("net files", "*.net"),
                                                                                              ("all files", "*.*")))
        self.classpath_result.set(filename)

    def analyze_button_func(self):
        self.cancel_button.grid(row=0, column=0, ipady=10, ipadx=10, pady=self.widget_pady)
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
        self.back_button.config(state=NORMAL)

    def back(self, controller):
        self.classpath_result.set("")
        self.text_area.delete('1.0', END)
        self.text_area.update()

        controller.show_frame(self.retrieve_frame(controller, 'MainPage'), transform)
