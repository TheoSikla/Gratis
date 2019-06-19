import datetime
from tkinter import END
from tkinter import messagebox
import re
from os_recon.define_os import path_escape


class Analyze:

    @staticmethod
    def analyze_matrix(adjacency_matrix, graph_type, numOfVertices, graphDegree=None, numOfEdges=None,
                       numOfInitialNodes=None, initialConnectionsPerNode=None, probability=None, seed=None):
        """ Analyzes a generated graph. """

        global highest_node_indicator, first
        with open(f"Output_Files{path_escape}graph_analysis_matrix.txt", "w") as f:

            version = 'Gratis v1.0'

            analysis = {
                        'Graph type: ': graph_type,
                        'Number of Vertices: ': numOfVertices,
                        'Graph Degree: ': graphDegree,
                        'Number of maximum Edges: ': numOfEdges,
                        'Number of Initial Nodes: ': numOfInitialNodes,
                        'Initial Connections Per Node: ': initialConnectionsPerNode,
                        'Probability: ': probability,
                        'Seed: ': seed
                        }

            # Matrix Analysis
            connections = 0
            numOfEdgesPerNode = [0] * numOfVertices

            for i in range(len(adjacency_matrix)):
                for j in range(len(adjacency_matrix)):
                    if i != j and i < j:
                        if adjacency_matrix[i][j] >= 1:
                            numOfEdgesPerNode[i] += 1
                            numOfEdgesPerNode[j] += 1
                            connections += 1

            first = 0
            highest_node_indicator = 0
            for i in range(numOfVertices):
                if numOfEdgesPerNode[i] > first:
                    highest_node_indicator = i
                    first = numOfEdgesPerNode[i]

            analysis['Total number of Edges: '] = connections

            # ====================================================
            output = ''
            output += "[*] Starting last generated Graph Analysis (Matrix)...\n"
            output += "===================================\n"
            output += f"Version: {version}\n"

            for k, v in analysis.items():
                if v is not None:
                    output += "{k}{v}\n"

            try:
                output += f"Node {highest_node_indicator + 1} has the most edges ({first})\n"

            except NameError:
                pass

            output += f"The date is: {datetime.datetime.today().strftime('%m/%d/%Y')}\n"
            output += "===================================\n\n"
            
            f.write(output)
            del output


    @staticmethod
    def analyze_list(adjacency_list, graph_type, numOfVertices, graphDegree=None, numOfEdges=None,
                     numOfInitialNodes=None, initialConnectionsPerNode=None, probability=None, seed=None):
        """ Analyzes a generated graph. """

        global highest_node_indicator, first
        with open(f"Output_Files{path_escape}graph_analysis_list.txt", "w") as f:

            version = 'Graph Sphere v1.0'

            analysis = {
                'Graph type: ': graph_type,
                'Number of Vertices: ': numOfVertices,
                'Graph Degree: ': graphDegree,
                'Number of maximum Edges: ': numOfEdges,
                'Number of Initial Nodes: ': numOfInitialNodes,
                'Initial Connections Per Node: ': initialConnectionsPerNode,
                'Probability: ': probability,
                'Seed: ': seed
            }

            # Matrix Analysis
            connections = 0

            numOfEdgesPerNode = [0] * numOfVertices

            for vertex, neighbors in adjacency_list.items():
                number_of_edges = 0
                for _ in neighbors:
                    number_of_edges += 1

                numOfEdgesPerNode[int(vertex)] = number_of_edges
                connections += number_of_edges

            connections = connections // 2

            first = 0
            highest_node_indicator = 0
            for i in range(numOfVertices):
                if numOfEdgesPerNode[i] > first:
                    highest_node_indicator = i
                    first = numOfEdgesPerNode[i]

            analysis['Total number of Edges: '] = connections

            # ====================================================
            output = ''
            output += "[*] Starting last generated Graph Analysis (List)...\n"
            output += "===================================\n"
            output += f"Version: {version}\n"

            for k, v in analysis.items():
                if v is not None:
                    output += f"{k}{v}\n"

            try:
                output += f"Node {highest_node_indicator + 1} has the most edges ({first})\n"

            except NameError:
                pass

            output += f"The date is: {datetime.datetime.today().strftime('%m/%d/%Y')}\n"
            output += "===================================\n\n"
            f.write(output)
            del output

    @staticmethod
    def read_analysis(adjacency_type, text_area):

        text_area.delete('1.0', END)
        text_area.update()

        if adjacency_type == "Matrix":
            with open(f"Output_Files{path_escape}graph_analysis_matrix.txt", "r") as f:
                for line in f:
                    text_area.insert(END, line)
                text_area.update()

        elif adjacency_type == "List":
            with open(f"Output_Files{path_escape}graph_analysis_list.txt", "r") as f:
                for line in f:
                    text_area.insert(END, line)
                text_area.update()

    @staticmethod
    def pajek_file_to_dict(path):
        try:

            nodes_n_edges = {}
            with open(path, "r") as f:
                flag = False
                # For node names
                for line in f:
                    line = line.replace("\n", "").strip()

                    if flag is True:
                        break

                    if "*Vertices" in str(line):
                        pass

                    elif "*Edges" in str(line):
                        break

                    elif re.search(r'(\b[0-9]*)', line) is None and re.search(r'"([A-Za-z0-9]*)"', line) is None \
                            or re.search(r'(\b[0-9]*)', line).group(1) == "":
                        messagebox.showerror("Error", "Invalid pajek file format!")
                        flag = True
                        break

                    elif re.search(r'\d+', line) is not None:
                        nodes_n_edges[str(int(re.search(r'\d+', line).group()) - 1)] = []

                    else:
                        messagebox.showerror("Error", "Invalid pajek file format!")
                        flag = True
                        break

                # For edges
                for line in f:
                    if flag is True:
                        break
                    try:
                        line = line.replace("\n", "").strip()
                        edge = re.findall(r'(\b[0-9]+)', line)

                        nodes_n_edges[str(int(edge[0]) - 1)].append(str(int(edge[1]) - 1))
                        nodes_n_edges[str(int(edge[1]) - 1)].append(str(int(edge[0]) - 1))

                    except (IndexError, KeyError):
                        messagebox.showerror("Error", "Invalid pajek file format!")
                        break

                return nodes_n_edges

        except FileNotFoundError:
            message = "File not found!"
            messagebox.showerror("Error", message)

    @staticmethod
    def analyze_pajek_file(text_area, path):
        if len(path) == 0:
            messagebox.showerror("Error", "Please select a file to import!")
            return False

        try:
            re.search(r'\.net$', path).group()
        except AttributeError:
            messagebox.showerror("Error", "Invalid file!")
            return False

        try:
            text_area.delete('1.0', END)
            text_area.update()

            node_names = []
            nodes_n_edges = {}
            counter = 1
            with open(path, "r") as f:
                # For node names
                for line in f:
                    line = line.replace("\n", "").strip()

                    if "*Vertices" in str(line):
                        pass

                    elif "*Edges" in str(line):
                        break

                    elif re.search(r'(\b[0-9]*)', line) is None and re.search(r'"([A-Za-z0-9]*)"', line) is None \
                            or re.search(r'(\b[0-9]*)', line).group(1) == "":
                        messagebox.showerror("Error", "Invalid pajek file format!")
                        return False

                    elif re.search(r'"([A-Za-z0-9]*)"', line) is not None:
                        nodes_n_edges[str(counter)] = 0
                        counter += 1
                        node_names.append(str((re.search(r'"([A-Za-z0-9]*)"', line).group(1))))

                    elif re.search(r'(\b[0-9]*)', line) is not None:
                        nodes_n_edges[str(counter)] = 0
                        counter += 1
                        node_names.append(str((re.search(r'(\b[0-9]*)', line).group(1))))

                    else:
                        messagebox.showerror("Error", "Invalid pajek file format!")
                        return False

                # For edges
                for line in f:
                    try:
                        line = line.replace("\n", "").strip()
                        edge = re.findall(r'(\b[0-9]+)', line)

                        nodes_n_edges[str(edge[0])] += 1
                        nodes_n_edges[str(edge[1])] += 1

                    except (IndexError, KeyError):
                        messagebox.showerror("Error", "Invalid pajek file format!")
                        return False

                counter = 0
                max_edges = 0
                node_most_edges = None
                for k, v in nodes_n_edges.items():
                    if max_edges < int(v):
                        max_edges = int(v)
                        node_most_edges = counter
                    text = "Node {:<{}} has {:<{}} edges.\n".format(node_names[counter],
                                                                    len(node_names[-1]), int(v), len(str(v)))
                    text_area.insert(END, text)
                    text_area.update()
                    counter += 1

                text = f"\nNode {node_names[node_most_edges]} has the most edges ({max_edges})!\n\n"=

                text_area.insert(END, text)
                text_area.update()

                return True

        except FileNotFoundError:
            message = "File not found!"
            messagebox.showerror("Error", message)
            return False


analyzer = Analyze()
