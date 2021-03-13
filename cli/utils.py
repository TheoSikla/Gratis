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

from cli.common import AVAILABLE_MESSAGE_PREFIXES, AVAILABLE_MESSAGE_PREFIX_COLOURS, MessageColor, MessageType
from graphs.er_graph import ErdosRenyi
from graphs.full_scale_free_graph import FullScaleFree
from graphs.graph import GraphType
from graphs.homogeneous import Homogeneous
from graphs.random_fixed_graph import RandomFixed
from graphs.scale_free_graph_pa import ScaleFreePA


def communicate_cli_message(message, _type):
    print(f'{AVAILABLE_MESSAGE_PREFIX_COLOURS[_type]}{AVAILABLE_MESSAGE_PREFIXES[_type]}{MessageColor.END.value} '
          f'{message}')


def validate_model_cli_arg_values(model: str, number_of_vertices=None, number_of_edges=None,
                                  number_of_initial_nodes=None, graph_degree=None, initial_connections_per_node=None,
                                  probability=None, seed=None) -> bool:

    if all(_ is None for _ in [number_of_vertices, number_of_edges, number_of_initial_nodes, graph_degree,
                               initial_connections_per_node, probability, seed]):
        return False

    # Ensure non negative and non zero numbers
    if any([_ is not None and float(_) <= 0 for _ in [number_of_vertices, number_of_edges, number_of_initial_nodes,
                                                      graph_degree, initial_connections_per_node, probability, seed]]):
        return False

    # Ensure more than 1 vertices
    if number_of_vertices <= 1:
        return False

    if model == GraphType.CUSTOM_ER.value:
        if number_of_edges > ((number_of_vertices * (number_of_vertices - 1)) // 2):
            communicate_cli_message(message=f'The maximum number of edges can be '
                                            f'{(number_of_vertices * (number_of_vertices - 1)) // 2} for '
                                            f'{number_of_vertices} vertices in an undirected graph',
                                    _type=MessageType.ERROR.value)
            return False
        if number_of_edges == ((number_of_vertices * (number_of_vertices - 1)) // 2):
            communicate_cli_message(message=f'The resulting graph for '
                                            f'{(number_of_vertices * (number_of_vertices - 1)) // 2} edges and for '
                                            f'{number_of_vertices} vertices will be a '
                                            f'{GraphType.HOMOGENEOUS.value} graph',
                                    _type=MessageType.WARNING.value)
            return True

    if model == GraphType.CUSTOM_SCALE_FREE.value:
        if number_of_edges is not None:
            if not all([_ is None for _ in [number_of_initial_nodes, initial_connections_per_node]]):
                return False
            if number_of_edges > ((number_of_vertices * (number_of_vertices - 1)) // 2):
                communicate_cli_message(message=f'The maximum number of edges can be '
                                                f'{(number_of_vertices * (number_of_vertices - 1)) // 2} for '
                                                f'{number_of_vertices} vertices in an undirected graph',
                                        _type=MessageType.ERROR.value)
                return False
            if number_of_edges == ((number_of_vertices * (number_of_vertices - 1)) // 2):
                communicate_cli_message(message=f'The resulting graph for '
                                                f'{(number_of_vertices * (number_of_vertices - 1)) // 2} edges and for '
                                                f'{number_of_vertices} vertices will be a '
                                                f'{GraphType.HOMOGENEOUS.value} graph',
                                        _type=MessageType.WARNING.value)
            return True
        if number_of_edges is None:
            if any([_ is None for _ in [number_of_initial_nodes, initial_connections_per_node]]):
                return False
            if initial_connections_per_node > ((number_of_initial_nodes * (number_of_initial_nodes - 1)) // 2):
                communicate_cli_message(message=f'The maximum number of edges can be '
                                                f'{(number_of_initial_nodes * (number_of_initial_nodes - 1)) // 2} for '
                                                f'{number_of_initial_nodes} initial vertices in an undirected graph',
                                        _type=MessageType.ERROR.value)
                return False
    return True


def validate_model_cli_args(args) -> bool:
    try:
        if not args.model:
            return False
        if args.model == GraphType.HOMOGENEOUS.value and (
                args.number_of_vertices is None or
                not validate_model_cli_arg_values(model=GraphType.HOMOGENEOUS.value,
                                                  number_of_vertices=args.number_of_vertices)
        ):
            return False
        elif args.model == GraphType.ER.value and (
                any([_ is None for _ in [args.number_of_vertices, args.probability, args.seed]]) or
                not validate_model_cli_arg_values(model=GraphType.ER.value, number_of_vertices=args.number_of_vertices,
                                                  probability=args.probability, seed=args.seed)
        ):
            return False
        elif args.model == GraphType.CUSTOM_ER.value and (
                any([_ is None for _ in [args.number_of_vertices, args.number_of_edges, args.probability, args.seed]])
                or not validate_model_cli_arg_values(model=GraphType.CUSTOM_ER.value,
                                                     number_of_vertices=args.number_of_vertices,
                                                     number_of_edges=args.number_of_edges, probability=args.probability,
                                                     seed=args.seed)
        ):
            return False
        elif args.model == GraphType.RANDOM_FIXED.value and (
                any([_ is None for _ in [args.number_of_vertices, args.graph_degree, args.seed]]) or
                not validate_model_cli_arg_values(model=GraphType.RANDOM_FIXED.value,
                                                  number_of_vertices=args.number_of_vertices,
                                                  graph_degree=args.graph_degree, seed=args.seed)
        ):
            return False
        elif args.model == GraphType.SCALE_FREE.value and (
                any([_ is None for _ in [args.number_of_vertices, args.seed]]) or
                not validate_model_cli_arg_values(model=GraphType.SCALE_FREE.value,
                                                  number_of_vertices=args.number_of_vertices,
                                                  number_of_initial_nodes=args.number_of_initial_nodes, seed=args.seed)
        ):
            return False
        elif args.model == GraphType.CUSTOM_SCALE_FREE.value and (
                any([_ and _ is None for _ in [args.number_of_vertices, args.seed]]) or
                (
                    args.number_of_edges is None and
                    any([_ is None for _ in [args.number_of_initial_nodes, args.initial_connections_per_node]])
                ) or not validate_model_cli_arg_values(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                       number_of_vertices=args.number_of_vertices,
                                                       number_of_edges=args.number_of_edges,
                                                       number_of_initial_nodes=args.number_of_initial_nodes,
                                                       initial_connections_per_node=args.initial_connections_per_node,
                                                       seed=args.seed)

        ):
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
                                                               number_of_edges=args.number_of_edges,
                                                               probability=args.probability,
                                                               seed=args.seed)
    elif args.model == GraphType.RANDOM_FIXED.value:
        RandomFixed(args.adjacency_type).create_random_fixed_graph(number_of_vertices=args.number_of_vertices,
                                                                   graph_degree=args.graph_degree,
                                                                   seed=args.seed)
    elif args.model == GraphType.SCALE_FREE.value:
        if not args.number_of_initial_nodes:
            # Scale Free with Preferential Attachment
            ScaleFreePA(args.adjacency_type).create_scale_free_graph(number_of_vertices=args.number_of_vertices,
                                                                     seed=args.seed)
        else:
            # Full Scale Free with Preferential Attachment and Incremental Growth
            FullScaleFree(args.adjacency_type).create_full_scale_free_graph(
                number_of_vertices=args.number_of_vertices,
                number_of_initial_nodes=args.number_of_initial_nodes,
                seed=args.seed)
    elif args.model == GraphType.CUSTOM_SCALE_FREE.value:
        if args.number_of_edges:
            # Custom Scale Free with Preferential Attachment
            ScaleFreePA(args.adjacency_type).create_custom_scale_free_graph(
                number_of_vertices=args.number_of_vertices,
                number_of_edges=args.number_of_edges,
                seed=args.seed)
        elif args.number_of_initial_nodes and args.initial_connections_per_node:
            # Custom Full Scale Free with Preferential Attachment and Incremental Growth
            FullScaleFree(args.adjacency_type).create_full_scale_free_graph(
                number_of_vertices=args.number_of_vertices,
                number_of_initial_nodes=args.number_of_initial_nodes,
                initial_connections_per_node=args.initial_connections_per_node,
                seed=args.seed)
    else:
        communicate_cli_message('Unknown graph model', MessageType.ERROR.value)
        sys.exit(1)
