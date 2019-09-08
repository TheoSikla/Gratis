__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

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
