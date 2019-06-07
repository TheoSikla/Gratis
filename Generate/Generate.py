import sys
from os_recon.define_os import path_escape


class Generate:

    @staticmethod
    def generate(adjacency_type, graph, thread):
        """ Generates the file that will be used to visualize the graph. """

        file_output = ''

        if adjacency_type == "Matrix":
            
            for i in range(len(graph.edges)):
                if thread.isStopped():
                    graph.reset_graph()
                    f.close()
                    sys.exit(0)

                for j in range(len(graph.edges)):
                    if graph.edges[i][j] == 1:
                        file_output += '1'
                    else:
                        file_output += '0'
                file_output += '\n'
            
        else:

            for vertex, neighbors in graph.neighbors.items():
                if thread.isStopped():
                    graph.reset_graph()
                    f.close()
                    sys.exit(0)

                file_output += f"{vertex}:"

                for node in graph.neighbors[vertex]:
                    file_output += f"{node},"
                
                file_output = file_output[:-1]
                file_output += "\n"
        
        if adjacency_type == "Matrix":

            with open("Output_Files{}matrix.txt".format(path_escape), "w") as f:
                f.write(file_output)
                f.close()
        else:
            
            with open("Output_Files{}list.txt".format(path_escape), "w") as f:
                f.write(file_output)
                f.close()


generator = Generate()
