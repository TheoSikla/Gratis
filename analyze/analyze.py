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

import re
import datetime
from os.path import join
from tkinter import END
from tkinter import messagebox

from conf.base import OUTPUT_FILES_DIRECTORY
from sqlite3_db.database import Graph
from os_recon.define_os import path_escape


class Analyze:

    def __init__(self):
        self.version = 'Gratis v1.0'

    def analyze_generated_graph(self, graph_representation, graph_representation_type,
                                graph_type, number_of_vertices, graph_degree=None,
                                number_of_edges=None, number_of_initial_nodes=None,
                                initial_connections_per_node=None, probability=None, seed=None):
        
        """ Analyzes a generated graph. """
        with open(join(OUTPUT_FILES_DIRECTORY, f'graph_analysis_{graph_representation_type.lower()}.txt'), "w") as f:
            analysis = {
                        'Graph_Representation_Type': graph_representation_type,
                        'Graph_Type': graph_type,
                        'Number_Of_Vertices': number_of_vertices,
                        'Graph_Degree': graph_degree,
                        'Number_Of_Maximum_Edges': number_of_edges,
                        'Number_Of_Initial_Nodes': number_of_initial_nodes,
                        'Initial_Connections_Per_Node': initial_connections_per_node,
                        'Probability': probability,
                        'Seed': seed
                        }

            # Graph Analysis
            connections = 0
            number_of_edges_per_node = [0] * number_of_vertices

            if graph_representation_type == "matrix":
                for i in range(len(graph_representation)):
                    for j in range(len(graph_representation)):
                        if i != j and i < j:
                            if graph_representation[i][j] >= 1:
                                number_of_edges_per_node[i] += 1
                                number_of_edges_per_node[j] += 1
                                connections += 1
            else:
                for vertex, neighbors in graph_representation.items():
                    number_of_edges = 0
                    for _ in neighbors:
                        number_of_edges += 1

                    number_of_edges_per_node[int(vertex)] = number_of_edges
                    connections += number_of_edges

                connections = connections // 2

            first = 0
            highest_node_indicator = 0
            for i in range(number_of_vertices):
                if number_of_edges_per_node[i] > first:
                    highest_node_indicator = i
                    first = number_of_edges_per_node[i]

            analysis['Total_Number_Of_Edges'] = connections

            # ====================================================
            output = ''
            output += f"[*] Starting last generated Graph Analysis...\n"
            output += "===================================\n"
            output += f"Version: {self.version}\n"

            for k, v in analysis.items():
                if v is not None:
                    output += f"{k.replace('_', ' ')}: {v}\n"

            try:
                output += f"Node {highest_node_indicator + 1} has the most edges ({first})\n"

            except NameError:
                pass

            output += f"The date is: {datetime.datetime.today().strftime('%m/%d/%Y')}\n"
            output += "===================================\n\n"
            
            f.write(output)
            del output

            graph_connection_handler = Graph()
            graph_connection_handler.create(analysis)
            graph_connection_handler.close()

    @staticmethod
    def read_analysis(adjacency_type, text_area):

        text_area.delete('1.0', END)
        text_area.update()

        try:
            with open(join(OUTPUT_FILES_DIRECTORY, f'graph_analysis_{adjacency_type.lower()}.txt'), 'r') as f:
                for line in f:
                    text_area.insert(END, line)
                text_area.update()
        except FileNotFoundError:
            message = f"Please generate a graph first!"
            messagebox.showerror("Error", message)

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

                    text = f"Node {node_names[counter]:<{len(node_names[-1])}} has {int(v):<{len(str(v))}} edges.\n"
                    
                    text_area.insert(END, text)
                    text_area.update()
                    counter += 1

                text = f"\nNode {node_names[node_most_edges]} has the most edges ({max_edges})!\n\n"

                text_area.insert(END, text)
                text_area.update()

                return True

        except FileNotFoundError:
            message = "File not found!"
            messagebox.showerror("Error", message)
            return False


analyzer = Analyze()
