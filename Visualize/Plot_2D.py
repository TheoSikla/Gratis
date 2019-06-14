from os_recon.define_os import path_escape
import re
import operator
import matplotlib.pyplot as plt
import matplotlib.ticker
from math import pow


class Plot2D:
    """ Extracts the probabilities and creates a plot (Distribution plot) of the graph chosen by the UI. """

    def __init__(self):
        self.num_of_vertices = None

    def graph_topology_matrix(self):
        file_output = ''
        with open(f"Output_Files{path_escape}Graph_topology.txt", "w") as graph_topology:

            try:
                with open(f"Output_Files{path_escape}matrix.txt", buffering=20000) as f:
                    # Number of Vertices

                    self.num_of_vertices = len(f.readline().replace("\n", ""))
                    f.seek(0)

                    i = 0
                    j = 0
                    for line in f:
                        for char in line:
                            if str(char) == '1' and i < j:
                                file_output += f"{i} {j}\n"
                            j += 1
                        j = 0
                        i += 1

                graph_topology.write(file_output)
                del file_output
                return True
            except FileNotFoundError:
                return False

    def graph_topology_list(self):
        file_output = ''
        with open(f"Output_Files{path_escape}Graph_topology.txt", "w") as graph_topology:

            try:
                with open(f"Output_Files{path_escape}list.txt", buffering=20000) as f:
                    # Number of Vertices
                    self.num_of_vertices = int(f.readlines()[-1].split(':')[0]) + 1
                    f.seek(0)
                    # ===============================================

                    for i in range(self.num_of_vertices):
                        neighbors = re.findall(r'(\d*[^,\n])', f.readline().split(':')[1])
                        if len(neighbors) > 0:
                            for neighbor in neighbors:
                                if i < int(neighbor):
                                    file_output += f"{i} {neighbor}\n"

                graph_topology.write(file_output)
                del file_output
                return True
            except FileNotFoundError:
                return False

    def extract_possibilities(self):
        with open(f"Output_Files{path_escape}Graph_topology.txt") as f:
            num_of_edges = {i: 0 for i in range(self.num_of_vertices)}

            line = f.readline()
            while line:
                if len(line) != 0:
                    line = re.findall(r'(\b[0-9]+)', line)
                    num_of_edges[int(line[0])] += 1
                    num_of_edges[int(line[1])] += 1
                    line = f.readline()

            # for key, value in num_of_edges.items():
            #     print("Node {} has {} edges.".format(key, value))

            edges_n_nodes = {}

            for i in range(self.num_of_vertices):
                counter = 0
                for key, value in num_of_edges.items():
                    if i == value:
                        counter += 1

                if counter != 0:
                    edges_n_nodes[i] = counter  # nodes_n_edges[number_of_edges] = number_of_nodes

        # for key, value in edges_n_nodes.items():
        #     print("{} nodes has {} edges.".format(value, key))

        with open(f"Output_Files{path_escape}2D_data.txt", "w") as f:
            for key, value in sorted(edges_n_nodes.items(), key=operator.itemgetter(0), reverse=True):
                if value != 0:
                    f.write(f"{key} {value / self.num_of_vertices}\n")

            f.close()

    @classmethod
    def intRound(cls, x, base):
        return int(base * round(float(x)/base))

    @staticmethod
    def plot_2d(graph_adjacency_type):
        with open(f"Output_Files{path_escape}2D_data.txt") as f:
            connections = []
            probabilities = []
            graph_type = None
            number_of_vertices = None

            line = f.readline().replace("\n", "")
            while line:
                line = re.findall(r'(\b[0-9.]+)', line)
                connections.append(int(line[0]))
                probabilities.append(float(line[1]))

                line = f.readline().replace("\n", "")
            f.close()

        if graph_adjacency_type == "Matrix":
            f = open(f"Output_Files{path_escape}graph_analysis_matrix.txt")

        elif graph_adjacency_type == "List":
            f = open(f"Output_Files{path_escape}graph_analysis_list.txt")

        try:
            line = f.readline().replace("\n", "")
        except IndexError:
            pass

        while line:
            line = f.readline().replace("\n", "")
            try:
                line_split = line.split(":")[0]

                if line_split == "Graph type":
                    graph_type = line.split(":")[1].strip()
                    plt.title(line.split(":")[1].strip())

                if line_split == "Number of Vertices":
                    number_of_vertices = int(line.split(":")[1].strip())

            except IndexError:
                pass

        if "Scale-Free" in graph_type:
            plt.plot(connections, probabilities, ".")
        else:
            plt.plot(connections, probabilities, marker=".")

        plt.ylabel('Probability')
        plt.xlabel('Edges')

        if graph_type is None:
            plt.title("Unknown Graph")
        if number_of_vertices is None:
            number_of_vertices = 100

        if len(str(connections[0])) == 1:
            plt.xticks(range(0, Plot2D.intRound(connections[0], 5) + 1, 1))
        elif len(str(connections[0])) == 2:
            if connections[0] < 20:
                plt.xticks(range(0, Plot2D.intRound(connections[0], 5) + 1, 1))
            else:
                plt.xticks(range(0, Plot2D.intRound(connections[0], 5) + 1, 5))
        elif len(str(connections[0])) == 3:
            plt.xticks(range(0, Plot2D.intRound(connections[0], 5) + 1, 100))
        elif len(str(connections[0])) == 4:
            plt.xticks(range(0, Plot2D.intRound(connections[0], 5) + 1, 1000))
        elif len(str(connections[0])) == 5:
            plt.xticks(range(0, Plot2D.intRound(connections[0], 5) + 1, 10000))

        if "Scale-Free" in graph_type:
            plt.xscale("log")
            plt.yscale("log")
            plt.xlim(0, pow(10, len(str(connections[0]))))
            plt.ylim(0.0001, 1)
            plt.gca().xaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("{x:.0f}"))
            plt.gca().yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("{x:.3f}"))

        plt.show()
