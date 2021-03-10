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

from cli.common import AVAILABLE_MESSAGE_PREFIXES, AVAILABLE_MESSAGE_PREFIX_COLOURS, MessageColor
from graphs.er_graph import ErdosRenyi
from graphs.full_scale_free_graph import FullScaleFree
from graphs.graph import GraphType
from graphs.homogeneous import Homogeneous
from graphs.random_fixed_graph import RandomFixed
from graphs.scale_free_graph_pa import ScaleFreePA


def communicate_cli_message(message, _type):
    print(f'{AVAILABLE_MESSAGE_PREFIX_COLOURS[_type]}{AVAILABLE_MESSAGE_PREFIXES[_type]}{MessageColor.END.value} '
          f'{message}')


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
        elif args.model == GraphType.SCALE_FREE.value and (
                any([_ is None for _ in [args.number_of_vertices, args.seed]])):
            return False
        elif args.model == GraphType.CUSTOM_SCALE_FREE.value and (
                any([_ and _ is None for _ in [args.number_of_vertices, args.seed]]) or
                (
                    args.number_of_edges is None and
                    any([_ is None for _ in [args.number_of_initial_nodes, args.number_of_initial_edges]])
                )

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
                                                               total_number_of_edges=args.number_of_edges,
                                                               probability=args.probability,
                                                               seed=args.seed)
    elif args.model == GraphType.RANDOM_FIXED.value:
        RandomFixed(args.adjacency_type).create_random_fixed_graph(number_of_vertices=args.number_of_vertices,
                                                                   connectivity=args.graph_degree,
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
                total_number_of_edges=args.number_of_edges,
                seed=args.seed)
        elif args.number_of_initial_nodes and args.number_of_initial_edges:
            # Full Scale Free with Preferential Attachment and Incremental Growth
            FullScaleFree(args.adjacency_type).create_full_scale_free_graph(
                number_of_vertices=args.number_of_vertices,
                number_of_initial_nodes=args.number_of_initial_nodes,
                number_of_initial_edges=args.number_of_initial_edges,
                seed=args.seed)


