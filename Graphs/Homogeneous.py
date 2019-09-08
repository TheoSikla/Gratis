__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

from Analyze.Analyze import *
from Generate.Generate import *
from Graphs.vertex import Vertex
from Graphs.graph_adjacency_list import AdjacencyListGraph
from Graphs.graph import GraphRepresentationType, GraphType
from Graphs.graph_adjacency_matrix import AdjacencyMatrixGraph


class Homogeneous:
    """
        This class creates a homogeneous graph and an adjacency matrix based on the number of vertices given by the
        user interface.
        Homogeneous graph is a graph that has all its vertices connected with each other.
    """

    def __init__(self, graph_representation_type):
        if graph_representation_type == str(GraphRepresentationType.MATRIX):
            self.graph = AdjacencyMatrixGraph(GraphRepresentationType.MATRIX, GraphType.HOMOGENEOUS)
        else:
            self.graph = AdjacencyListGraph(GraphRepresentationType.LIST, GraphType.HOMOGENEOUS)

    def create_homogeneous_graph(self, number_of_vertices, thread, **kwargs):
        self.graph.reset_graph()

        if self.graph.graph_representation_type == "matrix":
            if kwargs.get('rle'):
                self.graph.mode = "memory efficient"

        for i in range(number_of_vertices):
            self.graph.add_vertex(Vertex(str(i)))
            if thread.isStopped():
                sys.exit(0)

        for i in range(number_of_vertices):
            for j in range(number_of_vertices):
                if i != j and i < j:
                    self.graph.add_edge_undirected(i, j)
                    if thread.isStopped():
                        sys.exit(0)

        generator.generate(self.graph.graph_representation_type, self.graph, thread)
        analyzer.analyze_generated_graph(self.graph.edges, self.graph.graph_representation_type,
                                         self.__class__.__name__.replace("_", " "), number_of_vertices)
