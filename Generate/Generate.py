import sys
from os_recon.define_os import path_escape


class Generate:

    @staticmethod
    def generate(adjacency_type, graph, thread):
        """ Generates the file that will be used to visualize the graph. """

        if adjacency_type == "Matrix":
            with open("Output_Files{}matrix.txt".format(path_escape), "w") as f:
                for i in range(len(graph.edges)):
                    if thread.isStopped():
                        graph.reset_graph()
                        f.close()
                        sys.exit(0)

                    for j in range(len(graph.edges)):
                        if graph.edges[i][j] == 1:
                            f.write('1')
                        else:
                            f.write('0')
                    f.write('\n')
                f.close()

        else:
            with open("Output_Files{}list.txt".format(path_escape), "w") as f:
                for vertex, neighbors in graph.neighbors.items():
                    if thread.isStopped():
                        graph.reset_graph()
                        f.close()
                        sys.exit(0)

                    f.write("{}:".format(vertex))
                    for node in graph.neighbors[vertex]:
                        if node == graph.neighbors[vertex][-1]:
                            f.write("{}".format(node))
                        else:
                            f.write("{},".format(node))

                    f.write('\n')
                f.close()


generator = Generate()
