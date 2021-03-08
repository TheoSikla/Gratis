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
from graphs.er_graph import ErdosRenyi
from graphs.graph import GraphType
from graphs.homogeneous import Homogeneous
from graphs.random_fixed_graph import RandomFixed


def validate_model_cli_args(args):
    try:
        if args.model == GraphType.HOMOGENEOUS.value and args.number_of_vertices is None:
            return False
        elif args.model == GraphType.ER.value and (
                any([_ is None for _ in [args.number_of_vertices, args.probability, args.seed]])):
            return False
        elif args.model == GraphType.CUSTOM_ER.value and (
                any([_ is None for _ in [args.number_of_vertices, args.number_of_edges, args.probability, args.seed]])):
            return False
        elif args.model == GraphType.RANDOM_FIXED.value and (
                any([_ is None for _ in [args.number_of_vertices, args.graph_degree, args.seed]])):
            return False
        elif args.model in [GraphType.SCALE_FREE.value, GraphType.CUSTOM_SCALE_FREE.value] and (
                any([_ is None for _ in [args.number_of_vertices, args.seed]])):
            return False
        return True
    except AttributeError:
        return False


def handle_graph_creation(args):
    if args.model == GraphType.HOMOGENEOUS.value:
        Homogeneous(args.adjacency_type).create_homogeneous_graph(number_of_vertices=args.number_of_vertices)
    elif args.model == GraphType.ER.value:
        ErdosRenyi(args.adjacency_type).create_er_graph(number_of_vertices=args.number_of_vertices,
                                                        probability=args.probability,
                                                        seed=args.seed)
    elif args.model == GraphType.CUSTOM_ER.value:
        ErdosRenyi(args.adjacency_type).create_custom_er_graph(number_of_vertices=args.number_of_vertices,
                                                               total_number_of_edges=args.number_of_edges,
                                                               probability=args.probability,
                                                               seed=args.seed)
