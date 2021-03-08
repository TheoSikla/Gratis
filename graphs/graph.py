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

from enum import Enum


class GraphRepresentationType(Enum):
    """Enumeration Class for Graph Representation types"""

    MATRIX = 'matrix'
    LIST = 'list'


class GraphType(Enum):
    """Enumeration Class for Graph types"""

    HOMOGENEOUS = 'Homogeneous'
    ER = 'Erdos Renyi'
    CUSTOM_ER = 'Custom Erdos Renyi'
    RANDOM_FIXED = 'Random Fixed'
    SCALE_FREE = 'Scale Free'
    CUSTOM_SCALE_FREE = 'Custom Scale Free'


AVAILABLE_GRAPH_TYPES = [_.value for _ in GraphType]


class AbstractGraph:
    """Abstract class for Graph objects"""

    _representation_type: GraphRepresentationType = None
    _type: GraphType = None

    class Meta:
        abstract = True


class Graph(AbstractGraph):
    def __init__(self, repr_type, graph_type):
        """

        :param repr_type: Graph representation type (Matrix or List)
        :param graph_type: Type of Graph

        Attributes:
            :var vertices: A dictionary that hold the name of the vertex as key and the memory position as value
            :var edge_indices: A dictionary that hold the name of the vertex as key and the name's integer form as value
            :var edges: A list that holds the adjacency matrix, gradually is becoming a 2 dimension list if graph type
                        is Matrix else a dictionary that holds the adjacency list in form vertex:[neighbors]
        """
        self._type = graph_type
        self._representation_type = repr_type

        self.vertices = {}
        self.edge_indices = {}
        self.edges = [] if self.graph_representation_type is 'matrix' else {}

    @property
    def graph_representation_type(self):
        return self._representation_type.value

    @property
    def graph_type(self):
        return self._type.value

    def reset_graph(self):
        pass
