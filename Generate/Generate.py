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
from os_recon.define_os import path_escape
from Support_Folders.run_length_encoder import RunLengthEncoder


class Generate:

    @staticmethod
    def generate(adjacency_type, graph, thread):
        """ Generates the file that will be used to visualize the graph. """

        file_output = ''

        if adjacency_type == "matrix":
            if hasattr(graph, 'mode'):
                if graph.mode == 'normal':
                    for i in range(len(graph.edges)):
                        if thread.isStopped():
                            graph.reset_graph()
                            sys.exit(0)

                        for j in range(len(graph.edges)):
                            if graph.edges[i][j] == 1:
                                file_output += '1'
                            else:
                                file_output += '0'
                        file_output += '\n'
                else:
                    encoder = RunLengthEncoder()
                    for row in graph.edges:
                        if thread.isStopped():
                            graph.reset_graph()
                            sys.exit(0)

                        row = ''.join([str(x) for x in row])

                        file_output += encoder.encode(row) + '\n'
            else:
                raise Exception("Graph without mode found.")
            
        else:
            for vertex, edges in graph.edges.items():
                if thread.isStopped():
                    graph.reset_graph()
                    sys.exit(0)

                file_output += f"{vertex}:"
                if len(edges) > 0:
                    for node in graph.edges[vertex]:
                        file_output += f"{node},"

                    file_output = file_output[:-1]
                file_output += "\n"
        
        if adjacency_type == "matrix":

            with open(f"Output_Files{path_escape}matrix.txt", "w") as f:
                f.write(file_output)
        else:
            
            with open(f"Output_Files{path_escape}list.txt", "w") as f:
                f.write(file_output)

        del file_output


generator = Generate()
